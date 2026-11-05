

"""
We're going to make another conversational chatbot functionality
But this time, it'll be able to CHOOSE what VectorDB Collection if pulls from

We'll define tools with good descriptions so the LLM can make an informed choice
BASED ON the user's query

This is an example of AGENTIC AI. Our LLM has the AGENCY to choose a tool to use
"""
from typing import TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from langgraph.graph import add_messages

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
