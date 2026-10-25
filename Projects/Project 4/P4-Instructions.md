# Project Specification: Documentation Digester Chatbot

## 1. Overview
Welcome to **Documentation Digester**! You have reached the final frontier of the curriculum. 

In the previous projects, you built engines and dashboards. Now, you are going to build a **Full Stack Chatbot with Semantic Search Capabilities**. Your mission is to ingest the massive, complex official documentation of the Godot Game Engine and transform it into a high-precision retrieval system.

This isn's a standard "keyword search." You are building a system that understands **meaning**. When a user asks a question in plain English, your engine should be able to find the exact paragraph in the documentation that contains the answer, even if the exact words don't match.

## 2. Your Mission (The Semantic Pipeline)
Your team is responsible for building a specialized data pipeline that follows a "Source-to-Search" workflow.

### Phase 1: Data Ingestion
After choosing a theme for your chatbot, you must ingest some proprietary data that it can refer to.
* **Create your data:** Find and ingest data somehow! You can write (or generate) your own text files, scrape the web for documents or code, or use relational database data to gather the data accessible to your chatbot.
* **Data Cleaning:** Raw documentation is "noisy." You must write logic to strip out any irrelevant or meaningless information in generated responses. Your chatbot should never generate irrelevant or incorrect information!
* **Semantic Chunking:** You cannot just split text by character count. You must implement "smart chunking" (e.g., splitting by headers or logical sections) so that every piece of data maintains its context.
* **Vectorization:** You will use local embedding models to turn these text chunks into mathematical vectors and store them in a **Vector Database**. This is what will accomplish your semantic search capabilities.

### Phase 2: The Searcher (The API)
Once the data is vectorized, you will build the interface that allows users to query it.
* **Natural Language Querying:** A user should be able to ask a question like, *"How do I use signals to communicate between nodes?"*
* **Top-K Retrieval:** Your system must return the most semantically relevant documentation chunks.
* **Provenance (The "Why"):** It isn't enough to just give the text. Your API must return a conversational response that USES the semantically relevant chunks.
* **FastAPI Backend:** All of this must be wrapped in a high-performance, asynchronous API.
* **User Interface:** Use a frontend framework/library of your choice to connect to the FastAPI backend. Angular, React, Streamlit, plain HTML/CSS - all fair game.


### The Tech Stack
* **Orchestration:** **LangChain** (to manage your retrieval chains).
* **API Framework:** **FastAPI** (to serve your search engine).
* **UI Framework/Library:** **YOUR CHOICE** (to allow the user to send questions and recieve responses)
* **Language:** **Python** (the industry standard for AI/ML).
* **Vector Database:** **Chroma** or **FAISS**.
* **Embeddings:** **Sentence-Transformers** (running locally on your machine).


## 3. Quality Standards (The "Retrieval" Metric)
Your success is measured by your LLM's **Natural Responses and Search Precision**:
* **Natural Responses:** Does the system generate understandable and realistic responses?
* **Semantic Precision:** Does the system actually find the right information for the question?
* **Chunk Integrity:** Are the chunks useful, or are they too small/fragmented to make sense?
* **Latency:** How fast can your engine go from "Question" to "Result"? (Yes local models are inherently slow - will one teammate install a powerful model for the demo? Will you look into AWS Bedrock for incredibly low-latency response times?)

## 4. Roadmap
*Note: the weeks referenced are training weeks*

* **Week 11: The Digester (ETL).** Focus on the "hard engineering": creating data, writing data cleaning logic, building your vector index for RAG.
* **Week 12: The Searcher (API).** Focus on the "search intelligence": building the FastAPI interface, refining your retrieval logic, and building up the UI to communicate with it.

**Good luck - this is very cutting edge stuff! A great portfolio piece.**
