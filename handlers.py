# handlers.py

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from db import add_task, get_all_executors

# Регистрируем хендлеры
def register_handlers(dp: Dispatcher):

    @dp.message_handler(commands=['start'])
    async def start_handler(message: types.Message):
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("📝 Разместить задание", callback_data="client"),
            InlineKeyboardButton("🛠 Я исполнитель", callback_data="executor")
        )
        await message.answer("Привет! Кто ты?", reply_markup=keyboard)

    @dp.callback_query_handler(lambda c: c.data == "executor")
    async def handle_executor(callback_query: types.CallbackQuery):
        user_id = callback_query.from_user.id
        add_task("executors", user_id)  # сохраняем id исполнителя
        await callback_query.message.answer("✅ Вы зарегистрированы как исполнитель!")

    @dp.callback_query_handler(lambda c: c.data == "client")
    async def handle_client(callback_query: types.CallbackQuery):
        await callback_query.message.answer("✍️ Введите описание задания:")
        dp.register_message_handler(get_task, state=None, content_types=types.ContentTypes.TEXT)

    async def get_task(message: types.Message):
        desc = message.text
        add_task("tasks", desc)  # сохраняем задание
        await message.answer("✅ Задание размещено. Сейчас уведомим исполнителей.")

        # Рассылаем задание всем исполнителям
        executors = get_all_executors()
        username = message.from_user.username or "аноним"
        for uid in executors:
            btn = InlineKeyboardMarkup().add(
                InlineKeyboardButton("Откликнуться", callback_data=f"respond_{message.from_user.id}")
            )
            try:
                await message.bot.send_message(
                    uid,
                    f"📢 Новое задание от @{username}:\n\n{desc}",
                    reply_markup=btn
                )
            except Exception as e:
                print(f"Ошибка при отправке пользователю {uid}: {e}")
