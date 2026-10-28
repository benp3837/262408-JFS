from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.langchain_service import get_basic_chain
from app.services.vectordb_service import ingest_json, search_collection, ingest_text, extract_entities

router = APIRouter(
    prefix="/vectordb",
    tags=["vectordb"]
)

# Pydantic Model for ingesting JSON items
class IngestItem(BaseModel):
    id: str
    text: str

# One more Pydantic Model for ingest text
class IngestText(BaseModel):
    document:str
    game_title:str

# Import our basic chain here
basic_chain = get_basic_chain()

# Ingest JSON endpoint
@router.post("/ingest-json")
async def ingest_json_items(items:list[IngestItem]):

    # Call the service method that ingests JSON
    ingested_items = ingest_json(
        collection_name="video_games",
        items=[item.model_dump() for item in items]
    )

    return {"ingested_items": ingested_items}

# Ingest Text endpoint
@router.post("/ingest-text")
async def ingest_text_items(text:IngestText):

    # Call the service method to ingest text
    # NOTE: we're create a new collection here called critic_reviews
    ingested_items = ingest_text(
        collection_name="critic_reviews",
        text=text.document,
        game_title=text.game_title
    )

    return {"ingested_items": ingested_items}


# Similarity search for video games
# (not RAG, just getting similarity search results directly)
@router.post("/search-games")
async def search_games(query:str, k:int=5):

    # Call search collection from the service and return it
    results = search_collection(
        collection_name="video_games",
        query=query,
        k=k
    )

    return results

# Similarity search for critic reviews
@router.post("/search-reviews")
async def search_reviews(query:str, k:int=5):

    # Call search collection from the service, this time for the critic_reviews collection
    results = search_collection(
        collection_name="critic_reviews",
        query=query,
        k=k
    )

    return results


# RAG ENDPOINT - get the JSON search results (video_games collection)
# And Augment the LLM's Generated response based on the Retrieved data
@router.get("/games-rag")
async def games_rag(query:str):

    # Get the search results from the vector DB
    results = search_collection(query=query, k=5, collection_name="video_games")

    return basic_chain.invoke(
        input=f"Respond to the User's Query based on the following Search Results. "
              f"ONLY use the information in the Search Results. "
              f"Don't fall back to any outside information, say you don't know if you have to."
                f"User's Query: {query}"
                f"Search Results: {results}")

# RAG ENDPOINT - same as above, but for critic reviews
@router.get("/reviews-rag")
async def reviews_rag(query:str):

    # Get the search results from the vector DB
    results = search_collection(query=query, k=9, collection_name="critic_reviews")

    return basic_chain.invoke(
        input=f"Respond to the User's Query based on the following Search Results. "
              f"ONLY use the information in the Search Results. "
              f"Don't fall back to any outside information, say you don't know if you have to."
              f"User's Query: {query}"
              f"Search Results: {results}")

# RAG ENDPOINT WITH FILTER - same as above, but takes a game title to filter results
@router.get("/reviews-rag-filtered")
async def reviews_rag_filtered(query:str, game_title:str):

    # Get the search results from the vector DB
    results = search_collection(query=query, k=3, collection_name="critic_reviews", game_title=game_title)

    return basic_chain.invoke(
        input=f"Respond to the User's Query based on the following Search Results. "
              f"ONLY use the information in the Search Results. "
              f"Don't fall back to any outside information, say you don't know if you have to."
              f"User's Query: {query}"
              f"Search Results: {results}")

# Endpoint that uses NER to extract entities from some text
@router.post("/extract-entities")
async def respond_with_entities(query:str, text:str):

    # Call the service method that uses NER for extraction
    entities = extract_entities(text)

    # Temporary - just wanna see the data
    # return {"entities": entities}

    # Let's do some RAG, the LLM will take a query
    # And answer it based on the NER entities that were extracted
    return basic_chain.invoke(
        input=f"Answer the User's Query based on the following extracted entities. "
              f"ONLY use the provided information. "
              f"Don't fall back to any outside information, try your best! "
              f"User's Query: {query}"
              f"Extracted Entities: {entities}")