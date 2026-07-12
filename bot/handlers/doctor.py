import json
import re
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message, ReplyKeyboardRemove

from bot.analysis_types import ANALYSIS_TYPES
from bot.config import DOCTOR_IDS
from bot.database import add_analysis
from bot.keyboards import get_analysis_type_keyboard, get_new_patient_keyboard
from bot.pdf_generator import generate_pdf
from bot.states import DoctorStates

router = Router()
router.message.filter(F.from_user.id.in_(DOCTOR_IDS))
router.callback_query.filter(F.from_user.id.in_(DOCTOR_IDS))

PHONE_PATTERN = re.compile(r"^\+?\d{7,15}$")


async def _start_flow(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Assalomu alaykum, Doktor!\nKerakli analiz turini tanlang:",
        reply_markup=get_analysis_type_keyboard(),
    )


@router.message(CommandStart())
async def doctor_start(message: Message, state: FSMContext) -> None:
    await _start_flow(message, state)


@router.message(Command("add_patient"))
async def doctor_add_patient(message: Message, state: FSMContext) -> None:
    await _start_flow(message, state)


@router.message(Command("cancel"))
async def doctor_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "❌ Bekor qilindi. Qaytadan boshlash uchun /add_patient yuboring.",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.callback_query(F.data == "new_patient")
async def doctor_new_patient(callback: CallbackQuery, state: FSMContext) -> None:
    await _start_flow(callback.message, state)
    await callback.answer()


@router.callback_query(F.data.startswith("analysis:"))
async def doctor_choose_analysis(callback: CallbackQuery, state: FSMContext) -> None:
    analysis_type = callback.data.split(":", 1)[1]
    if analysis_type not in ANALYSIS_TYPES:
        await callback.answer("Noma'lum analiz turi", show_alert=True)
        return

    await state.clear()
    await state.update_data(analysis_type=analysis_type)
    await state.set_state(DoctorStates.waiting_for_full_name)

    info = ANALYSIS_TYPES[analysis_type]
    await callback.message.edit_text(f"✅ Tanlandi: {info['button_label']}")
    await callback.message.answer("Bemorning ism-familiyasini (F.I.SH) kiriting:")
    await callback.answer()


@router.message(DoctorStates.waiting_for_full_name, F.text)
async def doctor_receive_full_name(message: Message, state: FSMContext) -> None:
    full_name = message.text.strip()

    if len(full_name) < 3:
        await message.answer("❌ F.I.SH juda qisqa. Qaytadan kiriting:")
        return

    await state.update_data(full_name=full_name)
    await state.set_state(DoctorStates.waiting_for_birth_date)
    await message.answer("Bemorning tug'ilgan sanasini kiriting (masalan, 15.05.1990):")


@router.message(DoctorStates.waiting_for_full_name)
async def doctor_receive_full_name_invalid(message: Message) -> None:
    await message.answer("❌ Iltimos, F.I.SH ni matn ko'rinishida kiriting.")


@router.message(DoctorStates.waiting_for_birth_date, F.text)
async def doctor_receive_birth_date(message: Message, state: FSMContext) -> None:
    birth_date = message.text.strip()

    try:
        datetime.strptime(birth_date, "%d.%m.%Y")
    except ValueError:
        await message.answer(
            "❌ Sana formati noto'g'ri. Qaytadan kiriting.\nMasalan: 15.05.1990"
        )
        return

    await state.update_data(birth_date=birth_date)
    await state.set_state(DoctorStates.waiting_for_phone)
    await message.answer("Bemorning telefon raqamini kiriting (+998...):")


@router.message(DoctorStates.waiting_for_birth_date)
async def doctor_receive_birth_date_invalid(message: Message) -> None:
    await message.answer(
        "❌ Iltimos, tug'ilgan sanani matn ko'rinishida kiriting.\nMasalan: 15.05.1990"
    )


@router.message(DoctorStates.waiting_for_phone, F.text)
async def doctor_receive_phone(message: Message, state: FSMContext) -> None:
    phone = message.text.strip()

    if not PHONE_PATTERN.match(phone):
        await message.answer(
            "❌ Telefon raqam formati noto'g'ri. Qaytadan kiriting.\nMasalan: +998901234567"
        )
        return

    await state.update_data(phone=phone, field_index=0, results=[])
    await _send_field_prompt(message, state)


@router.message(DoctorStates.waiting_for_phone)
async def doctor_receive_phone_invalid(message: Message) -> None:
    await message.answer(
        "❌ Iltimos, telefon raqamini matn ko'rinishida kiriting.\nMasalan: +998901234567"
    )


async def _send_field_prompt(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    analysis_type = data["analysis_type"]
    fields = ANALYSIS_TYPES[analysis_type]["fields"]
    index = data["field_index"]

    field = fields[index]
    norma_line = f"✅ <b>Norma: {field.norma}</b>\n\n" if field.norma else ""
    await state.set_state(DoctorStates.waiting_for_field_manual_value)
    await message.answer(
        f"📋 {index + 1}/{len(fields)}-qadam\n"
        f"<b>{field.name}</b>\n"
        f"Birlik: {field.unit}\n\n"
        f"{norma_line}"
        f"✏️ Qiymatni kiriting:"
    )


@router.message(DoctorStates.waiting_for_field_manual_value, F.text)
async def doctor_field_manual_value(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    results = data["results"]
    results.append(message.text.strip())
    await state.update_data(results=results, field_index=data["field_index"] + 1)
    await _advance(message, state)


@router.message(DoctorStates.waiting_for_field_manual_value)
async def doctor_field_manual_value_invalid(message: Message) -> None:
    await message.answer("❌ Iltimos, natijani matn ko'rinishida kiriting.")


async def _advance(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    analysis_type = data["analysis_type"]
    fields = ANALYSIS_TYPES[analysis_type]["fields"]

    if data["field_index"] >= len(fields):
        await _finalize(message, state)
    else:
        await _send_field_prompt(message, state)


async def _finalize(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    analysis_type = data["analysis_type"]
    full_name = data["full_name"]
    birth_date = data["birth_date"]
    phone = data["phone"]
    results = data["results"]

    pdf_path = generate_pdf(analysis_type, full_name, birth_date, results)

    fields = ANALYSIS_TYPES[analysis_type]["fields"]
    results_payload = [
        {"code": fields[i].code, "name": fields[i].name, "result": results[i]}
        for i in range(len(fields))
    ]
    await add_analysis(
        phone,
        full_name,
        birth_date,
        analysis_type,
        json.dumps(results_payload, ensure_ascii=False),
        pdf_path,
        message.from_user.id,
    )

    await message.answer(f"✅ Saqlandi va PDF yaratildi.\n👤 {full_name}\n📞 {phone}")
    await message.answer_document(FSInputFile(pdf_path))
    await message.answer(
        "Davom etish uchun tanlang:",
        reply_markup=get_new_patient_keyboard(),
    )

    await state.clear()
