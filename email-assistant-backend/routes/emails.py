from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from db.database import SessionLocal
from models.tables import EmailTable
from services.openai_client import generate_embedding, summarize_intent, suggest_draft_reply
from services.outlook_fetch import fetch_received_emails, fetch_sent_emails
from services.vector_db import upsert_email_embedding, query_similar_emails
from services.knowledge_base import query_knowledge_base
from utils.email_cleaner import clean_email_body, extract_recipients, parse_timestamp
from utils.results_cleaner import clean_results

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/test")
def test(token: str = Body(...), user_email: str = Body(...), db: Session = Depends(get_db)):
    sent_emails = fetch_sent_emails(token)
    received_emails = fetch_received_emails(token)
    return {
        "sent_emails": sent_emails,
        "received_emails": received_emails
    }

@router.get("/emails")
def get_emails(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1), db: Session = Depends(get_db)):
    offset = (page - 1) * page_size
    total = db.query(EmailTable).count()
    emails = (
        db.query(EmailTable)
        .order_by(EmailTable.timestamp.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return { "emails": emails, "total": total }

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

        if db.query(EmailTable).filter(EmailTable.id == email_id).first():
            continue

        recipient_emails, recipient_names = extract_recipients(msg.get("toRecipients", []))
        body_original = msg.get("body", {}).get("content", "")
        body_cleaned = clean_email_body(body_original)
        db_email = EmailTable(
            id=email_id,
            user_email=user_email,
            source="sent",
            sender_email=user_email,
            sender_name="Me",
            recipient_emails=recipient_emails,
            recipient_names=recipient_names,
            subject=msg.get("subject", ""),
            body_original=body_original,
            body_cleaned=body_cleaned,
            thread_id=msg.get("conversationId", ""),
            message_id=msg.get("internetMessageId", ""),
            has_attachments=bool(msg.get("hasAttachments", False)),
            is_read=True,
            importance=msg.get("importance", "normal"),
            web_link=msg.get("webLink", ""),
            timestamp=parse_timestamp(msg.get("receivedDateTime", ""))
        )

        db.add(db_email)

        if body_cleaned:
            embedding = generate_embedding(body_cleaned)
            upsert_email_embedding(
                email_id=email_id,
                embedding=embedding,
                metadata={
                    "sender_email": user_email,
                    "sender_name": "Me",
                    "subject": msg.get("subject", ""),
                    "user_email": user_email,
                    "body": body_cleaned,
                    "source": "sent",
                    "thread_id": msg.get("conversationId", ""),
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
