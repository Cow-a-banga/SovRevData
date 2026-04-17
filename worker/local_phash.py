from config import OUTPUT_PATH
from services.image_service import calculate_phash

filename = input("Название картинки: ")
path = OUTPUT_PATH / filename

phash = calculate_phash(path)
print(phash)