from typing import TypedDict, Annotated, Any

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import add_messages, StateGraph

from app.services.vectordb_service import search_collection

# We're going to rewrite the langgraph_service to be an actual AGENTIC Graph now
    # No more keyword matching
# We're going to define tools that the LLM can decide to use
# This is an example of AGENTIC AI. Our AI has the /agency/ to decide which tool to use

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

# =======================(TOOL DEFINITIONS)======================== #

# Remember, tools are just Python functions our agent can choose to use.
# BUT they have a @tool decorator and a docstring defining the tool's purpose

@tool(name_or_callable="search_games")
def search_games_tool(query:str) -> list[dict[str, Any]]:
    """
    This tool performs a similarity search on the video_games VectorDB collection. 
    This is primarily for video game recommendations and suggestions. 
    The result of this tool is a list of relevant video games for RAG functionality
    """
    return search_collection(collection_name="video_games", query=query, k=5)

@tool(name_or_callable="search_reviews")
def search_reviews_tool(query:str) -> list[dict[str, Any]]:
    """
    This tool performs a similarity search on the critic_reviews VectorDB collection.
    This is for users curious about others thoughts on certain games.
    The result of this tool is a list of relevant excerpts from critic reviews.
    """
    return search_collection(collection_name="critic_reviews", query=query, k=5)

# A List of the available Tools
TOOLS = [search_games_tool, search_reviews_tool]

# Map the tool names to their functions in a dict (so we can call them later)
TOOL_MAP = {tool.name: tool for tool in TOOLS}
# Each value looks like: "search_games": <search_games_tool function call>

# Get a version of the LLM that's aware of the tools
llm_with_tools = llm.bind_tools(TOOLS)

# =========================(NODE DEFINITIONS)======================= #

# We're not doing away with nodes!
# It's just that those 2 tools up there are no longer nodes.

# Here's our AGENTIC BEHAVIOR - an AGENTIC ROUTER! (Instead of keyword matching)
def agentic_router_node(state:GraphState) -> GraphState:

    # Get the query from state
    query = state.get("query", "").lower()

    # Prompt the LLM to decide which tool to use based on the query (AGENCY!)
    # Using a slightly different chat prompt style, just cuz I saw it
    messages = [
        SystemMessage(content=(
            """
            You are an internal decision making assistant for a user-facing AI chatbot.
            
            If the user is asking about video game recommendations or general info, 
            use the "search_games" tool. 
            
            If the user is asking specifically about critic reviews or opinions, 
            use the "search_reviews" tool. 
            
            You must always call at least one tool. DO NOT answer the user without tools.
            Feel free to call multiple tools.  
            """
        )),
        HumanMessage(content=query)
    ]

    # Call the LLM to decide which tool to use
    agentic_response = llm_with_tools.invoke(messages)
    # agentic_response contains the chosen tool(s).

    print(agentic_response.tool_calls)

    # Invoke whatever tools were called and store the results in state
    for tool_call in agentic_response.tool_calls:
        tool_name = tool_call["name"]

        # Look up the tool function from the TOOL_MAP and call it with the provided args
        if tool_name in TOOL_MAP:

            tool_function = TOOL_MAP[tool_name]
            tool_result = tool_function.invoke(query) # Unpack the args

            print(tool_result)

            # Save the tool result in state - we can use this in later nodes (like a RAG node)
            return {"docs":tool_result}

# RAG NODE - The same as in the non-agentic LangGraph Service
def rag_node(state:GraphState) -> GraphState:

    query = state.get("query", "")
    docs = state.get("docs", [])

    prompt=f"""Respond to the User's Query based on the provided Search Results - 
           ONLY use the provided Search Results 
           or say you don't have any results if there are no provided Search Results. 
            
           User's Query: {query}
           Search Results: {docs} """

    # Invoke the LLM and save the answer in state
    answer = llm.invoke(prompt)
    return {"answer": answer.text}


# ===================(GRAPH BUILDER)=================== #

# Mostly the same, just a bit different node config and no routing.
def build_agentic_graph():

    # Define the Builder with State
    builder = StateGraph(GraphState)

    # Register the Nodes
    builder.add_node("route", agentic_router_node)
    builder.add_node("rag", rag_node)

    # Define starting node
    builder.set_entry_point("route")

    # Define one edge - router node flows to rag node
    builder.add_edge("route", "rag")

    # Define terminal node
    builder.set_finish_point("rag")

    # Compile and build!
    return builder.compile()

# I like to build the graph here as a singleton. This is what we'll use in the endpoint
agentic_graph = build_agentic_graph()