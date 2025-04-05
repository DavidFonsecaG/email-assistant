from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from db.database import SessionLocal
from models.tables import EmailTable, LeadTable
from services.openai_client import generate_email
from services.outlook_fetch import fetch_recent_emails

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

        db_email = EmailTable(
            id=email_id,
            user_email=user_email,
            sender_email=sender_email,
            sender_name=sender_name,
            recipient=user_email,  # Simplified for now
            subject=subject,
            body=body,
            thread_id=thread_id,
            timestamp=timestamp
        )
        db.add(db_email)
        saved += 1

    db.commit()
    return {"message": f"{saved} new emails saved to DB."}