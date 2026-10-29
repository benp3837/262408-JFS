# FastAPI Routers share a use case with Spring Controllers
# They take in HTTP requests, and return HTTP responses
from fastapi import APIRouter
from pydantic import SecretStr

from models.monster_model import MonsterModel
from services.langchain_service import get_general_chain

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


# 2 routes that talk to the LLM via LangChain service --------

@router.get("/chat")
async def general_chat(input:str):

    # Get the chain
    chain = get_general_chain()

    # Return the invocation of the string
    return chain.invoke({"input":input})

# TODO: How can we get the LLM to answer questions based on the monster data?
# This is the concept of RAG which you'll need for your project