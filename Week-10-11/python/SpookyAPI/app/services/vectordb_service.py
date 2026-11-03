from typing import Any

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

# This Service is full of functions that let our VectorDB work
# Creating/Getting Collections, ingesting data, and searching that data

# Where the VectorDB lives
PERSISTY_DIRECTORY = "app/chroma_db"

# The model we pulled - we'll use this to make our embeddings
EMBEDDING_MODEL = OllamaEmbeddings(model="nomic-embed-text")

# The ChromaDB vector store itself (this contains our collections)
vector_store: dict[str, Chroma] = {}

# Create a new Collection (remember a Collection is a group of related embeddings)
# If the Collection exists already, just return it
def create_or_get_collection(collection_name:str):

    # If the Collection doesn't already exist, make a new one
    if collection_name not in vector_store:
        vector_store[collection_name] = Chroma(
            persist_directory=PERSISTY_DIRECTORY,
            collection_name=collection_name,
            embedding_function=EMBEDDING_MODEL
        )

    # Return the new (or existing) Collection
    return vector_store[collection_name]


# Ingest JSON data into a Collection
def ingest_json(collection_name:str, items:list[dict[str, Any]]):

    # Get an instance of the Collection in the vector store
    collection = create_or_get_collection(collection_name)

    # Turn the inputted list into a list of langchain Document objects
    docs = [
        Document(page_content=item["text"], metadata=item.get("metadata", {}))
                 for item in items
    ]

    print(items)

    # Attach IDs to each Document (easy since the JSON has an "id" field)
    ids = [item["id"] for item in items]

    # Finally add the Documents to the Collection!!
    embedded_docs = collection.add_documents(documents=docs, ids=ids)

    # Just wanna see
    print(embedded_docs)

    # Return the amount of ingested items just for visibility
    return len(embedded_docs)


# TODO: Ingest text data into a Collection




# Here's the function that actually searches a Collection
def search_collection(collection_name:str, query:str, k:int=5):

    # Get collection
    collection = create_or_get_collection(collection_name)

    # Perform the similarity search
    # This is a RETRIEVER, we're using it to RETRIEVE data for an LLM response
    results = collection.similarity_search_with_score(query, k)

    return results
