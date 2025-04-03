from pydantic import BaseModel
from typing import List
from uuid import UUID

class Lead(BaseModel):
    name: str
    email: str
    company: str
    job_title: str
    interest: str

class EmailDraft(BaseModel):
    id: str
    lead: Lead
    draft_text: str
    approved: bool = False

