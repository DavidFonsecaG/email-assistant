from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from db.database import SessionLocal
from models.tables import EmailTable
from services.openai_client import generate_embedding
from services.outlook_fetch import fetch_recent_emails
from services.vector_db import upsert_email_embedding
from services.vector_db import query_similar_emails

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/sync-emails")
def sync_user_emails(token: str = Body(...), user_email: str = Body(...), db: Session = Depends(get_db)):
    messages = fetch_recent_emails(token)

    saved = 0
    for msg in messages:
        print(msg)
        # for key, value in msg.items():
        #     print(f"--> {key}: {value}")
        email_id = msg["id"]
        sender_info = msg.get("from", {}).get("emailAddress", {})
        sender_email = sender_info.get("address", "")
        sender_name = sender_info.get("name", "")
        subject = msg.get("subject", "")
        body = msg.get("body", {}).get("content", "")
        thread_id = msg.get("conversationId", "")
        timestamp_str = msg.get("receivedDateTime", "")
        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00")) if timestamp_str else None

        exists = db.query(EmailTable).filter(EmailTable.id == email_id).first()
        if exists:
            continue

        # Save to database
        db_email = EmailTable(
            id=email_id,
            user_email=user_email,
            sender_email=sender_email,
            sender_name=sender_name,
            recipient=user_email,
            subject=subject,
            body=body,
            thread_id=thread_id,
            timestamp=timestamp
        )
        # db.add(db_email)

        # Generate embedding
        if body.strip():  # Skip empty bodies
            embedding = generate_embedding(body)

            # Upsert to vector DB
            # upsert_email_embedding(
            #     email_id=email_id,
            #     embedding=embedding,
            #     metadata={
            #         "sender_email": sender_email,
            #         "sender_name": sender_name,
            #         "subject": subject,
            #         "user_email": user_email
            #     }
            # )

        saved += 1

    db.commit()
    return {"message": f"{saved} new emails saved to DB."}

@router.post("/query-emails")
def query_emails(text: str = Body(...)):
    embedding = generate_embedding(text)
    result = query_similar_emails(embedding)
    # return {result}
    print(f"--> {type(result)}")
    return {f"Embedding dimension: {len(embedding)}"}
