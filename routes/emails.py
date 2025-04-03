from fastapi import APIRouter, Body
from uuid import uuid4
from models.schemas import Lead, EmailDraft
from storage.memory import email_drafts
from services.openai_client import generate_email
from services.outlook_email import send_outlook_email

router = APIRouter()

@router.post("/generate-email")
def generate_email_for_lead(lead: Lead):
    email_text = generate_email(lead.dict())
    draft = EmailDraft(
        id=str(uuid4()),
        lead=lead,
        draft_text=email_text,
        approved=False
    )
    email_drafts.append(draft)
    return {"draft_id": draft.id, "draft": draft}

@router.post("/approve-email/{draft_id}")
def approve_email(draft_id: str):
    for draft in email_drafts:
        if draft.id == draft_id:
            draft.approved = True
            return {"message": "Draft approved", "draft": draft}
    return {"error": "Draft not found"}, 404

@router.post("/send-email/{draft_id}")
def send_approved_email(draft_id: str, token: str = Body(...)):
    print("-->", token)
    for draft in email_drafts:
        if draft.id == draft_id:
            if not draft.approved:
                return {"error": "Email not approved yet"}
            recipient = draft.lead.email
            subject = f"Following up from {draft.lead.company}"
            return send_outlook_email(token, recipient, subject, draft.draft_text)
    return {"error": "Draft not found"}, 404