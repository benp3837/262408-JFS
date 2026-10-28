from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, add_messages
from langgraph.graph.state import CompiledStateGraph

from app.services.vectordb_service import search_collection

# This service will define the State, Nodes, and overall Graph
# This is a GRAPH-BASED workflow with LangGraph (as opposed to chain-based with LangChain)

# First, define the LLM like before
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.1
)

# Define the State Object for the Graph - stores temp data we want to keep track of
# Each Node in the Graph can read/write to this state object
class GraphState(TypedDict, total=False): # total=False makes the fields optional
    query:str # The user's query to the LLM
    answer:str # The LLM's answer to the query
    docs:list[dict] # Retrieved documents from a VectorDB search
    route:str # The "routing" decision we make. Determines which Node executes next

    # State field to store message history
    # This gets stored across graph invocations so the LLM remembers what we're talking about
    # add_messages is a reducer that merges the user/AI interactions into one list
    message_memory:Annotated[list[BaseMessage], add_messages]

# ======================(Node Definitions)============================= #

# Each Node is like a "step" in the Graph. Functions that may or may not be invoked
# Nodes have read/write access to the GraphState

# Our first Node - kind of like a Front Controller - The ROUTING NODE
# When the user sends a query, this node decides which path to take
def route_node(state:GraphState) -> GraphState:

    # Get the user's query from state - default to empty string if not present
    query = state.get("query", "").lower()

    # VERY simple keyword matching (FOR NOW) to determine the route
    # Fallback to general chat node if no keywords match
    if any(word in query for word in ["recommend", "recs", "suggest"]):
        return {"route": "recs"}
    elif any(word in query for word in ["review", "critic", "critics"]):
        return {"route": "reviews"}
    else:
        return {"route":"general_chat"}

# Node that queries the video_games VectorDB collection
def search_games_node(state:GraphState) -> GraphState:

    # Get the query from state
    query = state.get("query", "").lower()

    # Similarity search, same function we made earlier
    results = search_collection("video_games", query, k=5)

    # Save the results in state!
    return {"docs": results}


# Node that queries the critic_reviews VectorDB collection
def search_reviews_node(state:GraphState) -> GraphState:

    # Get the query from state
    query = state.get("query", "").lower()

    # Similarity search, same function we made earlier
    results = search_collection("critic_reviews", query, k=5)

    # Save the results in state!
    return {"docs": results}

# Node that uses the VectorDB results to generate a RAG response
def rag_node(state:GraphState) -> GraphState:

    # Ultimately, this node just invokes the LLM using retrieved data. We've done this

    # Get the query and docs from state
    query = state.get("query", "")
    docs = state.get("docs", [])

    # Basic prompt - kept it basic cuz this Service is already long
    prompt=f"""Respond to the User's Query based on the provided Search Results - 
           ONLY use the provided Search Results or say you don't know 
            
           User's Query: {query}
           Search Results: {docs} """

    # Invoke the LLM and save the answer in state
    answer = llm.invoke(prompt)
    return {"answer": answer.text}


# Node that handles general chat queries (no keywords detected)
def general_chat_node(state:GraphState) -> GraphState:

    # Get the query, define a prompt, and answer the question!
    query = state.get("query", "")

    prompt=(
        f"""You are a general chat bot with a southern twang. 
        You answer the user's general queries in a concise way. 
        You have context from previous 3 interactions: {state.get("message_memory")[-6:]}

        User Query: {query}
        Your Answer: """
    )

    answer = llm.invoke(prompt)

    # NOTE: we are using our memory manager here!
    return {"answer": answer.text,
            "message_memory": [
                HumanMessage(content=query),
                AIMessage(content=answer.text)
            ]}

# ==================(End of Node Definitions)======================== #

# Finally, we can define the overall structure of the Graph
# This function is what BUILDS OUR GRAPH. We define the Nodes and how they flow (Edges)
def build_graph():

    # First, define the graph builder which will be used throughout this method
    builder = StateGraph(GraphState) # This is a "StateGraph". A Graph that uses state

    # Register each Node - defining the name to call them by and the function to invoke
    builder.add_node("route", route_node)
    builder.add_node("search_games", search_games_node)
    builder.add_node("search_reviews", search_reviews_node)
    builder.add_node("rag", rag_node)
    builder.add_node("general_chat", general_chat_node)

    # Define the "entry node" - the node that starts the Graph by taking the user's query
    builder.set_entry_point("route")

    # Set up a "conditional edge" for condition node invocation
    # Depending on the value of the "route" state field, call one of the nodes
    builder.add_conditional_edges(
        source="route", # After route node, run this conditional to determine the next node
        path=lambda state: state.get("route", ""), # Determine the path based on the "route" state field
        path_map={
            "recs": "search_games", # If route is "recs", go to search_games_node
            "reviews": "search_reviews",
            "general_chat": "general_chat"
        }
    )

    # Adding generic edges - after either search node runs, invoke the RAG node
    builder.add_edge("search_games", "rag")
    builder.add_edge("search_reviews", "rag")

    # Finally, we'll define the terminal nodes (where the graph can end) and return the built graph
    builder.set_finish_point("rag") # After the RAG node runs, end the graph
    builder.set_finish_point("general_chat")

    # NOTE: Using an in-memory checkpointer here so we can persist message memory
    return builder.compile(checkpointer=MemorySaver())


# Instantiate a single Graph object that we'll use in the router
# (Singleton pattern, we only need one instance of the Graph at a time)
graph = build_graph()