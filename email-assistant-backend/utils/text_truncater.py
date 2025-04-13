import tiktoken

def truncate_text_to_token_limit(text: str, model_name: str = "text-embedding-ada-002", max_tokens: int = 8000) -> str:
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text
    truncated_text = encoding.decode(tokens[:max_tokens])
    return truncated_text
