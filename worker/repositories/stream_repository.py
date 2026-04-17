import json

def load_streams(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_streams(path, streams):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(streams, f, ensure_ascii=False, indent=2)


def build_hash_index(streams):
    result = {}
    for s in streams:
        if "thumbnailHash" in s:
            result[s["thumbnail"]] = s["thumbnailHash"]
    return result