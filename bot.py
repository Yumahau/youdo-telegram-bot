import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from db import init_db, add_task, add_executor, get_executors
from config import BOT_TOKEN

# Инициализация логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def on_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Добавляем пользователя как исполнителя
    await add_executor(user_id)

    await message.answer(f"Привет, {username}! Ты зарегистрирован как исполнитель. Для получения заданий напиши /tasks")

# Хэндлер команды /start
@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    await on_start(message)

# Хэндлер команды /tasks – показывает все доступные задания
@dp.message_handler(commands=['tasks'])
async def handle_tasks(message: types.Message):
    tasks = await get_executors()
    if not tasks:
        await message.answer("Нет доступных заданий.")
    else:
        response = "Доступные задания:\n"
        for task in tasks:
            response += f"Задание ID: {task}\n"
        await message.answer(response)

# Хэндлер для публикации задания
@dp.message_handler(commands=['new_task'])
async def handle_new_task(message: types.Message):
    # Проверим, что это заказчик
    user_id = message.from_user.id
    if user_id not in await get_executors():
        await message.answer("Вы не зарегистрированы как заказчик.")
        return

    task_info = message.text.split(" ", 2)
    if len(task_info) < 3:
        await message.answer("Для создания задания используйте формат: /new_task имя задания описание")
        return

    title = task_info[1]
    description = task_info[2]
    await add_task(user_id, message.from_user.username, title, description)
    await message.answer(f"Задание '{title}' успешно добавлено!")

# Запуск бота
if __name__ == '__main__':
    from handlers import register_handlers
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
