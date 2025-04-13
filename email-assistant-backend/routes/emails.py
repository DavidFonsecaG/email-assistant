from datetime import datetime
from fastapi import APIRouter, Body, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.tables import EmailTable
from services.openai_client import generate_embedding, summarize_intent, suggest_draft_reply, generate_summary
from services.outlook_fetch import fetch_received_emails, fetch_sent_emails
from services.vector_db import upsert_email_embedding, query_similar_emails, query_email_embeddings
from services.knowledge_base import query_knowledge_base
from utils.email_cleaner import clean_email_body, extract_recipients, parse_timestamp
from utils.results_cleaner import clean_results
from utils.text_truncater import truncate_text_to_token_limit

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/emails")
def get_emails(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    user_email: str = Query(...),
    source: str = Query(None, regex="^(sent|received)$"),
    is_read: bool = Query(None),
    has_attachments: bool = Query(None),
    sort_by: str = Query("timestamp", regex="^(timestamp|subject)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * page_size
    query = db.query(EmailTable).filter(EmailTable.user_email == user_email)

    if source:
        query = query.filter(EmailTable.source == source)

    if is_read is not None:
        query = query.filter(EmailTable.is_read == is_read)

    if has_attachments is not None:
        query = query.filter(EmailTable.has_attachments == has_attachments)

    sort_column = getattr(EmailTable, sort_by)
    if order == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    query = query.order_by(sort_column)

    total = query.count()

    emails = query.offset(offset).limit(page_size).all()

    serialized_emails = []
    for email in emails:
        serialized_emails.append({
            "id": email.id,
            "source": email.source,
            "sender_name": email.sender_name,
            "sender_email": email.sender_email,
            "recipient_names": email.recipient_names,
            "recipient_emails": email.recipient_emails,
            "subject": email.subject,
            "is_read": email.is_read,
            "body_preview": email.body_cleaned[:150] if email.body_cleaned else "",
            "timestamp": email.timestamp.isoformat() if email.timestamp else None,
            "thread_id": email.thread_id,
            "has_attachments": email.has_attachments,
            "web_link": email.web_link
        })

    return {
        "emails": serialized_emails,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

@router.get("/emails/{email_id}")
def get_email_by_id(email_id: str, db: Session = Depends(get_db)):
    email = db.query(EmailTable).filter(EmailTable.id == email_id).first()

    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    return {
        "id": email.id,
        "source": email.source,
        "sender_name": email.sender_name,
        "sender_email": email.sender_email,
        "recipient_names": email.recipient_names,
        "recipient_emails": email.recipient_emails,
        "subject": email.subject,
        "body_original": email.body_original,
        "timestamp": email.timestamp.isoformat(),
        "has_attachments": email.has_attachments,
        "web_link": email.web_link
    }

@router.get("/emails/thread/{thread_id}")
def get_emails_by_thread(thread_id: str, user_email: str, db: Session = Depends(get_db)):
    emails = (
        db.query(EmailTable)
        .filter(EmailTable.user_email == user_email, EmailTable.thread_id == thread_id)
        .order_by(EmailTable.timestamp.asc())
        .all()
    )

    results = []
    for email in emails:
        results.append({
            "id": email.id,
            "source": email.source,
            "sender_name": email.sender_name,
            "sender_email": email.sender_email,
            "recipient_names": email.recipient_names,
            "recipient_emails": email.recipient_emails,
            "subject": email.subject,
            "body_original": email.body_original,
            "timestamp": email.timestamp.isoformat(),
            "has_attachments": email.has_attachments,
            "web_link": email.web_link
        })

    return results

@router.get("/emails/{email_id}/summary")
def summarize_email(email_id: str, db: Session = Depends(get_db)):
    email = db.query(EmailTable).filter(EmailTable.id == email_id).first()

    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    prompt = f"Summarize the following email in a few sentences:\n\n{email.body_cleaned}"
    summary = generate_summary(prompt)

    return {"email_id": email_id, "summary": summary}

@router.get("/emails/thread/{thread_id}/summary")
def summarize_thread(thread_id: str, user_email: str, db: Session = Depends(get_db)):
    emails = (
        db.query(EmailTable)
        .filter(EmailTable.user_email == user_email, EmailTable.thread_id == thread_id)
        .order_by(EmailTable.timestamp.asc())
        .all()
    )

    if not emails:
        raise HTTPException(status_code=404, detail="Thread not found")

    conversation_text = "\n\n".join(
        f"{email.sender_name}: {email.body_cleaned}" for email in emails if email.body_cleaned
    )

    prompt = f"Summarize the following email conversation in a few sentences:\n\n{conversation_text}"
    summary = generate_summary(prompt)

    return {"thread_id": thread_id, "summary": summary}

@router.post("/query-emails")
def query_emails(text: str = Body(...)):
    # Step 1: Generate embedding from the input text
    embedding = generate_embedding(text)

    # Step 2: Query Pinecone for sent emails
    sent_results = clean_results(query_similar_emails(embedding, source="sent"))

    # Step 3: Check manual knowledge base
    manual_facts = query_knowledge_base(text)

    # Step 5: Summarize intent (optional: with GPT)
    intent_summary = summarize_intent(text)

    # Step 6: Suggest a draft reply (combine past replies + manual facts)
    suggested_reply = suggest_draft_reply(text, sent_results, manual_facts)

    return {
        "intent_summary": intent_summary,
        "manual_facts": manual_facts,
        "matches_sent": sent_results,
        "suggested_reply": suggested_reply
    }

@router.post("/search-emails")
def search_emails(query: str = Body(...), user_email: str = Body(...), top_k: int = Body(5), db: Session = Depends(get_db)):
    query_embedding = generate_embedding(query)

    results = query_email_embeddings(
        embedding=query_embedding,
        top_k=top_k,
        filter={"user_email": {"$eq": user_email}}
    )

    email_ids = [match["id"] for match in results["matches"]]
    emails = db.query(EmailTable).filter(EmailTable.id.in_(email_ids)).all()

    response = []
    for email in emails:
        response.append({
            "id": email.id,
            "source": email.source,
            "sender_name": email.sender_name,
            "sender_email": email.sender_email,
            "recipient_names": email.recipient_names,
            "recipient_emails": email.recipient_emails,
            "subject": email.subject,
            "body_original": email.body_original,
            "timestamp": email.timestamp.isoformat(),
            "thread_id": email.thread_id,
            "has_attachments": email.has_attachments,
            "web_link": email.web_link
        })

    return response

@router.post("/sync-received-emails")
def sync_received_emails(token: str = Body(...), user_email: str = Body(...), db: Session = Depends(get_db)):
    messages = fetch_received_emails(token)

    saved = 0
    for msg in messages:
        email_id = msg["id"]

        if db.query(EmailTable).filter(EmailTable.id == email_id).first():
            continue

        sender_info = msg.get("from", {}).get("emailAddress", {})
        sender_email = sender_info.get("address", "")
        sender_name = sender_info.get("name", "")

        recipient_emails, recipient_names = extract_recipients(msg.get("toRecipients", []))

        body_original = msg.get("body", {}).get("content", "")
        body_cleaned = clean_email_body(body_original)

        db_email = EmailTable(
            id=email_id,
            user_email=user_email,
            source="received",
            sender_email=sender_email,
            sender_name=sender_name,
            recipient_emails=recipient_emails,
            recipient_names=recipient_names,
            subject=msg.get("subject", ""),
            body_original=body_original,
            body_cleaned=body_cleaned,
            thread_id=msg.get("conversationId", ""),
            message_id=msg.get("internetMessageId", ""),
            has_attachments=bool(msg.get("hasAttachments", False)),
            is_read=bool(msg.get("isRead", False)),
            importance=msg.get("importance", "normal"),
            web_link=msg.get("webLink", ""),
            timestamp=parse_timestamp(msg.get("receivedDateTime", ""))
        )

        db.add(db_email)

        if body_cleaned:
            embedding = generate_embedding(truncate_text_to_token_limit(body_cleaned))
            upsert_email_embedding(
                email_id=email_id,
                embedding=embedding,
                metadata={
                    "sender_email": sender_email,
                    "sender_name": sender_name,
                    "subject": msg.get("subject", ""),
                    "user_email": user_email,
                    "body": body_cleaned,
                    "source": "received",
                    "thread_id": msg.get("conversationId", ""),
                }
            )

        saved += 1

    db.commit()
    return {"message": f"{saved} received emails saved and embedded."}

@router.post("/sync-sent-emails")
def sync_sent_emails(token: str = Body(...), user_email: str = Body(...), db: Session = Depends(get_db)):
    messages = fetch_sent_emails(token)

    saved = 0
    for msg in messages:
        email_id = msg["id"]

        if db.query(EmailTable).filter(EmailTable.id == email_id).first():
            continue

        recipient_emails, recipient_names = extract_recipients(msg.get("toRecipients", []))
        body_original = msg.get("body", {}).get("content", "")
        body_cleaned = clean_email_body(body_original)
        db_email = EmailTable(
            id=email_id,
            user_email=user_email,
            source="sent",
            sender_email=user_email,
            sender_name="Me",
            recipient_emails=recipient_emails,
            recipient_names=recipient_names,
            subject=msg.get("subject", ""),
            body_original=body_original,
            body_cleaned=body_cleaned,
            thread_id=msg.get("conversationId", ""),
            message_id=msg.get("internetMessageId", ""),
            has_attachments=bool(msg.get("hasAttachments", False)),
            is_read=True,
            importance=msg.get("importance", "normal"),
            web_link=msg.get("webLink", ""),
            timestamp=parse_timestamp(msg.get("receivedDateTime", ""))
        )

        db.add(db_email)

        if body_cleaned:
            embedding = generate_embedding(truncate_text_to_token_limit(body_cleaned))
            upsert_email_embedding(
                email_id=email_id,
                embedding=embedding,
                metadata={
                    "sender_email": user_email,
                    "sender_name": "Me",
                    "subject": msg.get("subject", ""),
                    "user_email": user_email,
                    "body": body_cleaned,
                    "source": "sent",
                    "thread_id": msg.get("conversationId", ""),
                }
            )

        saved += 1

    db.commit()
    return {"message": f"{saved} sent emails saved and embedded."}
