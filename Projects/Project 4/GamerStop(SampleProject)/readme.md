# Sample AI-Powered Python Project (GamerStop)

This is a sample AI-powered Python project from a prior cohort that demonstrates various final-qc topics, including FastAPI, LangChain, AWS Bedrock, and more. It's a little messy, but it's full of project-based examples - it's a FastAPI app, powered by LangChain and VectorDB for chat and RAG functionality.

---

## Getting Started

### Prerequisites

- Python and Ollama
    - https://docs.google.com/document/d/1-qTezE8u9i54AKsts14TITfgQ1IDIfRh5aG3hJW3FxQ/edit?usp=sharing
- pip (Python package manager)
- A Python virtual environment tool (I use venv)

### Installation

1. Clone the repository to your local machine, and open it up in Intellij (or whatever IDE)

2. Create and activate a virtual environment (Using venv):

   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required dependencies in the requirements.txt file:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the FastAPI application using Uvicorn:
```bash
uvicorn app.main:app --reload
```

Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the Swagger UI for testing the API just like you would in Postman.

---

## Starting before the demos?

If you're new to FastAPI or AI-powered projects, I recommend starting by learning FastAPI and creating a non-AI Python CRUD API. You can find my setup notes at the top of the .md file for FastAPI in week 10. 

This will help you get familiar with handling HTTP requests and responses, similar to what you may have done with Spring MVC.

THEN you can start looking at LangChain, which will feel very familiar to Spring AI.