# Retrieval-Augmented Generation (RAG)

* Notes on VectorDB, which we'll use for RAG: https://docs.google.com/document/d/10iaJ2pxuAyUpap3q5zKx2WvSKXqK4tAp/edit?usp=sharing&ouid=116178657849214355990&rtpof=true&sd=true

## Table of Contents

* [1. High-Level Overview](#1-high-level-overview)
* [2. The RAG Architecture](#2-the-rag-architecture)
    * [2.1 The Core Problem: LLM Knowledge Limits](#21-the-core-problem-llm-knowledge-limits)
    * [2.2 How RAG Works: The Retrieval-Generation Loop](#22-how-rag-works-the-retrieval-generation-loop)
* [3. The Knowledge Foundation](#3-the-knowledge-foundation)
    * [3.1 Embeddings](#31-embeddings)
    * [3.2 Vector Databases](#32-vector-databases)
* [4. The Retrieval Process](#4-the-retrieval-process)
    * [4.1 Chunking Strategies](#41-chunking-strategies)
    * [4.2 Similarity Search](#42-similarity-search)
* [5. Advanced System Design](#5-advanced-system-design)
    * [5.1 Retriever Design](#51-retriever-design)

***

## 1. High-Level Overview

Large Language Models (LLMs) are incredibly capable, but they suffer from two fundamental limitations: **knowledge cutoff** (they only know what was in their training data) and **hallucination** (they may confidently state false information). 

**Retrieval-Augmented Generation (RAG)** is an architectural pattern that solves these problems by providing the LLM with access to external, real-time, or private data. Instead of relying solely on its internal weights, the model "looks up" relevant information from a provided context before generating a response.

[↑ Back to Table of Contents](#table-of-contents)

***

*Since LLMs are limited by their training data, we need a way to transform massive amounts of external information into a format the model can actually "search" through. This leads us to the core building blocks: Embeddings and Vector Databases.*

## 2. The RAG Architecture

### 2.1 The Core Problem: LLM Knowledge Limits

To understand why RAG is necessary, we must understand the constraints of a standard LLM.

| Constraint | Description | Impact on RAG |
| :--- | :--- | :--- |
| **Knowledge Cutoff** | LLMs are frozen in time at the moment their training ends. | RAG provides "fresh" information. |
| **Private Data Gap** | LLMs have no access to your internal company docs or emails. | RAG allows "grounding" in private data. |
| **Hallucination** | LLMs predict the next token, which can lead to plausible but false facts. | RAG provides "evidence" to reduce error. |

### 2.2 How RAG Works: The Retrieval-Generation Loop

RAG transforms the way a model processes a query. It moves from a direct **Query $\rightarrow$ Answer** flow to a multi-stage **Query $\rightarrow$ Retrieve $\rightarrow$ Augment $\rightarrow$ Answer** flow.

**The RAG Lifecycle:**
1.  **Ingestion:** External data is broken into pieces, converted into numbers, and stored in a database.
2.  **Retrieval:** When a user asks a question, the system finds the most relevant pieces of data.
3.  **Augmentation:** The retrieved data is "stuffed" into the prompt as context.
4.  **Generation:** The LLM reads the prompt + context and generates a grounded answer.

[↑ Back to Table of Contents](#table-of-contents)

***

*The magic of RAG lies in how we represent human language as data. This requires moving from text to mathematics through Embeddings and Vector Databases.*

## 3. The Knowledge Foundation

### 3.1 Embeddings

**Embeddings** are the mathematical representation of meaning. In RAG, we do not search for exact word matches; we search for **semantic similarity**.

An embedding model takes a piece of text (a word, a sentence, or a paragraph) and converts it into a long vector (a list of numbers). These numbers represent the "coordinates" of that text in a high-dimensional conceptual space.

**Key Concept: Semantic Proximity**
In an embedding space:
*   The vector for *"King"* will be physically close to the vector for *"Queen"*.
*   The vector for *"Apple"* (the fruit) will be far from *"Apple"* (the tech company) if the context distinguishes them.

> [!IMPORTANT]
> **Embeddings are not just keywords.** A search for "canine" will successfully retrieve a document about "dogs" because their embedding vectors are located in the same conceptual region, even though they share no characters.

### 3.2 Vector Databases

A **Vector Database** is a specialized storage system designed to hold and query these high-dimensional embeddings efficiently. Unlike traditional SQL databases that look for exact matches (e.g., `WHERE name = 'John'`), a vector database is optimized for **Approximate Nearest Neighbor (ANN)** searches.

| Feature | Traditional Database (SQL) | Vector Database |
| :--- | :--- | :--- |
| **Primary Data** | Structured (Rows/Columns) | Unstructured (Vectors/Embeddings) |
| **Search Type** | Exact Match / Keyword | Semantic / Similarity |
| **Query Example** | `SELECT * FROM docs WHERE text LIKE '%cat%'` | `FIND top_k neighbors of vector(query_text)` |
| **Examples** | PostgreSQL, MySQL | **Pinecone, Milvus, Weaviate, Chroma** |

[↑ Back to Table of Contents](#table-of-contents)

***

*Now that we have a place to store our vectors, how do we prepare the raw data for that storage? This requires efficient Chunking and intelligent Similarity Search.*

## 4. The Retrieval Process

### 4.1 Chunking Strategies

You cannot embed an entire 500-page textbook as a single vector; it would be too "blurry" and lose detail. Instead, we must break the text into **Chunks**.

**Chunking** is the process of dividing a large document into smaller, manageable pieces of text. The strategy you choose directly impacts the quality of your retrieval.

**Common Chunking Methods:**
*   **Fixed-Size Chunking:** Breaking text every $N$ characters or tokens.
    *   *Pros:* Simple, fast.
    *   *Cons:* Often cuts sentences or paragraphs in half, destroying context.
*   **Recursive Character Chunking:** Attempts to split text at natural boundaries (like `\n\n`, `\n`, or spaces) to keep related ideas together.
    *   *Pros:* Respects structure.
    *   *Cons:* Harder to tune.
*   **Semantic Chunking:** Using embeddings to detect when the topic changes and splitting there.
    *   *Pros:* Highest context preservation.
    *   *Cons:* Computationally expensive.

> [!TIP]
> **The "Overlap" Technique:** To prevent losing context at the edges of a chunk, we often use **Chunk Overlap**. If Chunk A ends at character 100, Chunk B might start at character 80. This "bridge" ensures that information split between chunks is still captured.

### 4.2 Similarity Search

**Similarity Search** is the mechanism used to find the "closest" chunks to a user's query. Once the user's question is converted into a vector, the database calculates the distance between that query vector and all stored document vectors.

**Common Distance Metrics:**
| Metric | Name | Best For... |
| :--- | :--- | :--- |
| **Cosine Similarity** | Measures the *angle* between vectors. | Most common in NLP; focuses on orientation rather than magnitude. |
| **Euclidean Distance (L2)** | Measures the straight-line distance between points. | Useful when the magnitude of the vector matters. |
| **Dot Product** | Measures both angle and magnitude. | Often used in high-performance, large-scale retrieval. |

[↑ Back to Table of Contents](#table-of-contents)

***

*Basic retrieval is a great start, but production-grade RAG systems require more sophisticated "intelligence" in how they select and rank information. This is where Retriever Design comes in.*

## 5. Advanced System Design

### 5.1 Retriever Design

A **Retriever** is the high-level component that orchestrates the entire search process. In simple RAG, the retriever is just a similarity search. In advanced RAG, the retriever is a sophisticated pipeline.

**Advanced Retrieval Patterns:**

1.  **Hybrid Search:** Combines **Semantic Search** (vector-based) with **Keyword Search** (BM25/traditional). This ensures you get the "feeling" of the query *and* the exact technical terms (like product serial numbers).
2.  **Multi-Query Retrieval:** Uses an LLM to take one user question and expand it into 3-5 different variations. This helps capture different facets of the same intent.
3.  **Re-Ranking (The Two-Stage Approach):**
    *   *Stage 1:* Use a fast, cheap vector search to retrieve 50 potential candidates.
    *   *Stage 2:* Use a much smarter, slower "Cross-Encoder" model to precisely rank those 50 candidates and pick the top 5.
4.  **Contextual Compression:** Instead of passing the whole chunk to the LLM, the retriever extracts only the specific sentences that are actually relevant to the query, saving precious tokens.

> [!IMPORTANT]
> **The Goal of Retriever Design:** The "Golden Rule" of RAG is that the LLM can only be as good as the context it is given. If the retriever provides garbage, the LLM will generate garbage (**GIGO: Garbage In, Garbage Out**).
