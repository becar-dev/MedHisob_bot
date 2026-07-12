import os
from datetime import datetime
from typing import Optional

import aiosqlite

from bot.config import DB_PATH, PDF_DIR
from bot.utils import normalize_phone

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS analyses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_raw TEXT NOT NULL,
    phone_normalized TEXT NOT NULL,
    full_name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    analysis_type TEXT NOT NULL,
    results_json TEXT NOT NULL,
    pdf_path TEXT NOT NULL,
    doctor_id INTEGER NOT NULL,
    created_at TEXT NOT NULL
)
"""

CREATE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_phone_normalized ON analyses (phone_normalized)
"""


async def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(PDF_DIR, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_TABLE_SQL)
        await db.execute(CREATE_INDEX_SQL)
        await db.commit()


async def add_analysis(
    phone_raw: str,
    full_name: str,
    birth_date: str,
    analysis_type: str,
    results_json: str,
    pdf_path: str,
    doctor_id: int,
) -> None:
    phone_normalized = normalize_phone(phone_raw)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO analyses
               (phone_raw, phone_normalized, full_name, birth_date, analysis_type,
                results_json, pdf_path, doctor_id, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                phone_raw,
                phone_normalized,
                full_name,
                birth_date,
                analysis_type,
                results_json,
                pdf_path,
                doctor_id,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        await db.commit()


async def get_latest_pdf_by_phone(phone: str) -> Optional[str]:
    phone_normalized = normalize_phone(phone)
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """SELECT pdf_path FROM analyses
               WHERE phone_normalized = ?
               ORDER BY id DESC LIMIT 1""",
            (phone_normalized,),
        )
        row = await cursor.fetchone()
        return row[0] if row else None
