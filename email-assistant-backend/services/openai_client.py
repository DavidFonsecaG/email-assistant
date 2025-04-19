import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.env import get_env_var 

client = OpenAI(api_key=get_env_var("OPENAI_API_KEY"))

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
    You're my email assistant. Reply to the inquiry using my tone, past replies, and the facts provided. Keep the message concise and professional.

    Return your response in the following JSON format:

    {{
    "response": "Hi ,\\n\\n<response text>\\n\\nBest regards,\\n ",
    "more_ideas": [
        "Short one sentence alternative response topic 1. Keep it under 4 words.",
        "Short one sentence alternative response topic 2. Keep it under 4 words."
    ]
    }}

    Inquiry:
    {query}

    Previous Replies:
    {past_replies}

    Official Facts:
    {facts}
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