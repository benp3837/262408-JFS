from fastapi import FastAPI

from routers import monsters

# Set up FastAPI. We'll use this "app" variable to do FastAPI stuff below
app = FastAPI()


# TODO: Global exception handling with @app.exception_handler


# import/activate the routers here
app.include_router(monsters.router)


# Generic sample endpoint (GET request with a greeting)
@app.get("/")
async def sample_endpoint():
    return {"greeting":"Hello from FastAPI! This is our project backend library"}