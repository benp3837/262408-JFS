# very small corner-cutty router to show bedrock stuff
import boto3
from fastapi import APIRouter

from app.routers.langchain_router import ChatRequest
from app.services.langchain_service import get_basic_chain

router = APIRouter(
    prefix="/bedrock",
    tags=["bedrock"]
)

# Sanity test (just lists all the models to confirm we can access AWS)
@router.get("/list-models")
async def list_models():
    client = boto3.client("bedrock", region_name="us-east-1")
    return client.list_foundation_models()

# Now, let's actually use Bedrock for a basic chat endpoint

# Define the chat client (replaces the LLM object we've been using)
chat_client = boto3.client("bedrock-runtime", region_name="us-east-1")

@router.get("/chat")
async def bedrock_chat(query: str):
    response = chat_client.converse(
        modelId="amazon.nova-micro-v1:0",
        messages=[{
            "role":"user",
            "content":[{"text": query}]
        }]
    )

    return response

# NOTE: Bedrock is not meant to replace LangChain/Graph/Etc.
# it's a replacement for our MODEL. We can use Bedrock as the LLM (and other stuff)
# See langchain_service for the example of us doing this