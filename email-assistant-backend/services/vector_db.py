from pinecone import Pinecone, ServerlessSpec
import os
from typing import List, Dict
from utils.env import get_env_var 

# Initialize Pinecone client
pc = Pinecone(api_key=get_env_var("PINECONE_API_KEY"))

index_name = "email-assistant"

# Create index if not exists
if index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

# Connect to index
index = pc.Index(index_name)

def upsert_email_embedding(email_id: str, embedding: list, metadata: dict):
    # Add raw email body to metadata before upserting
    vector = {
        "id": email_id,
        "values": embedding,
        "metadata": metadata  # should include sender_name, sender_email, subject, body (full text!)
    }
    index.upsert(vectors=[vector])

def query_similar_emails(embedding, source="sent", top_k=5):
    result = index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True,
        filter={"source": source}
    )
    return result

def query_email_embeddings(embedding: List[float], top_k: int = 5, filter: Dict = None):
    query_params = {
        "vector": embedding,
        "top_k": top_k,
        "include_values": False,
        "include_metadata": True
    }

    if filter:
        query_params["filter"] = filter

    response = index.query(**query_params)

    if not response.matches:
        return {"matches": []}

    return response.to_dict()
