from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from db.database import SessionLocal
from models.tables import EmailTable
from services.openai_client import generate_embedding
from services.openai_client import summarize_intent
from services.openai_client import suggest_draft_reply
from services.outlook_fetch import fetch_received_emails
from services.outlook_fetch import fetch_sent_emails
from services.vector_db import upsert_email_embedding
from services.vector_db import query_similar_emails
from services.knowledge_base import query_knowledge_base
from utils.email_cleaner import clean_email_body

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clean_results(results):
    clean = []
    for match in results.get('matches', []):
        metadata = match.get('metadata', {})
        clean.append({
            "email_id": match.get('id'),
            "subject": metadata.get('subject'),
            "sender_email": metadata.get('sender_email'),
            "sender_name": metadata.get('sender_name'),
            "body": metadata.get('body'),
            "score": match.get('score'),
        })
    return clean

@router.post("/sync-received-emails")
def sync_received_emails(token: str = Body(...), user_email: str = Body(...), db: Session = Depends(get_db)):
    messages = fetch_received_emails(token)

    saved = 0
    for msg in messages:
        email_id = msg["id"]
        sender_info = msg.get("from", {}).get("emailAddress", {})
        sender_email = sender_info.get("address", "")
        sender_name = sender_info.get("name", "")
        subject = msg.get("subject", "")
        body = clean_email_body(msg.get("body", {}).get("content", ""))
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
        db.add(db_email)

        # Generate embedding
        if body.strip():  # Skip empty bodies
            embedding = generate_embedding(body)

        #     # Upsert to vector DB
            upsert_email_embedding(
                email_id=email_id,
                embedding=embedding,
                metadata={
                    "sender_email": sender_email,
                    "sender_name": sender_name,
                    "subject": subject,
                    "user_email": user_email
                }
            )

        saved += 1

    db.commit()
    return {"message": f"{saved} new emails saved to DB."}

@router.post("/sync-sent-emails")
def sync_sent_emails(token: str = Body(...), user_email: str = Body(...), db: Session = Depends(get_db)):

    messages = fetch_sent_emails(token)

    saved = 0
    for msg in messages:
        email_id = msg["id"]
        recipients = msg.get("toRecipients", [])
        recipient_emails = [rec.get("emailAddress", {}).get("address", "") for rec in recipients]
        recipient_names = [rec.get("emailAddress", {}).get("name", "") for rec in recipients]

        subject = msg.get("subject", "")
        body = clean_email_body(msg.get("body", {}).get("content", ""))
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
            sender_email=user_email,  # your sent emails
            sender_name="Me",
            recipient=", ".join(recipient_emails),
            subject=subject,
            body=body,
            thread_id=thread_id,
            timestamp=timestamp
        )
        db.add(db_email)

        # Generate embedding and upsert to Pinecone
        if body.strip():
            embedding = generate_embedding(body)
            upsert_email_embedding(
                email_id=email_id,
                embedding=embedding,
                metadata={
                    "sender_email": user_email,
                    "sender_name": "Me",
                    "subject": subject,
                    "user_email": user_email,
                    "body": body,
                    "source": "sent",
                    "message_class": "manual",  # future proofing
                }
            )

        saved += 1

    db.commit()
    return {"message": f"{saved} sent emails saved and embedded."}

@router.post("/query-emails")
def query_emails(text: str = Body(...)):
    # Step 1: Generate embedding from the input text
    embedding = generate_embedding(text)

    # Step 2: Query Pinecone for sent emails
    sent_results = clean_results(query_similar_emails(embedding, source="sent"))

    # Step 3: Check manual knowledge base
    manual_facts = query_knowledge_base(text)

    # Step 5: Summarize intent (optional: with GPT)
    intent_summary = summarize_intent(text)

    # Step 6: Suggest a draft reply (combine past replies + manual facts)
    suggested_reply = suggest_draft_reply(text, sent_results, manual_facts)

    return {
        "intent_summary": intent_summary,
        "manual_facts": manual_facts,
        "matches_sent": sent_results,
        "suggested_reply": suggested_reply
    }
