from fastapi import FastAPI

from app.routers import langchain_router, vectordb_router, langgraph_router, bedrock_router, crewai_router

# Set up our FastAPI instance
app = FastAPI()

# Register routers
app.include_router(langchain_router.router)
app.include_router(vectordb_router.router)
app.include_router(langgraph_router.router)
app.include_router(bedrock_router.router)
app.include_router(crewai_router.router)

