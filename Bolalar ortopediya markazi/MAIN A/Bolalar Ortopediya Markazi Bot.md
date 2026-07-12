# Bolalar Ortopediya Markazi — Doktor/Bemor PDF Bot

Framework: aiogram 3.x + aiosqlite + Jinja2 + WeasyPrint
Vazifa: Doktor va Bemor o'rtasida analiz natijalarini faqat PDF formatda xavfsiz almashish. PDF dizayni markazning haqiqiy Word blankalariga (4 ta analiz turi) mos qilib qurilgan.

## Bot nima qiladi
- **Doktor**: `/start` (yoki `/add_patient`) → darhol `InlineKeyboardMarkup` GUI: 4 ta analiz turi tugmasi (Qon analizi, Vitamin D, Siydik analizi, Umumiy klinik analiz).
- Tur tanlangach: F.I.SH → tug'ilgan sana (DD.MM.YYYY) → telefon raqam (+998...) so'raladi (har birida validatsiya).
- Shundan so'ng bot shu analiz turiga tegishli har bir natija maydonini birma-bir so'raydi — har birida ikkita tezkor variant: **✅ Norma** (bitta tugma bosish bilan "Norma chegarasida" deb yozadi) yoki **✏️ Qiymat kiritish** (qo'lda aniq son/matn). Bu ayniqsa 21 maydonli "Umumiy klinik analiz" uchun kiritishni sezilarli tezlashtiradi.
- Barcha maydonlar to'ldirilgach: SQLite'ga saqlanadi (`results_json` sifatida, chunki turlar orasida maydon soni 1 tadan 21 tagacha farq qiladi) va darhol tegishli Jinja2/WeasyPrint shabloni bilan PDF generatsiya qilinib doktorga yuboriladi.
- **Bemor**: `/start` → "Kontaktni yuborish" tugmasi orqali o'z raqamini yuboradi → bot mos PDF topsa, faqat PDF faylning o'zini yuboradi (ortiqcha xabarsiz).
- **Xavfsizlik**: `contact.user_id == message.from_user.id` tekshiruvi — birov boshqasining kontaktini yuborsa, rad etiladi.
- Ikkala rol bitta botda: Doktor routeri `.env`dagi `DOCTOR_IDS` ro'yxati bilan filtrlangan.
- Hech qanday qo'shimcha funksiya yo'q (to'lov, admin panel va h.k.) — faqat so'ralgan vazifa.

## PDF dizayni — 4 ta haqiqiy blankadan olingan
Foydalanuvchi yuklagan 4 ta Word fayl (`Downloads\Telegram Desktop\`) asosida qurilgan:
- `lab_result_blank.docx` → Vitamin D (1 maydon)
- `Анализ крови.docx` → Qon analizi / koagulogramma (8 maydon: PT, PTI, INR, FIB, TT sek/nisbat, PTT sek/nisbat)
- `Результаты тестирования мочи.docx` → Siydik analizi (11 maydon)
- `Общие клинические анализы.docx` → Umumiy klinik analiz (21 maydon)

Har bir PDF quyidagilarni o'z ichiga oladi: markaz logotipi (header), ikki tilli (rus/o'zbek) sarlavha "ЛАБОРАТОРНЫЙ АНАЛИЗ / LABORATORIYA TAHLILI NATIJALARI", bemor ma'lumotlari jadvali, Nomi/Natija/Birlik/Norma ustunli natija jadvali, imzo joyi (Zav.laboratoriya yoki Laborant), "ВАЖНО / MUHIM" ogohlantirish qutisi (O'zR JK 228-moddasi) va Instagram QR kodi (@ortopediya_markazi).

Rang kodlari (Word fayllardan XML orqali olingan): sarlavha paneli `#1A5276`, jadval header `#2E86C1`, bemor jadval foni `#D6EAF8`, ogohlantirish qutisi `#FEF9E7`.

## Fayllar tuzilishi
```
Bolalar ortopediya markazi/
├── .env / .env.example
├── requirements.txt
├── bot/
│   ├── config.py            # .env, DOCTOR_IDS, DB/PDF/TEMPLATES/STATIC yo'llari
│   ├── utils.py              # normalize_phone()
│   ├── analysis_types.py     # 4 analiz turi + har biri uchun maydonlar (kod/nomi/birlik/norma)
│   ├── database.py           # SQLite: full_name, birth_date, analysis_type, results_json
│   ├── pdf_generator.py      # Jinja2 render + WeasyPrint HTML→PDF
│   ├── states.py             # Doktor FSM holatlari
│   ├── keyboards.py          # analiz turi + "Norma/Qiymat kiritish" inline tugmalari, kontakt tugmasi
│   ├── main.py
│   ├── templates/
│   │   ├── base.html         # umumiy struktura + CSS (logo, jadvallar, ogohlantirish, QR)
│   │   ├── vitamin_d.html
│   │   ├── qon_analizi.html
│   │   ├── siydik_analizi.html
│   │   └── umumiy_klinik.html
│   ├── static/
│   │   ├── logo.png           # markaz logotipi (Word fayllardan chiqarilgan)
│   │   └── instagram_qr.jpeg  # @ortopediya_markazi QR kodi
│   └── handlers/
│       ├── doctor.py          # inline GUI → FSM → PDF
│       └── patient.py         # kontakt → xavfsizlik → PDF
└── data/                       # runtime: database.db va pdfs/
```

## ⚠️ Muhim: ishga tushirish uchun alohida conda muhiti kerak
WeasyPrint Windows'da oddiy `pip install`da ishlamaydi (GTK/Pango/Cairo native kutubxonalari yo'qligi sababli `OSError: cannot load library 'libgobject-2.0-0'`). Shuning uchun **`ortopediya-bot`** nomli alohida conda muhiti yaratilgan:

```
conda activate ortopediya-bot
python -m bot.main
```

yoki to'g'ridan-to'g'ri: `C:\Users\becar\miniconda3\envs\ortopediya-bot\python.exe -m bot.main`

Global miniconda `base` muhitida oddiy `python -m bot.main` ishlamaydi (WeasyPrint import xatosi beradi). Batafsil: [[tech]] (`Documents\Obsidian Vault\Learnings\tech.md`).

## Asosiy sozlamalar

| Kalit | Qiymat |
|-------|--------|
| BOT_TOKEN | BotFather'dan olingan token (`.env`) |
| DOCTOR_IDS | Doktorlarning Telegram ID'lari, vergul bilan (`.env`, hozircha 3 ta) |
| DB | SQLite — `data/database.db` (`analyses` jadvali: phone, full_name, birth_date, analysis_type, results_json, pdf_path, doctor_id, created_at) |
| PDF papkasi | `data/pdfs/` |
| PDF sarlavhasi | "ЛАБОРАТОРНЫЙ АНАЛИЗ / LABORATORIYA TAHLILI NATIJALARI" + logo header |
| Conda muhit | `ortopediya-bot` (weasyprint, jinja2, aiogram, aiosqlite, python-dotenv) |
| Telefon normalizatsiyasi | oxirgi 9 xona bo'yicha solishtiriladi |

## Holat
✅ To'liq qayta qurildi: 4 ta haqiqiy Word blankaga mos Inline GUI + Jinja2/WeasyPrint PDF tizimi. Barcha 4 PDF turi generatsiya qilinib, PyMuPDF bilan vizual tekshirildi — Word originalga yaqin fidelity tasdiqlandi.
✅ Bot `ortopediya-bot` conda muhitida ishga tushirilib, polling holatida ishlagani tasdiqlandi.
⏳ Hali qilinmagan: real Telegram orqali to'liq doktor oqimi (barcha 4 tur bo'yicha) va bemor tomonidan PDF olish qo'lda sinalmagan.

## Bog'liq sahifalar
- [[MAIN A]]
