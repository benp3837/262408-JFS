import boto3
from langchain_aws import ChatBedrock
from langchain_classic.chains.conversation.base import ConversationChain
from langchain_classic.chains.transform import TransformChain
from langchain_classic.memory import ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# This Service will hold different functions for chain creation
# A chain is a series of steps taken to communicate with an LLM

# Define the LLM we're using (Llama3.2)
# llm = ChatOllama(
#     model="llama3.2:3b", # The name of the model we're using
#     temperature=0.5 # How "creative" the LLM can be. 0 - not at all. 1 - very creative.
# )

# Using Amazon Bedrock's Nova model instead
llm = ChatBedrock(
    model_id="amazon.nova-micro-v1:0",
    region_name="us-east-1",
    temperature=0.5,
)

# Define the prompt (instructions for the LLM. How to respond, tone, restrictions, etc.)
prompt = ChatPromptTemplate.from_messages([
    ("system",
     """
     You are a helpful, snarky, and nerdy chat bot that answers questions about video games.
     Imagine you're like a clerk at a video game store, and you're a know-it-all.
     
     You give brief but informative answers, and you are very opinionated.
     You love to give recommendations and refer to critic reviews when answering questions.
     
     You only answer questions about games or gaming culture.
     You don't provide further suggestions beyond what the user asks for.
     """),
    ("user", "{input}")
])

# First basic chain
def get_basic_chain():

    # This is a basic chain - it consists of:
        # a prompt
        # an LLM that will use that prompt to answer user queries
    # This pipe-based syntax is LCEL (LangChain Expression Language)
    chain = prompt | llm

    # This chain will get invoked by endpoints in our router!
    return chain

# Sequential Chain - take the initial LLM output and feed it into another LLM invocation
def get_sequential_chain():

    """ This chain is for customer support.
     The first LLM response is our typical sarcatic LLM tone
     We want customer support chats to take a more professional and kind tone """

    # First LLM, just get a basic chain from above
    first_chain = get_basic_chain()

    # Define a new prompt for the second LLM call
    second_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and kind customer support chatbot. "
                   "You respond to hypothetical customer support chats. "
                   "Take the initial response from the first LLM and rewrite it. "
                   "Change sarcastic tone of the first response into a more kind response. "
                   "ONLY return the rewritten response, imagine this is a chat to a real customer. "
                   "Don't include any preamble text, ONLY the response to the user. "
                   "You don't need to comfort the user, just tell them a solution. "),
        ("user", "Initial LLM response: {input}")
    ])

    # Second chain, same model, different prompt
    second_chain = second_prompt | llm

    # Finally, build a sequential chain (take first LLM output and feed it to the second LLM)
    final_chain = first_chain | second_chain
    # (prompt | llm | second_prompt | llm)

    return final_chain

# TRANSFORM CHAIN EXAMPLE - returning a predetermined response using vanilla Python code
def get_transform_chain():

    # This chain will ONLY return the text "I cannot help you with that."
    # If the user says something about wanting to touch grass and stop playing games

    trigger_phrases = ["touch grass", "stop playing", "go outside", "get a life", "job"]

    # This is a legacy chain, and I'm going to build it in the old fashioned way
    # The old fashioned way still works, but LCEL is the new and recommended chain syntax
    transform_chain = TransformChain(
        input_variables=["input"],
        output_variables=["output"],
        transform=lambda inputs: {
            "output": (
                "I cannot help you with that... Buy more games"
                if isinstance(inputs["input"], str)
                   and any(keyword in inputs["input"].lower() for keyword in trigger_phrases)
                else "I can help you with that!"
                # We could actually invoke the LLM in the else, but I won't.
            )})

    # ignore the "Unexpected Argument" in the "transform" field. It works.

    return transform_chain

# CHAIN WITH MEMORY
def get_memory_chain():

    # First, we'll set up the memory object to store convo history
    # CBWM remembers the last "k" interactions
    # memory = ConversationBufferWindowMemory(k=3)

    # Let's try using Summary instead - remember the whole convo, but less detail
    memory = ConversationSummaryMemory(llm=llm)

    # Prompt, mostly the same but one small addition - {history} variable
    # These older chains don't use LCEL and have opinionated variable names
    memory_prompt = ChatPromptTemplate.from_messages([
        ("system",
          """
          You are a helpful, snarky, and nerdy chat bot that answers questions about video games.
          Imagine you're like a clerk at a video game store, and you're a know-it-all.
          
          You give brief but informative answers, and you are very opinionated.
          You love to give recommendations and refer to critic reviews when answering questions.
          
          You only answer questions about games or gaming culture.
          You don't provide further suggestions beyond what the user asks for.
          """),
        ("user",
        """
            Conversation History: {history}
            Current User Input: {input}
        """)
    ])

    # Make the chain! Old fashioned syntax, we will get deprecation warnings when we run
    memory_chain = ConversationChain(
        llm = llm,
        prompt = memory_prompt,
        memory = memory
    )

    return memory_chain