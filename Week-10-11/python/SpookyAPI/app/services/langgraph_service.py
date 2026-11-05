from typing import TypedDict, Annotated, Any

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.graph import add_messages

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

    

    pass




