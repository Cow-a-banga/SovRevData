from config import DATA_PATH, OUTPUT_PATH, ON_GH
from repositories.stream_repository import load_streams, save_streams, build_hash_index
from services.youtube_service import get_channel_streams, get_video_info, parse_upload_date
from services.image_service import process_image
from utils.text_utils import extract_original_link

import argparse

from utils.url_utils import extract_youtube_id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    streams = load_streams(DATA_PATH)
    existing_urls = {s["url"] for s in streams}
    existing_hashes = build_hash_index(streams)

    entries = get_channel_streams("https://www.youtube.com/@sovrev/streams")

    new_streams = []

    for entry in entries[:args.limit]:
        url = f"https://www.youtube.com/watch?v={entry['id']}"
        if url in existing_urls:
            continue

        video_url = extract_original_link(entry.get("description"))

        data = {
            "title": entry["title"],
            "url": url,
            "type": "реакции",
            "publishedAt": "",
            "video": []
        }

        image_url = f"https://img.youtube.com/vi/{entry['id']}/hqdefault.jpg"
        filename = f"{entry['id']}.jpg"

        if video_url:
            video_id = extract_youtube_id(video_url)

            data["video"] = [{
                'url': video_url,
                'title': '',
                'author': ''
            }]
            
            image_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            filename = f"{video_id}.jpg"

        if not ON_GH:
            info = get_video_info(url)
            data["publishedAt"] = parse_upload_date(info.get("upload_date"))

        path, phash = process_image(image_url, filename, OUTPUT_PATH, existing_hashes)

        data["thumbnail"] = path
        data["thumbnailHash"] = phash

        existing_hashes[path] = phash

        new_streams.append(data)

    save_streams(DATA_PATH, new_streams + streams)


if __name__ == "__main__":
    main()