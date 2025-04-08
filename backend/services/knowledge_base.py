import json

with open("knowledge_base.json", "r") as file:
    KNOWLEDGE_BASE = json.load(file)

def query_knowledge_base(query):
    matches = {}
    query_lower = query.lower()

    for key, value in KNOWLEDGE_BASE.items():
        if key.lower() in query_lower:
            matches[key] = value

    return matches
