# TODO: Ben - talk about what this service will do
from langchain_classic.chains.conversation.base import ConversationChain
from langchain_classic.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# Define the LLM we're going to use
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=.9 # from 0-1. higher temp = more creativity
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


# Create a different chain that has conversational memory
# This is gonna be very taxing on our local LLMs
def get_memory_chain():

    # Create a memory object

    # Window memory - remembers the last "k" interactions
    ### memory = ConversationBufferWindowMemory(k=3)

    # Summary memory - keeps a running paragraph of what we've talked about
    memory = ConversationSummaryMemory(llm=llm)
    # Our LLM is doing the summarization THEN generating a response... expensive

    # Similar prompt, but with history attached
    # These older memory classes expect a {history} prompt variable
    memory_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a evil scientist chatbot that answers questions."
                   "You give helpful concise advice."),
        ("user", "Conversation History: {history}"
                 "Current Input: {input}")
    ])

    # Make and return a chain in the old fashioned way (NOT using LCEL)
    return ConversationChain(
        llm = llm,
        memory = memory,
        prompt = memory_prompt
    )