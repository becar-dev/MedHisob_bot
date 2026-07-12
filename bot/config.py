import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN .env faylida topilmadi!")

_doctor_ids_raw = os.getenv("DOCTOR_IDS", "")
DOCTOR_IDS = {int(x.strip()) for x in _doctor_ids_raw.split(",") if x.strip()}
if not DOCTOR_IDS:
    raise RuntimeError("DOCTOR_IDS .env faylida topilmadi! (Doktorlarning Telegram ID'lari)")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "database.db")
PDF_DIR = os.path.join(BASE_DIR, "data", "pdfs")
TEMPLATES_DIR = os.path.join(BASE_DIR, "bot", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "bot", "static")
