from aiogram import Router, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

from db import users
from llm import generate_ai_reply

router = Router()

# ---------------- STATES ----------------
class Register(StatesGroup):
    mobile = State()
    name = State()
    year = State()
    dept = State()

# ---------------- KEYBOARDS ----------------
start_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="▶ Start", callback_data="start_bot")]
    ]
)

verify_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📱 Verify Mobile", callback_data="verify_mobile")]
    ]
)

contact_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Share Mobile Number", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True
)

# ---------------- START ----------------
@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Welcome!\nI am your AI Academic Assistant.",
        reply_markup=start_inline_kb
    )

# ---------------- START CALLBACK ----------------
@router.callback_query(F.data == "start_bot")
async def start_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "To continue, please verify your mobile number.",
        reply_markup=verify_inline_kb
    )

# ---------------- VERIFY MOBILE ----------------
@router.callback_query(F.data == "verify_mobile")
async def verify_mobile(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📱 Please share your mobile number",
        reply_markup=contact_kb
    )
    await state.set_state(Register.mobile)

# ---------------- GET MOBILE ----------------
@router.message(Register.mobile, F.contact)
async def get_mobile(message: Message, state: FSMContext):
    mobile = message.contact.phone_number
    await message.delete()

    user = await users.find_one({"mobile": mobile})

    if user:
        msg = await message.answer(
            f"👋 Welcome back, {user['name']}!\n\n"
            "🤖 I can help you with:\n"
            "📅 Timetable\n📝 Exams\n📚 Notes\n🎓 Events",
            reply_markup=ReplyKeyboardRemove()
        )
        await asyncio.sleep(5)
        await msg.delete()
        await state.clear()
        return

    await state.update_data(mobile=mobile)
    await message.answer("Enter your name:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Register.name)

# ---------------- REGISTRATION ----------------
@router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.delete()
    await message.answer("Enter your year:")
    await state.set_state(Register.year)

@router.message(Register.year)
async def get_year(message: Message, state: FSMContext):
    await state.update_data(year=message.text)
    await message.delete()
    await message.answer("Enter your department:")
    await state.set_state(Register.dept)

@router.message(Register.dept)
async def get_dept(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.delete()

    await users.insert_one({
        "mobile": data["mobile"],
        "name": data["name"],
        "year": data["year"],
        "dept": message.text
    })

    msg = await message.answer(
        f"✅ Registration completed!\nWelcome {data['name']} 🎉"
    )
    await asyncio.sleep(5)
    await msg.delete()
    await state.clear()

# ---------------- AI CHAT ----------------
@router.message(F.text & ~F.text.startswith("/"))
async def ai_chat(message: Message):
    user_input = message.text
    await message.delete()

    ai_response = generate_ai_reply(user_input)

    bot_msg = await message.answer(ai_response)
    await asyncio.sleep(6)
    await bot_msg.delete()
