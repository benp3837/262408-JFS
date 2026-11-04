from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.langchain_service import get_general_chain
from app.services.vectordb_service import ingest_json, search_collection, ingest_text

# Set up the router (we do this in every router)
router = APIRouter(
    prefix="/vectordb",
    tags=["vectordb"]
)

# Pydantic Model for ingesting Data
class IngestData(BaseModel):
    id:str
    text:str
    metadata:Any = None # Lazy, didn't wanna make a whole new object

# Import our basic chain for LLM operations
chain = get_general_chain()


# Ingest JSON endpoint
@router.post("/submit_json")
async def submit_json(items:list[IngestData]):

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
async def search_tools(query:str, k:int=5):


    # Call the Service method to search the collection
    results = search_collection(
        collection_name="monster_fighting_tools",
        query=query,
        # We COULD set the k value here, or just let default to 5
        k=k
    )

    return results

# RAG endpoint for MONSTER FIGHTING TOOLS
@router.get("/rag_monster_tools")
async def tools_rag(query:str):

    # First, get the search results from the collection
    results = search_collection(
        collection_name="monster_fighting_tools",
        query=query
        # We COULD set the k value here, or just let default to 5
    )

    # Here's the RAG part -
    # Augmenting the Generated response with the data we Retrieved
    return chain.invoke({
        "input": f"""
            Respond to the user's query by suggesting tools to fight monsters
            
            ONLY use info from the search results, 
            but you can be creative about how to use them.
            
            Don't fall back to outside info, and you can say you don't know.
            
            The User's Query: {query}
            
            The Search Results: {results}
            
        """
    })


# Text ingestion and querying ---------------------------------------

@router.post("/submit_text")
async def submit_text(text:IngestData):

    # Call the service method that ingests TEXT
    # Save the result so we have the count of ingestions
    ingested_items = ingest_text(
        collection_name="monster_incident_reports",
        text=text.text,
        source_id=text.id
    )

    return {"ingested_items": ingested_items}


# Just retrieve chunks, no RAG
@router.get("/search_incident_reports")
async def search_reports(query:str, k:int=5):

    # Call the Service method to search the collection
    results = search_collection(
        collection_name="monster_incident_reports",
        query=query,
        k=k
    )

    return results

# RAG for the incident reports
@router.get("/rag_incident_reports")
async def report_rag(query:str):

    # Search the appropriate collection
    results = search_collection(
        collection_name="monster_incident_reports",
        query=query
        # We COULD set the k value here, or just let default to 5
    )

    # Here's the RAG part -
    # Augmenting the Generated response with the data we Retrieved
    return chain.invoke({
        "input": f"""
            Respond to the user's query by telling them info based on incident reports
            
            ONLY use info from the search results, 
            but you can be creative about how to use them.
            Feel free to add some conjecture based on the data. Don't go crazy.
            
            Don't fall back to outside info, and you can say you don't know.
            
            The User's Query: {query}
            
            The Search Results: {results}
            
        """
    })
