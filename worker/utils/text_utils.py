import re

def extract_original_link(description):
    if not description:
        return None

    match = re.search(r'Оригинал:\s*(https?://\S+)', description)
    return match.group(1) if match else None