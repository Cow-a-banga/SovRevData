import re

def extract_youtube_id(url: str) -> str | None:
    if not url:
        return None

    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",        # youtube.com/watch?v=
        r"youtu\.be/([a-zA-Z0-9_-]{11})" # youtu.be/
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None