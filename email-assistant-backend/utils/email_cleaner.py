import re
import html
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Tuple

def remove_html_tags(text):
    """
    Remove HTML tags and decode HTML entities.
    """
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ")
    text = html.unescape(text)
    return text

def remove_disclaimers(text):
    """
    Remove common disclaimers and warnings from the email body.
    """
    disclaimers = [
        r"This message was intended for .*?\. If you received it in error, please contact us\.",
        r"\[CAUTION: This email originated from outside of the organization\. Do not click links or open attachments unless you recognize the sender and know the content is safe\]"
    ]
    for disclaimer in disclaimers:
        text = re.sub(disclaimer, '', text, flags=re.IGNORECASE)
    return text

def remove_reply_headers(text):
    """
    Remove common reply headers like 'On [date], [person] wrote:'
    """
    pattern = r"On\s.+?wrote:"
    return re.split(pattern, text)[0]

def remove_signature(text):
    """
    Attempt to remove common email signatures.
    """
    signature_markers = ["--", "Thanks,", "Best,", "Sent from my", "Regards,"]
    for marker in signature_markers:
        if marker in text:
            text = text.split(marker)[0]
    return text

def remove_extra_whitespace(text):
    """
    Remove excessive whitespace.
    """
    return ' '.join(text.split())

def clean_email_body(raw_body):
    """
    Full cleaning pipeline for an email body.
    """
    text = remove_html_tags(raw_body)
    text = remove_disclaimers(text)
    text = remove_reply_headers(text)
    text = remove_signature(text)
    text = remove_extra_whitespace(text)
    return text

def extract_recipients(recipients: List[Dict]) -> Tuple[List[str], List[str]]:
    emails = []
    names = []
    for rec in recipients:
        email_data = rec.get("emailAddress", {})
        emails.append(email_data.get("address", ""))
        names.append(email_data.get("name", ""))
    return emails, names

def parse_timestamp(timestamp_str: str) -> datetime:
    if timestamp_str:
        return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    return datetime.utcnow()
