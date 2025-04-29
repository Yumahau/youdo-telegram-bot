from aiogram import types, F
from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import add_task, get_executors

router = Router()

@router.message(F.text == "/start")
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Разместить задание", callback_data="client")],
        [InlineKeyboardButton(text="🛠 Я исполнитель", callback_data="executor")]
    ])
    await message.answer("Привет! Кто ты?", reply_markup=keyboard)

@router.callback_query(F.data == "executor")
async def handle_executor(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    add_task("executors", user_id)
    await callback.message.answer("✅ Вы зарегистрированы как исполнитель!")

@router.callback_query(F.data == "client")
async def handle_client(callback: types.CallbackQuery):
    await callback.message.answer("✍️ Введите описание задания:")

@router.message()
async def get_task(message: types.Message):
    desc = message.text
    add_task("tasks", desc)
    await message.answer("✅ Задание размещено. Сейчас уведомим исполнителей.")

    executors = get_all_executors()
    username = message.from_user.username or "аноним"
    for uid in executors:
        btn = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Откликнуться", callback_data=f"respond_{message.from_user.id}")]
        ])
        try:
            await message.bot.send_message(
                uid,
                f"📢 Новое задание от @{username}:\n\n{desc}",
                reply_markup=btn
            )
        except Exception as e:
            print(f"Ошибка при отправке пользователю {uid}: {e}")

def register_handlers(dp):
    dp.include_router(router)
