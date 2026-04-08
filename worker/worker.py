import yt_dlp
import json
import os

import re
from datetime import datetime

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data.json"
ON_GH = os.environ.get("GITHUB_ACTIONS") == "true"

ydl_flat_opts = {
    'extract_flat': True,
    'skip_download': True,
    'dump_single_json': True
}

ydl_opts = {
    'skip_download': True,
    'dump_single_json': True
}

def get_streams_from_file() -> list:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_original_link(description):
    if not description:
        return None

    match = re.search(r'Оригинал:\s*(https?://\S+)', description)
    if match:
        return match.group(1)
    return None

def enrich_additional_info(url, video_url, data):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    upload_date_str = info.get('upload_date', '')
    if upload_date_str:
        published_at = datetime.strptime(upload_date_str, '%Y%m%d').strftime('%Y-%m-%d')
    else:
        published_at = ''

    data['publishedAt'] = published_at

    if video_url is not None:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(video_url, download=False)

        author = (
                video_info.get('uploader') or
                video_info.get('channel') or
                video_info.get('uploader_id')
        )

        data['video'] = [{
            'url': video_url,
            'title': video_info.get('title', 'Без названия'),
            'author': author
        }]

        data['thumbnail'] = f"https://img.youtube.com/vi/{video_info['id']}/hqdefault.jpg"

def get_stream_info(entry):
    url = f"https://www.youtube.com/watch?v={entry['id']}"
    video_url = extract_original_link(entry['description'])
    data = {
        'title': entry['title'],
        'url': f"https://www.youtube.com/watch?v={entry['id']}",
        'type': 'реакции',
        'thumbnail': f"https://img.youtube.com/vi/{entry['id']}/hqdefault.jpg",
        'video': [{
            'url': video_url,
            'title': '',
            'author': ''
        }],
        'publishedAt': ''
    }

    if not ON_GH:
        enrich_additional_info(url, video_url, data)

    return data

def main():
    streams = get_streams_from_file()
    max_date = max(s["publishedAt"] for s in streams)

    print(f"Max date: {max_date}")

    channel_url = "https://www.youtube.com/@sovrev/streams"

    with yt_dlp.YoutubeDL(ydl_flat_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    videos = []
    for entry in info['entries'][:20]:
        print(entry)
        info = get_stream_info(entry)
        if info['publishedAt'] != '' and info['publishedAt'] <= max_date:
            break
        videos.append(info)

    if len(videos) > 0:
        existing_urls = {s["url"] for s in streams}
        unique_new_videos = [v for v in videos if v["url"] not in existing_urls]
        streams = unique_new_videos + streams

        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(streams, f, ensure_ascii=False, indent=2)

main()
