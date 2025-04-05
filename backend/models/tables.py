from sqlalchemy import Column, String, Boolean, Text, DateTime
from db.database import Base
from datetime import datetime

class LeadTable(Base):
    __tablename__ = "leads"

    email = Column(String, primary_key=True, index=True)
    name = Column(String)
    company = Column(String)
    job_title = Column(String)
    interest = Column(String)

class EmailDraftTable(Base):
    __tablename__ = "email_drafts"

    id = Column(String, primary_key=True, index=True)
    lead_email = Column(String)
    draft_text = Column(Text)
    approved = Column(Boolean, default=False)

class UserTable(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    access_token = Column(Text)

class EmailTable(Base):
    __tablename__ = "emails"

    id = Column(String, primary_key=True)
    user_email = Column(String, index=True)
    sender_email = Column(String)
    sender_name = Column(String)
    recipient = Column(String)
    subject = Column(String)
    body = Column(Text)
    thread_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
