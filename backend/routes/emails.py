from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
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
        sender = msg.get("from", {}).get("emailAddress", {}).get("address", "")
        subject = msg.get("subject", "")
        body = msg.get("body", {}).get("content", "")
        thread_id = msg.get("conversationId", "")
        timestamp = msg.get("receivedDateTime", "")

        exists = db.query(EmailTable).filter(EmailTable.id == email_id).first()
        if exists:
            continue

        db_email = EmailTable(
            id=email_id,
            user_email=user_email,
            sender=sender,
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