from typing import TypedDict, Annotated, Any

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import add_messages, StateGraph

from app.services.vectordb_service import search_collection

"""
We're going to make another conversational chatbot functionality
But this time, it'll be able to CHOOSE what VectorDB Collection if pulls from

We'll define tools with good descriptions so the LLM can make an informed choice
BASED ON the user's query

This is an example of AGENTIC AI. Our LLM has the AGENCY to choose a tool to use
"""

# First, define the LLM like before
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=.1 # very little creativity
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


# ================= (TOOLS) =================== #

# Tools are just Python functions that our agent can choose to use.
# We have a special @tool decorator,
# and we need to provide descriptions of what the tool does via the """docstring"""

@tool(name_or_callable="search_monster_tools")
def search_monster_tools(query:str) -> list[dict[str, Any]]:
    """
    Search the monster tools collection in VectorDB for relevant chunks.
    Call this tool if the user is asking for defense mechanisms against monsters,
    or just expressing fear in general. Anything that implies that they have monsters to fight.

    :param query: The user's query
    :return: A list of dictionaries containing relevant chunks from the VectorDB.
    """
    return search_collection(collection_name="monster_fighting_tools", query=query)

@tool(name_or_callable="search_incident_reports")
def search_incident_reports(query:str) -> list[dict[str, Any]]:
    """
    Search the incident reports collection in VectorDB for relevant chunks.
    Call this tool if the user is asking about monster attacks, sightings, or other incidents.
    Anything that implies that they're curious about recent monster-related events.

    :param query: The user's query
    :return: A list of dictionaries containing relevant chunks from the VectorDB.
    """
    return search_collection(collection_name="monster_incident_reports", query=query)

# A List of the available tools
TOOLS = [search_monster_tools, search_incident_reports]

# Map the tool names to their functions (helps us call them dynamically
TOOL_MAP = {tool.name: tool for tool in TOOLS}
# Each pair will look like: "search_monster_tools": <function call for search_monster_tools>

# Supply the LLM with the tools we made. THIS is the object we'll be invoking for RAG
llm_with_tools = llm.bind_tools(TOOLS)

# ================== (NODES) ====================== #

# A Node is like a "step" in the Graph. Functions that may or may not be invoked
# Nodes have read/write access to the GraphState
    # This helps us with our branching capabilities in LangGraph

# Our first Node - kind of like a front controller - it decides what to do first
# Based on the user's query, which tool should I call?
def agentic_router_node(state:GraphState) -> GraphState:

    # Get the user's query from state
    query = state.get("query")

    # Prompt the LLM to decide which tool to use based on the query (AGENCY!)
    messages = [
        SystemMessage(content=(
            """
            You are an internal decision making assistant for a user-facing AI chatbot.
            
            If the user is asking about their fear of monsters, or weapons to fight monsters,  
            use the "search_monster_tools" tool. 
            
            If the user is asking specifically about current events and monster sightings,  
            use the "search_incident_reports" tool. 
            
            You must always call at least one tool. DO NOT answer the user without tools.
            Feel free to call multiple tools.  
            """
        )),
        HumanMessage(content=query)
    ]

    # Call the LLM, which will choose which tool to call
    response = llm_with_tools.invoke(messages)
    # This response contains the tool call

    print(response.tool_calls) # Just to see what was called

    # Invoke whatever tool was called and store the results in state
    for tool_call in response.tool_calls:

        tool_name = tool_call["name"]
        tool_function = TOOL_MAP[tool_name]
        tool_result = tool_function.invoke("query")

        print(tool_result) # Visibility

        # Save the result in state - this data will be used for RAG in the next node
        return {"docs": tool_result}

# One more node - does the RAG with the data stored in state
def rag_node(state:GraphState) -> GraphState:

    # Get the query and docs from state
    query = state.get("query")
    docs = state.get("docs")

    prompt = f"""Respond to the user's Query based on the provided Search Results.
                ONLY use the provided search results to answer the user's query.
                
                The User's Query: {query}
                The Search Results: {docs}
            """

    # Invoke!
    return {"answer": llm.invoke(prompt).text}


# ============= (GRAPH BUILDER) ============== #

# Now that we've all the stuff above (state, tools, nodes), we have to TIE THEM TOGETHER!

def build_agentic_graph():

    # Define a builder object (using our GraphState)
    builder = StateGraph(GraphState)

    # Register the nodes
    builder.add_node("agentic_router", agentic_router_node)
    builder.add_node("rag_node", rag_node)

    # Define the starting node
    builder.set_entry_point("agentic_router")

    # Define an Edge (how nodes flow to one another)
    builder.add_edge("agentic_router", "rag_node")

    # Define the terminal (final) node
    builder.set_finish_point("rag_node")

    # Compile and build!
    return builder.compile()

# I like to build the Graph as a Singleton. This is what we'll call in the Router
agentic_graph = build_agentic_graph()