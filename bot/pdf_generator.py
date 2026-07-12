import os
from datetime import datetime
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML

from bot.analysis_types import ANALYSIS_TYPES
from bot.config import PDF_DIR, STATIC_DIR, TEMPLATES_DIR

_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)

_LOGO_URI = Path(os.path.join(STATIC_DIR, "logo.png")).as_uri()
_INSTAGRAM_QR_URI = Path(os.path.join(STATIC_DIR, "instagram_qr.png")).as_uri()
_TELEGRAM_QR_URI = Path(os.path.join(STATIC_DIR, "telegram_qr.png")).as_uri()

ORG_ADDRESS = "Toshkent viloyati, Qibray tumani, Universitet ko'chasi, 8-uy"
ORG_PHONES = ["+998 71 260-46-45", "+998 70 020-88-08"]


def generate_pdf(
    analysis_type: str,
    full_name: str,
    birth_date: str,
    field_results: List[str],
) -> str:
    """`field_results` — ANALYSIS_TYPES[analysis_type]['fields'] bilan bir xil
    tartibda, doktor kiritgan/tanlagan natija matnlari ro'yxati."""
    info = ANALYSIS_TYPES[analysis_type]
    field_defs = info["fields"]

    fields = [
        {
            "name": field_defs[i].name,
            "unit": field_defs[i].unit,
            "norma": field_defs[i].norma.replace("\n", "<br>"),
            "result": field_results[i],
        }
        for i in range(len(field_defs))
    ]

    now = datetime.now()
    template = _env.get_template(info["template"])
    html = template.render(
        title=info["title"],
        subtitle=info["subtitle"],
        full_name=full_name,
        birth_date=birth_date,
        registration_date=now.strftime("%d.%m.%Y"),
        ready_date=now.strftime("%d.%m.%Y"),
        fields=fields,
        logo_path=_LOGO_URI,
        instagram_qr_path=_INSTAGRAM_QR_URI,
        telegram_qr_path=_TELEGRAM_QR_URI,
        org_address=ORG_ADDRESS,
        org_phones=ORG_PHONES,
        generated_at=now.strftime("%d.%m.%Y %H:%M"),
    )

    os.makedirs(PDF_DIR, exist_ok=True)
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    safe_phone_or_name = "".join(ch for ch in full_name if ch.isalnum()) or "bemor"
    filename = f"{analysis_type}_{safe_phone_or_name}_{timestamp}.pdf"
    filepath = os.path.join(PDF_DIR, filename)

    HTML(string=html, base_url=TEMPLATES_DIR).write_pdf(filepath)
    return filepath
