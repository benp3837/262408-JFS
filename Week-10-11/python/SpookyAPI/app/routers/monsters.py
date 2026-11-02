# FastAPI Routers share a use case with Spring Controllers
# They take in HTTP requests, and return HTTP responses
from fastapi import APIRouter
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import SecretStr, BaseModel

from app.models.monster_model import MonsterModel
from app.services.langchain_service import get_general_chain, get_memory_chain

# Every router gets set up like this:
router = APIRouter(
    prefix="/monsters", # HTTP requests to /monsters will route here
    tags=["monsters"] # This is for the Swagger UI docs
)

monster_db = [
    MonsterModel(id=1, name="Babadook", motive=SecretStr("Fear")),
    MonsterModel(id=2, name="Cookie Monster", motive=SecretStr("Cookies")),
    MonsterModel(id=3, name="Minotaur", motive=SecretStr("Labyrinth")),
    MonsterModel(id=4, name="The Kraken", motive=SecretStr("Destruction")),
    MonsterModel(id=5, name="Cthulhuwu", motive=SecretStr("Madness"))
]

# 2 routes - one to get all monsters, one to insert monster

@router.get("/", status_code=200)
async def get_monsters():
    return monster_db

@router.post("/", status_code=201)
async def insert_monster(monster:MonsterModel):

    # TODO: error handling

    monster_db.append(monster)

    return {"output": monster}

# -------------------------------------------------------------------------------

# ChatInputModel - used in our LLM functions to pass the user's query in the body
class ChatInputModel(BaseModel):
    input:str

# Declare the general chain up here so we don't have to rewrite it
chain = get_general_chain()

# Now for routes that talk to the LLM via LangChain service --------

# Basic chat endpoint
@router.post("/chat")
async def general_chat(chat:ChatInputModel):

    # Return the invocation of the string
    return chain.invoke({"input":chat.input})

# How can we get the LLM to answer questions based on the monster data?
# This is our first look at RAG which you'll need for your project
@router.post("/rag_chat")
async def rag_chat(chat:ChatInputModel):

    # This time, lets add the monster data plus some extra prompting
    # Remember this is called a PROMPT TEMPLATE
        # A prompt that takes in {variables} for dynamic behavior
    return chain.invoke({
        "input": f"""
            Given this data on Monsters in the database, answer the user's question. 
            If the monster is NOT in the DB, then you don't know. 
            
            BUT, if the user is asking for info RELATED to the monsters, 
            you can pull from training data.
            
            The data: {monster_db}
            
            The User's query: {chat.input}
        """
    })

# Document Loader - text
@router.post("/txt_chat")
async def evil_rambling_chat(chat:ChatInputModel):

    # Loading in txt and other formats is easy - use Langchain's ___Loader Classes
    loader = TextLoader("app/files_to_load/evil_rambling.txt", encoding="utf-8")

    # Store the txt in a list of langchain Document object
    stored_text = loader.load()

    # Extract the text from the list
    extracted_text = stored_text[0].page_content

    # Invoke the LLM with the user's query and the extracted data
    return chain.invoke({
        "input":f"""
            Based on the ingest txt file, answer the user's question.
            Do NOT refer to the user in your answer. Respond in first person.
            
            The txt file: {extracted_text}
            
            The user's query: {chat.input}
        """
    })


# Document Loader - csv (mostly the same as txt, just some different objects/strats)
@router.post("/csv_chat")
async def monster_status_chat(chat:ChatInputModel):

    # Load in the csv, and extract it
    loader = CSVLoader("app/files_to_load/monster_statuses.csv")

    stored_csv = loader.load()

    # Extraction is slightly different - load all records into a single string
    extracted_data = "\n".join(doc.page_content for doc in stored_csv)

    print(extracted_data)

    # Invoke the LLM!
    return chain.invoke({
        "input":f"""
        
        Based on the provided CSV data, answer the user's questions. Be analytical.
        If the user isn't asking for analysis or overviews, ONLY say "Ask about analysis".
        
        The CSV: {extracted_data}
        
        The user's query: {chat.input}
        """
    })


# Output Parser - Pydantic

# Need a Monster Model with the motive as a regular str,
# cuz secretstr broke/confused our weak LLM
class MonsterModelRaw(BaseModel):
    id: int = 0
    name: str
    motive: str

# Output parsers take the LLM's response and turn them into a specific format
# TODO: this isn't working, I'll get it to work or switch to a list etc.
@router.get("/monster_rec")
async def get_monster_recommendation(characteristic:str):

    # Langchain's built-in PydanticParser to parse output into Pydantic
    parser = PydanticOutputParser(pydantic_object=MonsterModelRaw)

    # Testing out what the parser looks like - what it tells the LLM
    instructions = parser.get_format_instructions()
    print(instructions)

    # First, store the output of the LLM (we parse it after)
    output = chain.invoke({
        "input":f"""
            Make me a monster with this characteristic: {characteristic}
            
            Return ONLY a JSON object like this example:
            {{"id": 1, "name": "Bonecrawler", "motive": "seeks warmth"}}
        
            Use those exact field names. No extra text, no schema, just the object.
            
            Format your response according to these instructions:
            {instructions}
        """
    })

    print(output.content)

    # TODO: add it to the DB cleanly
    monster_db.append(output.content)

    # Here's the actual parsing into Pydantic:
    return parser.parse(output.content)

# Chat function with a memory chain - first we need to get the memory chain from service
memory_chain = get_memory_chain()

@router.post("/memory_chat")
async def chat_with_memory(chat:ChatInputModel):
    # One liner just like the general chain chat
    return memory_chain.invoke(input=chat.input)