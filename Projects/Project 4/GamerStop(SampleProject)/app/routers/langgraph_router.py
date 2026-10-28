from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agentic_langgraph_service import agentic_graph
from app.services.langgraph_service import graph

router = APIRouter(
    prefix="/langgraph",
    tags=["langgraph"]
)

# Basic Pydantic Model to handle user input
class ChatRequest(BaseModel):
    input: str


# Notice how we just have a single endpoint for 3 potential outcomes
# LangGraph is inherently multi-modal.
# All that complicated Service logic cleans up our routers
@router.post("/langgraph")
async def langgraph_chat(chat:ChatRequest):

    # Get the result of the invocation
    result = graph.invoke({"query":chat.input},
                          config={
                              "configurable":{"thread_id":"demo_thread"}
                          })
    # NOTE^: We're just hardcoding thread_id here... we don't have login functionality
    # Normally, the user would log in, their ID would get saved somewhere (session?)
        # Then that logged-in ID would be used to indicate the appropriate thread

    # Return the result and the route (just to see it)
    return {
        "response": result.get("answer"),
        "route": result.get("route"),
        "message_memory": result.get("message_memory")
    }


# New route for our agentic LangGraph, just to separate them
# Pretty much the same as above, but we left out memory and we use the agentic graph
@router.post("/agentic-langgraph")
async def agentic_langgraph_chat(chat:ChatRequest):

    result = agentic_graph.invoke({"query":chat.input})

    return {
        "response": result.get("answer")
    }