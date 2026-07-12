import os

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message

from bot.database import get_latest_pdf_by_phone
from bot.keyboards import get_contact_keyboard

router = Router()


@router.message(CommandStart())
async def patient_start(message: Message) -> None:
    await message.answer(
        "Assalomu alaykum!\nAnaliz natijangizni olish uchun pastdagi tugma orqali "
        "o'zingizning kontaktingizni yuboring.",
        reply_markup=get_contact_keyboard(),
    )


@router.message(F.contact)
async def patient_receive_contact(message: Message) -> None:
    contact = message.contact

    # Xavfsizlik tekshiruvi: yuborilgan kontakt aynan shu foydalanuvchining
    # o'ziga tegishli bo'lishi shart, aks holda birovning analizini
    # boshqa odam olib qo'yishi mumkin bo'ladi.
    if contact.user_id != message.from_user.id:
        await message.answer(
            "❌ Siz faqat o'zingizning shaxsiy kontaktingizni yuborishingiz mumkin.\n"
            "Iltimos, pastdagi tugma orqali o'z raqamingizni yuboring.",
            reply_markup=get_contact_keyboard(),
        )
        return

    pdf_path = await get_latest_pdf_by_phone(contact.phone_number)

    if pdf_path and os.path.exists(pdf_path):
        await message.answer_document(FSInputFile(pdf_path))
        await message.answer(
            "Yana natija olish uchun pastdagi tugma orqali kontaktni qayta yuboring:",
            reply_markup=get_contact_keyboard(),
        )
    else:
        await message.answer(
            "Sizga tegishli tibbiy natija topilmadi.\n"
            "Qaytadan urinish uchun pastdagi tugmani bosing:",
            reply_markup=get_contact_keyboard(),
        )
