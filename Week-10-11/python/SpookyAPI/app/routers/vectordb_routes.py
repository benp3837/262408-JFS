# TODO: ben - you need to register this in app.py
from fastapi import APIRouter
from pydantic.v1 import BaseModel

from app.services.langchain_service import get_general_chain

# Set up the router (we do this in every router)
router = APIRouter(
    prefix="/vectordb",
    tags=["vectordb"]
)

# Pydantic Model for ingesting JSON
class IngestJSON(BaseModel):
    text:str

# TODO: Pydantic Model for ingesting text

# Import our basic chain for LLM operations
chain = get_general_chain()


# Ingest JSON endpoint



# Similarity search endpoint for MONSTER FIGHTING TOOLS




