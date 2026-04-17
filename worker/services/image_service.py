import os
import requests
from PIL import Image
import imagehash

def calculate_phash(path):
    with Image.open(path) as img:
        return str(imagehash.phash(img))


def find_similar(new_hash, existing_hashes, threshold=5):
    for path, h in existing_hashes.items():
        if imagehash.hex_to_hash(new_hash) - imagehash.hex_to_hash(h) <= threshold:
            return path
    return None


def download_image(url, filepath):
    response = requests.get(url)
    with open(filepath, "wb") as f:
        f.write(response.content)


def process_image(url, filename, output_path, existing_hashes):
    filepath = os.path.join(output_path, filename)
    webpath = f"./images/{filename}"

    if existing_hashes.get(webpath) is not None:
        return webpath, existing_hashes.get(webpath)

    download_image(url, filepath)
    new_hash = calculate_phash(filepath)

    similar = find_similar(new_hash, existing_hashes)

    if similar:
        os.remove(filepath)
        return similar, existing_hashes[similar]

    return webpath, new_hash