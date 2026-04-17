import yt_dlp
from datetime import datetime

ydl_opts = {
    'skip_download': True,
    'dump_single_json': True
}

ydl_flat_opts = {
    'extract_flat': True,
    'skip_download': True,
    'dump_single_json': True
}

def get_channel_streams(channel_url):
    with yt_dlp.YoutubeDL(ydl_flat_opts) as ydl:
        return ydl.extract_info(channel_url, download=False)['entries']

def get_video_info(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

def parse_upload_date(upload_date_str):
    if not upload_date_str:
        return ''
    return datetime.strptime(upload_date_str, '%Y%m%d').strftime('%Y-%m-%d')