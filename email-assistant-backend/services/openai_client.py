import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def summarize_intent(text):
    prompt = f"What is the intent of the following email? Summarize in a short sentence.\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

def suggest_draft_reply(query, sent_results, manual_facts):
    past_replies = "\n".join(email.get('body', '') for email in sent_results)
    facts = "\n".join(f"{k}: {v}" for k, v in manual_facts.items())

    prompt = f"""
    You are my email assistant. Based on my previous replies and official facts, draft a reply to the following inquiry.

    Inquiry:
    {query}

    Previous Replies:
    {past_replies}

    Official Facts:
    {facts}

    Draft a polite and professional reply in my tone:
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

def generate_summary(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content