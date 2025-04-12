
def clean_results(results):
    clean = []
    for match in results.get('matches', []):
        metadata = match.get('metadata', {})
        clean.append({
            "email_id": match.get('id'),
            "subject": metadata.get('subject'),
            "sender_email": metadata.get('sender_email'),
            "sender_name": metadata.get('sender_name'),
            "body": metadata.get('body'),
            "score": match.get('score'),
        })
    return clean