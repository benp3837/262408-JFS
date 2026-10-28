from fastapi import APIRouter
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

from app.services.langchain_service import get_basic_chain, get_sequential_chain, get_transform_chain, get_memory_chain

# Router setup
router = APIRouter(
    prefix="/langchain", # Prefix defines which HTTP URLs hit our router
    tags=["langchain"] # These endpoints will be under the "langchain" tag in the SwaggerUI
)

# Quick Pydantic model for the user's query to our LLM
# This helps it play nice with FastAPI (user query goes in the body, not query params)
class ChatRequest(BaseModel):
    input: str

# Import the different chains we'll invoke in our routes
basic_chain = get_basic_chain()
sequential_chain = get_sequential_chain()
transform_chain = get_transform_chain()
memory_chain = get_memory_chain()

# General chat endpoint - no memory or fancy features
@router.post("/chat")
async def general_chat(chat:ChatRequest):

    # Invoke the chain, returning the response
    return basic_chain.invoke(input=chat.input)

# DOCUMENT LOADER - loading in a .txt file to summarize
@router.get("/summarize")
async def summarize():

    # Use a LangChain Document Loader called TextLoader
    loader = TextLoader("app/StarWarsWriteup.txt")

    # Extract the text (comes back as a List of LangChain Document objects)
    document = loader.load()
    text = document[0].page_content # Get the text content as a python String

    # Our first look at RAG -
    # the data we got from the .txt file will help the LLM generate its response
    # Invoke the same basic chain, this time the query will go straight into it
    return basic_chain.invoke(input={f"Summarize this text: {text}"})

# ANOTHER DOCUMENT LOADER
@router.post("/csv-analysis")
async def csv_analysis(chat:ChatRequest):

    # This time, we'll load in a CSV and let the user ask questions about it

    # Load in the CSV file and extract it
    loader = CSVLoader("app/video_games.csv")
    data = loader.load()

    # Convert the CSV content into a single string
    csv_content = "\n".join(row.page_content for row in data)

    # Invoke the LLM!
    return basic_chain.invoke(input = {
        f"""Answer the user's query with the provided video game data.
        ONLY use the provided data to answer the question

        User Query: {chat.input}
        CSV Data: {csv_content}
        """
    })


# INVOKING OUR SEQUENTIAL CHAIN
@router.post("/support-chat")
async def support_chat(chat:ChatRequest):

    # Almost identical to the first chat endpoint. Just a different chain.
    return sequential_chain.invoke(input=chat.input)

# INVOKING OUR TRANSFORM CHAIN
@router.post("/transform-chat")
async def transform_chat(chat:ChatRequest):
    return transform_chain.invoke(input=chat.input)

# OUTPUT PARSING EXAMPLE (Pydantic Objects)

# First, define 2 Pydantic models to help us format our output

class VideoGame(BaseModel):
    title: str
    genre:str
    rating: float

class VideoGameList(BaseModel):
    games: list[VideoGame]

@router.get("/game-recs")
# Returns 3 game recs by default
async def get_game_recs(amount:int = 3, genre:str = "any"):

    # Use PydanticOutputParser to format LLM out into the VideoGameList model
    parser = PydanticOutputParser(pydantic_object=VideoGameList)

    # Testing this out - looks like parsers have built in LLM format instructions
    instructions = parser.get_format_instructions()

    # Invoke the chain, asking for game recs in a specific format
    output = basic_chain.invoke(input = {
        f"""
        Recommend {amount} video games to me in {genre} genre. 
        ONLY return the required JSON object. 
        Format your response according to these instructions:
        
        {instructions}
        """
    })

    # Here's the actual parsing into Pydantic
    parsed_output = parser.parse(output.content)
    return parsed_output

# USING THE MEMORY CHAIN
@router.post("/memory-chat")
async def memory_chat(chat:ChatRequest):
    return memory_chain.invoke(input=chat.input)