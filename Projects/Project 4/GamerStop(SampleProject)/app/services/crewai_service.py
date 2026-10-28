import boto3
from crewai import Agent, Crew, Task, LLM
from crewai.tools import tool

from app.services.vectordb_service import search_collection


# CrewAI - A framework that lets us define "crews" of Agents
# These Agents work together to accomplish complex multi-step processes.

# Defined in this service:
    # Tools - functions an Agent can use
    # Agents - the entities that performs Tasks
    # Tasks - specific processes assigned to an Agent
    # Crew - the group of Agents we invoke to accomplish a goal

# =========== Defining our Misc. Helper tool ==============

# An instance of our Bedrock client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Define a CrewAI LLM object using our Bedrock nova model
llm = LLM(
    model="amazon.nova-micro-v1:0",
    region_name="us-east-1",
)

# =========== Defining Tools the Agents can use ===========

# A tool that does a similarity search on the video_games VectorDB collection
@tool("search_games")
def search_games_tool():
    """This tool performs a similarity search on the video_games VectorDB collection.
    This is primarily for video game recommendations and suggestions.
    The result of this tool is a list of relevant video games for RAG functionality"""
    # results = search_collection(collection_name="video_games", query=query, k=5)
    # return str(results) # I want it as a String for ease of use

    # TEMP: Just returning a string for now cuz Chroma machine broke!!
    return """
        Bioshock Finite: A first-person shooter with a gripping story and unique setting.
        Working with Dad Simulator: Hold a flashlight while getting yelled at. You can't win.
        Ultra Worm: A fun and chaotic multiplayer game where you play as a worm battling with friends.
        Call of Duty Shoot a Man: War is fun! First person, action packed, and lots of shooting!
        Super Backpack Bros: Explore the forest in this open world game... Don't stay out at night.
        """

# A tool that uses the similarity search data to generate a game recommendation
@tool("generate_recommendation")
def generate_recommendation_tool(game_info:str):
    """
    This tool takes in raw game info from the search_games tool.
    It then generates a conversational response that recommends a game or two to the user.
    """
    prompt = (f"You are a helpful assistant that takes raw game data, "
              f"and responds to the user with a paragraph recommending a game or two. "
              f"Here's the game data: {game_info}")

    # Bedrock invocation - different from LangChain but still just an LLM invocation
    response = client.converse(
        modelId="amazon.nova-micro-v1:0",
        messages=[{
            "role":"user",
            "content":[{"text": prompt}]
        }]
    )

    return response


# ============ Defining Agents to perform specialized tasks ==========

# Agent 1 - The Researcher - gathers data from VectorDB
researcher = Agent(
    role="Game Research Specialist",
    goal="Based on the user's query, find relevant game info from VectorDB. "
         "Use only the search_games tool to do your research. "
         "Use NO other training data or external sources to find video games."
         "You don't add any extra text to your response - just the games and their info.",
    backstory="You are a gaming expert that specializes in data gathering. ",
    tools=[search_games_tool],
    max_iter=1, # Only runs once
    llm=llm, # The CrewAI LLM object we defined above
    verbose=True
)

# Agent 2 - The Analyst - takes raw data from Researcher and builds a response
analyst = Agent(
    role="Game Recommendation Specialist",
    goal="Take the raw game data from the Researcher and generate a conversational recommendation for the user. "
         "Use only the generate_recommendation tool to create your response. "
         "You don't add any extra text to your response - just the recommendation.",
    backstory="You are a gaming expert that specializes in making recommendations based on data.",
    tools=[generate_recommendation_tool],
    max_iter=1, # Only runs once
    llm=llm,
    verbose=True
)


# ============ A function that defines Task order, and builds the Crew =======

def build_crew(query:str) -> Crew:

    # Task for Agent 1 (Research)
    research_task = Task(
        description=f"""Search the video_games VectorDB Collection for information 
        relevant to this User request: '{query}'. 
        Only use the tools you have access to, and return all relevant information you find.
        ONLY return the games and their descriptions - no preceding or concluding text""",
        expected_output="A String bulleted-list of info from the video_games collection.",
        agent=researcher
    )

    # Task for Agent 2 (Analysis)
    analysis_task = Task(
        description=f"""Take the raw game data from the Researcher, 
        and generate a conversational recommendation for the user. 
        Use only the tools you have access to in order to draft your response. 
        and generate a response recommending a game or two to the user.
        The User asked: {query}""",
        expected_output="A String paragraph recommendation for the user.",
        agent=analyst,
        context=[research_task]
    )

    # Build and Return the Crew!
    return Crew(
        agents=[researcher, analyst],
        tasks=[research_task, analysis_task],
        verbose=True # Prints lots of helpful info in the console during runtime
    )