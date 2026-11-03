from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.langchain_service import get_general_chain
from app.services.vectordb_service import ingest_json, search_collection

# Set up the router (we do this in every router)
router = APIRouter(
    prefix="/vectordb",
    tags=["vectordb"]
)

# Pydantic Model for ingesting JSON
class IngestJSON(BaseModel):
    id:str
    text:str
    metadata:Any # Lazy, didn't wanna make a whole new object

# TODO: Pydantic Model for ingesting text

# Import our basic chain for LLM operations
chain = get_general_chain()


# Ingest JSON endpoint
@router.post("/submit_json")
async def submit_json(items:list[IngestJSON]):

    # Call the service method that ingests JSON
    # Save the result so we have the count of ingestions
    ingested_items = ingest_json(
        collection_name="monster_fighting_tools",
        items=[item.dict() for item in items]
        #items=[item.model_dump() for item in items]
    )

    return {"ingested_items": ingested_items}


# Similarity search endpoint for MONSTER FIGHTING TOOLS
# (NOT RAG yet)
@router.get("/search_monster_tools")
async def search_tools(query:str):


    # Call the Service method to search the collection
    results = search_collection(
        collection_name="monster_fighting_tools",
        query=query
        # We COULD set the k value here, or just let default to 5
    )

    return results

# RAG endpoint for MONSTER FIGHTING TOOLS




