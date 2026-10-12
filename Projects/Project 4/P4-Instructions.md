# Project Specification: Documentation Digester

## 1. Overview
Welcome to **Documentation Digester**! You have reached the final frontier of the curriculum. 

In the previous projects, you built engines and dashboards. Now, you are going to build a **Semantic Search Engine**. Your mission is to ingest the massive, complex official documentation of the Godot Game Engine and transform it into a high-precision retrieval system.

This isn's a standard "keyword search." You are building a system that understands **meaning**. When a user asks a question in plain English, your engine should be able to find the exact paragraph in the documentation that contains the answer, even if the exact words don't match.

## 2. Your Mission (The Semantic Pipeline)
Your team is responsible for building a specialized data pipeline that follows a "Source-to-Search" workflow.

### Phase 1: The Digester (ETL Pipeline)
You must build a pipeline that turns raw source code into searchable "intelligence."
* **Build from Source:** Instead of scraping the web, you will clone the official Godot documentation repository and use **Sphinx** to build it into structured files.
* **Data Cleaning:** Raw documentation is "noisy." You must write logic to strip out navigation menus, footers, and HTML boilerplate so that only the high-value content is indexed.
* **Semantic Chunking:** You cannot just split text by character count. You must implement "smart chunking" (e.g., splitting by headers or logical sections) so that every piece of data maintains its context.
* **Vectorization:** You will use local embedding models to turn these text chunks into mathematical vectors and store them in a **Vector Database**.

### Phase 2: The Searcher (The API)
Once the data is indexed, you will build the interface that allows users to query it.
* **Natural Language Querying:** A user should be able to ask a question like, *"How do I use signals to communicate between nodes?"*
* **Top-K Retrieval:** Your system must return the most semantically relevant documentation chunks.
* **Provenance (The "Why"):** It isn't enough to just give the text. Your API must return the "Source of Truth"—the exact section title, URL, or file path where the information was found.
* **FastAPI Interface:** All of this must be wrapped in a high-performance, asynchronous API.

## 3. Technical Architecture
To succeed, you must master the flow of data through these four stages:

1.  **The Build Stage:** `Godot Docs Repo` $\rightarrow$ `Sphinx Build` $\rightarrow$ `Structured Files`.
2.  **The ETL Stage:** `Structured Files` $\rightarrow$ **`Data Cleaning`** $\rightarrow$ `Semantic Chunking` $\rightarrow$ `Embedding Model`.
3.  **The Storage Stage:** `Embeddings` $\rightarrow$ `Vector Database`.
4.  **The Search Stage:** `User Question` $\rightarrow$ `Embedding` $\rightarrow$ `Similarity Search` $\rightarrow$ `Ranked Chunks + Metadata`.

### The Tech Stack
* **Orchestration:** **LangChain** (to manage your retrieval chains).
* **API Framework:** **FastAPI** (to serve your search engine).
* **Language:** **Python** (the industry standard for AI/ML).
* **Vector Database:** **Chroma** or **FAISS**.
* **Embeddings:** **Sentence-Transformers** (running locally on your machine).
* **Build Tool:** **Sphinx** (to generate the docs from source).

## 4. Quality Standards (The "Retrieval" Metric)
Since you aren't using an LLM to "chat," your success is measured by **Search Precision**:
* **Semantic Precision:** Does the system actually find the right information for the question?
* **Chunk Integrity:** Are the chunks useful, or are they too small/fragmented to make sense?
* **Provenance Accuracy:** Does the system correctly cite the exact source for every result?
* **Latency:** How fast can your engine go from "Question" to "Result"?

## 5. Roadmap
*Note: the weeks referenced are training weeks*

* **Week 11: The Digester (ETL).** Focus on the "hard engineering": cloning the repo, building with Sphinx, cleaning the data, and building your vector index.
* **Week 12: The Searcher (API).** Focus on the "search intelligence": building the FastAPI interface, refining your retrieval logic, and perfecting your metadata reporting.

**Good luck—it's time to make the documentation searchable!**
