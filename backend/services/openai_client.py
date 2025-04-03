import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_email(lead: dict) -> str:
    prompt = f"""
    Write a friendly and professional follow-up sales email to {lead['name']}, a {lead['job_title']} at {lead['company']}, who showed interest in {lead['interest']}.
    The email should explain how our AI Sales Assistant works and offer a quick call to discuss.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content":prompt}],
        temperature=0.7,
        max_tokens=300
    )

    return response.choices[0].message.content

