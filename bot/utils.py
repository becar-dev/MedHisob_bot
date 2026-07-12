import re


def normalize_phone(phone: str) -> str:
    """Telefon raqamni faqat raqamlarga tushiradi va oxirgi 9 xonasini
    (O'zbekiston mahalliy raqami) qaytaradi, shu orqali '+998901234567',
    '998901234567' va '901234567' bir xil raqam sifatida solishtiriladi."""
    digits = re.sub(r"\D", "", phone or "")
    return digits[-9:] if len(digits) >= 9 else digits
