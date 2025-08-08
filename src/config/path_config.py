# src/config/path_config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
USER_DATA_DIR = DATA_DIR / "users"
