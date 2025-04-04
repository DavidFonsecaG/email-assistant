from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from db.database import SessionLocal
from models.schemas import Lead
from models.tables import EmailDraftTable, LeadTable
from services.openai_client import generate_email
from services.outlook_email import send_outlook_email

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/generate-email")
def generate_email_for_lead(lead: Lead, db: Session = Depends(get_db)):
    db_lead = db.query(LeadTable).filter(LeadTable.email == lead.email).first()
    if not db_lead:
        db_lead = LeadTable(
            email=lead.email,
            name=lead.name,
            company=lead.company,
            job_title=lead.job_title,
            interest=lead.interest
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)

    email_text = generate_email(lead.dict())

    db_draft = EmailDraftTable(
        id=str(uuid4()),
        lead_email=lead.email,
        draft_text=email_text,
        approved=False
    )
    db.add(db_draft)
    db.commit()
    db.refresh(db_draft)

    return {"draft_id": db_draft.id, "draft": {
        "id": db_draft.id,
        "lead_email": db_draft.lead_email,
        "draft_text": db_draft.draft_text,
        "approved": db_draft.approved
    }}

@router.post("/approve-email/{draft_id}")
def approve_email(draft_id: str, db: Session = Depends(get_db)):
    draft = db.query(EmailDraftTable).filter(EmailDraftTable.id == draft_id).first()

    if not draft:
        return {"error": "Draft not found"}, 404

    draft.approved = True
    db.commit()
    db.refresh(draft)

    return {"message": "Draft approved", "draft": {
        "id": draft.id,
        "lead_email": draft.lead_email,
        "draft_text": draft.draft_text,
        "approved": draft.approved
    }}

@router.post("/send-email/{draft_id}")
def send_approved_email(draft_id: str, token: str = Body(...), db: Session = Depends(get_db)):
    draft = db.query(EmailDraftTable).filter(EmailDraftTable.id == draft_id).first()

    if not draft:
        return {"error": "Draft not found"}, 404

    if not draft.approved:
        return {"error": "Draft not approved yet"}

    lead = db.query(LeadTable).filter(LeadTable.email == draft.lead_email).first()

    if not lead:
        return {"error": "Lead not found"}, 404

    recipient = lead.email
    subject = f"Following up from {lead.company}"
    body_text = draft.draft_text

    return send_outlook_email(token, recipient, subject, body_text)