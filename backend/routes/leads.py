from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.schemas import Lead
from models.tables import LeadTable

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/leads")
def create_lead(lead: Lead, db: Session = Depends(get_db)):
    existing_lead = db.query(LeadTable).filter(LeadTable.email == lead.email).first()

    if existing_lead:
        return {"message": "Lead already exists", "lead": {
            "email": existing_lead.email,
            "name": existing_lead.name,
            "company": existing_lead.company,
            "job_title": existing_lead.job_title,
            "interest": existing_lead.interest
        }}

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

    return {"message": "Lead saved to DB", "lead": db_lead}
