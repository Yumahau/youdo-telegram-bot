from aiogram import Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from db import add_executor, get_executors, add_task

def register_handlers(dp: Dispatcher):
    @dp.message(F.text == "/start")
    async def start_cmd(message: types.Message):
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton("📝 Разместить задание"), KeyboardButton("🛠 Я исполнитель"))
        await message.answer("Привет! Кто ты?", reply_markup=kb)

    @dp.message(F.text == "🛠 Я исполнитель")
    async def reg_exec(message: types.Message):
        await add_executor(message.from_user.id)
        await message.answer("✅ Зарегистрирован как исполнитель.")

    @dp.message(F.text == "📝 Разместить задание")
    async def ask_task(message: types.Message):
        await message.answer("Опиши задание с контактами:")

    @dp.message(lambda msg: len(msg.text) > 20 and any(w in msg.text for w in ["₽", "+7", "тел"]))
    async def save_task(message: types.Message):
        desc = message.text
        username = message.from_user.username or message.from_user.first_name
        await add_task(message.from_user.id, username, desc)

        btn = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton("🟢 Откликнуться", callback_data=f"reply_{message.from_user.id}")]]
        )
        for uid in await get_executors():
            try:
                await message.bot.send_message(uid, f"📢 Новое задание от @{username}:

{desc}", reply_markup=btn)
            except:
                continue
        await message.answer("✅ Задание отправлено исполнителям.")

    @dp.callback_query(F.data.startswith("reply_"))
    async def on_reply(callback: types.CallbackQuery):
        uid = int(callback.data.split("_")[1])
        username = callback.from_user.username or callback.from_user.first_name
        await callback.bot.send_message(uid, f"📩 @{username} откликнулся!")
        await callback.answer("✅ Отклик отправлен.")