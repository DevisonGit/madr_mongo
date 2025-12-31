def sanitize_string(word: str) -> str:
    return ' '.join(word.lower().strip().split())
