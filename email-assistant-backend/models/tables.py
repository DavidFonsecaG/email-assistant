from sqlalchemy import Column, String, Boolean, Text, DateTime, JSON, ForeignKey, Index
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
    __table_args__ = (
        Index("idx_user_email_timestamp", "user_email", "timestamp"),  # Composite index
    )

    id = Column(String, primary_key=True, index=True)
    user_email = Column(String, index=True)
    source = Column(String, index=True)
    sender_email = Column(String)
    sender_name = Column(String)
    recipient_emails = Column(JSON)
    recipient_names = Column(JSON)
    subject = Column(String)
    body_original = Column(Text)
    body_cleaned = Column(Text)
    thread_id = Column(String, index=True)
    message_id = Column(String, index=True)
    has_attachments = Column(Boolean, default=False)
    is_read = Column(Boolean, default=False)
    importance = Column(String, default="normal")
    web_link = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    attachments = relationship("AttachmentTable", back_populates="email", cascade="all, delete-orphan")


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


class OAuthTokenTable(Base):
    __tablename__ = "oauth_tokens"

    user_email = Column(String, primary_key=True, index=True)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)