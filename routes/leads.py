from fastapi import APIRouter
from models.schemas import Lead
from storage.memory import leads

router = APIRouter()

@router.post("/leads")
def create_lead(lead: Lead):
    leads.append(lead)
    return {"message": "Lead received", "lead": lead}

