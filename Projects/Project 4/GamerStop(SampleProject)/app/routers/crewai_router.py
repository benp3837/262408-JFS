from fastapi import APIRouter
from pydantic import BaseModel

from app.services.crewai_service import build_crew

router=APIRouter(
    prefix="/crew",
    tags=["crew"]
)

class ChatRequest(BaseModel):
    input: str

# Just one endpoint to send queries to our CrewAI agentic workflow
@router.post("/crewai")
async def crew_chat(query:ChatRequest):
    # get the crew by invoking build_crew
    crew = build_crew(query.input)
    # invoke the crew with the kickoff() function
    result = crew.kickoff()

    # TODO: cleaner response than just the raw result
    return result