# FastAPI Routers share a use case with Spring Controllers
# They take in HTTP requests, and return HTTP responses
from fastapi import APIRouter

# Every router gets set up like this:
router = APIRouter(
    prefix="/monsters", # HTTP requests to /monsters will route here
    tags=["monsters"] # This is for the Swagger UI docs
)

monster_db = ["Babadook", "Cookie Monster", "Minotaur", "Kraken", "Cthulhu"]

# 2 routes - one to get all monsters, one to insert monster

@router.get("/", status_code=200)
async def get_monsters():
    return monster_db

@router.post("/", status_code=201)
async def insert_monster(monster_name: str):
    # TODO: error handling

    monster_db.append(monster_name)

    return {"message": f"Monster '{monster_name}' added successfully!"}