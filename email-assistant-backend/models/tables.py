from sqlalchemy import Column, String, Boolean, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class EmailDraftTable(Base):
    __tablename__ = "email_drafts"

    id = Column(String, primary_key=True, index=True)
    lead_email = Column(String)
    draft_text = Column(Text)
    approved = Column(Boolean, default=False)

class EmailTable(Base):
    __tablename__ = "emails"

    id = Column(String, primary_key=True)  # Outlook ID
    user_email = Column(String, index=True)  # Account owner
    source = Column(String, index=True)  # 'sent' or 'received'
    sender_email = Column(String)
    sender_name = Column(String)
    recipient_emails = Column(JSON)  # List of recipient emails
    recipient_names = Column(JSON)   # List of recipient names
    subject = Column(String)
    body_original = Column(Text)  # Raw, for frontend display
    body_cleaned = Column(Text)   # Cleaned, for Pinecone embeddings
    thread_id = Column(String, index=True)  # ConversationId
    message_id = Column(String, index=True)  # internetMessageId
    has_attachments = Column(Boolean, default=False)
    is_read = Column(Boolean, default=False)
    importance = Column(String, default="normal")
    web_link = Column(String)  # Direct link to open in Outlook
    timestamp = Column(DateTime, default=datetime.utcnow)  # Best effort unified timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

class AttachmentTable(Base):
    __tablename__ = "attachments"

    id = Column(String, primary_key=True)
    email_id = Column(String, ForeignKey("emails.id"))
    name = Column(String)
    content_type = Column(String)
    size = Column(String)
    content_bytes = Column(Text)  # base64-encoded string or blob
    web_link = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    email = relationship("EmailTable", back_populates="attachments")