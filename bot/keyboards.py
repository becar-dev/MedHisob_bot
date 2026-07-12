from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from bot.analysis_types import ANALYSIS_TYPES


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Kontaktni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def get_analysis_type_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=info["button_label"], callback_data=f"analysis:{key}")]
        for key, info in ANALYSIS_TYPES.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_new_patient_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Yangi bemor qo'shish", callback_data="new_patient")],
        ]
    )
