from pinecone import Pinecone, ServerlessSpec
import os

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

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

def upsert_email_embedding(email_id, embedding, metadata):
    index.upsert([
        (email_id, embedding, metadata)
    ])

def query_similar_emails(embedding, top_k=1):
    result = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    return result
