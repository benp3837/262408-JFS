# TODO: Ben - talk about what this service will do
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# Define the LLM we're going to use
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=.5 # from 0-1. higher temp = more creativity
)

# Define a general prompt to help us define the LLM's persona
# We define system instructions, then pass along the user's input
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a evil scientist chatbot that answers questions."
               "You give helpful concise advice."),
    ("user", "{input}")
])

# Basic general chain that we'll call in the router for char functionality
def get_general_chain():

    # return a chain! This syntax is called "LCEL" LangChain Expression Language
        # Pass in the prompt
        # Pass in the LLM
        # This will get returned to the router to get invoked
    return prompt | llm

