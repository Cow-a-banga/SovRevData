import yt_dlp
import json
import sys

import re
from datetime import datetime

def get_streams_from_file() -> list:
    with open("../data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def extract_original_link(description):
    if not description:
        return None

    match = re.search(r'Оригинал:\s*(https?://\S+)', description)
    if match:
        return match.group(1)
    return None

def get_stream_info(entry):
    url = f"https://www.youtube.com/watch?v={entry['id']}"
    video_url = extract_original_link(entry['description'])
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        upload_date_str = info.get('upload_date', '')
        if upload_date_str:
            published_at = datetime.strptime(upload_date_str, '%Y%m%d').strftime('%Y-%m-%d')
        else:
            published_at = ''

        data = {
            'title': entry['title'],
            'url': f"https://www.youtube.com/watch?v={entry['id']}",
            'publishedAt': published_at,
            'type': 'video',
            'thumbnail': f"https://img.youtube.com/vi/{entry['id']}/hqdefault.jpg",
            'video': []
        }

        if video_url is not None:
            try:
                video_info = ydl.extract_info(video_url, download=False)
            except Exception:
                return data

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

        return data

def main():
    streams = get_streams_from_file()
    max_date = max(s["publishedAt"] for s in streams)

    print(f"Max date: {max_date}")

    channel_url = "https://www.youtube.com/@sovrev/streams"

    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
        'dump_single_json': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    videos = []
    for entry in info['entries']:
        print(entry)
        info = get_stream_info(entry)
        if info['publishedAt'] == '' or info['publishedAt'] <= max_date:
            break
        videos.append(info)

    if len(videos) == 0:
        sys.exit(0)

    streams = videos + streams
    with open("../data.json", "w", encoding="utf-8") as f:
        json.dump(streams, f, ensure_ascii=False, indent=2)

    sys.exit(1)

main()
