"""Doktor tanlaydigan 4 ta analiz turi va ularning natija maydonlari.

Har bir maydon PDF natija jadvalidagi bitta qatorga mos keladi va doktordan
alohida so'raladi: (kodi, nomi (bilingual), o'lchov birligi, norma matni).
"""

from typing import NamedTuple


class AnalysisField(NamedTuple):
    code: str
    name: str
    unit: str
    norma: str


ANALYSIS_TYPES = {
    "vitamin_d": {
        "button_label": "Vitamin D",
        "title": "ЛАБОРАТОРНЫЙ АНАЛИЗ",
        "subtitle": "LABORATORIYA TAHLILI NATIJALARI",
        "extra_lines": [],
        "template": "vitamin_d.html",
        "signature_label": "Заведующий лабораторией / Laboratoriya mudiri",
        "fields": [
            AnalysisField(
                code="vitamin_d",
                name="Витамин D / Vitamin D",
                unit="ng/ml",
                norma=(
                    "Дефицит: 0–10 / Defitsit: 0–10\n"
                    "Субоптимальное: 10–29 / Suboptimal: 10–29\n"
                    "Оптимальный: 30–70 / Optimal: 30–70\n"
                    "Верхняя норма: 70–100 / Yuqori norma: 70–100\n"
                    "Интоксикация: >100 / Intoksikatsiya: >100"
                ),
            ),
        ],
    },
    "qon_analizi": {
        "button_label": "Qon analizi",
        "title": "ЛАБОРАТОРНЫЙ АНАЛИЗ",
        "subtitle": "LABORATORIYA TAHLILI NATIJALARI",
        "extra_lines": [
            "Анализ крови (коагулограмма) / Qon analizi (koagulogramma)",
            "Коагулометр Humaclot junior (HUMAN GmbH)",
        ],
        "template": "qon_analizi.html",
        "signature_label": "Лаборант / Laborant",
        "fields": [
            AnalysisField("pt_sec", "Протромбиновое время / Protrombin vaqti (PT)", "сек", "8–15"),
            AnalysisField("pti", "П.Т.И. (время по Квику) / P.T.I.", "%", "75–140"),
            AnalysisField("inr", "МНО / INR", "-", "0,8–1,25"),
            AnalysisField("fib", "Фибриноген / Fibrinogen (FIB)", "г/л", "2,0–4,0"),
            AnalysisField("tt_sec", "Тромбиновое время (сек.) / Trombin vaqti", "сек", "до 30 / 30 gacha"),
            AnalysisField("tt_ratio", "Тромбиновое время (соотношение) / Trombin vaqti (nisbat)", "-", "0,8–1,25"),
            AnalysisField("aptt_sec", "А.Ч.Т.В. (сек.) / A.Ch.T.V.", "сек", "27–36"),
            AnalysisField("aptt_ratio", "А.Ч.Т.В. (соотношение) / A.Ch.T.V. (nisbat)", "-", "0,8–1,25"),
        ],
    },
    "siydik_analizi": {
        "button_label": "Siydik analizi",
        "title": "ЛАБОРАТОРНЫЙ АНАЛИЗ",
        "subtitle": "LABORATORIYA TAHLILI NATIJALARI",
        "extra_lines": ["Результаты тестирования мочи / Siydik tahlili natijalari"],
        "template": "siydik_analizi.html",
        "signature_label": "Лаборант / Laborant",
        "fields": [
            AnalysisField("leukocyte_cylinders", "Цилиндры лейкоцитарные / Leykotsitar tsilindrlar", "в п/зр", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("urate_sediment", "Осадок ураты / Urat cho'kmasi", "в п/зр", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("oxalates", "Оксалаты / Oksalatlar", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("uric_acid_crystals", "Кристаллы мочевой кислоты / Siydik kislotasi kristallari", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("amorphous_phosphates", "Аморфные фосфаты / Amorf fosfatlar", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("ammonium_urate", "Мочекислый аммоний / Siydik kislotali ammoniy", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("triple_phosphate", "Трипельфосфат / Tripelfosfat", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("mucus", "Слизь / Shilliq", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("bacteria", "Бактерии / Bakteriyalar", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("yeast", "Дрожжевые грибки / Achitqi qo'ziqorinlari", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("ascorbic_acid", "Аскорбиновая кислота / Askorbin kislotasi", "-", "abs (aniqlanmagan/yo'q)"),
        ],
    },
    "umumiy_klinik": {
        "button_label": "Umumiy klinik analiz",
        "title": "ЛАБОРАТОРНЫЙ АНАЛИЗ",
        "subtitle": "LABORATORIYA TAHLILI NATIJALARI",
        "extra_lines": ["Общие клинические анализы / Umumiy klinik analizlar"],
        "template": "umumiy_klinik.html",
        "signature_label": "Лаборант / Laborant",
        "fields": [
            AnalysisField("amount", "Количество / Miqdori", "мл", ""),
            AnalysisField("color", "Цвет / Rangi", "-", "солом.-желт. / somon-sariq"),
            AnalysisField("transparency", "Прозрачность / Tiniqligi", "-", "прозрачная / tiniq"),
            AnalysisField("density", "Относительная плотность / Solishtirma zichlik", "-", "1010–1026"),
            AnalysisField("ph", "Реакция Ph / Ph reaksiyasi", "-", "5.5–6.5"),
            AnalysisField("glucose", "Глюкоза / Glyukoza", "ммоль/л", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("nitrites", "Нитриты / Nitritlar", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("protein", "Белок / Oqsil", "г/л", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("ketones", "Кетоновые тела / Keton tanachalari", "mmol/l", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("urobilinogen", "Уробилиноген / Urobilinogen", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("bilirubin", "Билирубин / Bilirubin", "-", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("epithelium_flat", "Эпителий: Плоский / Epiteliy: Yassi", "в п/з", "0-3 в поле зрения"),
            AnalysisField("epithelium_transitional", "Эпителий: Переходной / Epiteliy: O'tuvchi", "в п/з", "0-3 в поле зрения"),
            AnalysisField("epithelium_renal", "Эпителий: Почечный / Epiteliy: Buyrak", "в п/з", "0-3 в поле зрения"),
            AnalysisField("leukocytes", "Лейкоциты / Leykotsitlar", "в п/зр", "муж. 1-3, жен. 2-5"),
            AnalysisField("erythrocytes_fresh", "Эритроциты неизмененные / O'zgarmagan eritrotsitlar", "в п/зр", "0–1"),
            AnalysisField("erythrocytes_changed", "Эритроциты измененные / O'zgargan eritrotsitlar", "в п/зр", "0–1"),
            AnalysisField("cylinders_hyaline", "Цилиндры гиалиновые / Gialin tsilindrlar", "в п/зр", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("cylinders_granular", "Цилиндры зернистые / Donador tsilindrlar", "в п/зр", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("cylinders_waxy", "Цилиндры восковидные / Momiqsimon tsilindrlar", "в п/зр", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("cylinders_epithelial", "Цилиндры эпителиальные / Epitelial tsilindrlar", "в п/зр", "abs (aniqlanmagan/yo'q)"),
            AnalysisField("cylinders_erythrocyte", "Цилиндры эритроцитарные / Eritrotsitar tsilindrlar", "в п/зр", "abs (aniqlanmagan/yo'q)"),
        ],
    },
}
