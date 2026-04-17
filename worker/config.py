from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data.json"
OUTPUT_PATH = BASE_DIR / "images"

ON_GH = os.environ.get("GITHUB_ACTIONS") == "true"