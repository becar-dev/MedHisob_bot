import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import BOT_TOKEN
from bot.database import init_db
from bot.handlers.doctor import router as doctor_router
from bot.handlers.patient import router as patient_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    await init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Doktor router user_id DOCTOR_IDS ro'yxatida bo'lganlar uchun ishlaydi,
    # qolgan barcha foydalanuvchilar patient_router orqali xizmat oladi.
    dp.include_router(doctor_router)
    dp.include_router(patient_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
