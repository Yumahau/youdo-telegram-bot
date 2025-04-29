# handlers.py

from aiogram import types
from db import add_task, get_tasks, get_executors
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Регистрация хендлеров
def register_handlers(dp):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(new_task_handler, commands=["new_task"])
    dp.register_message_handler(tasks_handler, commands=["tasks"])
    dp.register_message_handler(send_tasks_handler, commands=["send_tasks"])

# Команда /start
async def start_handler(message: types.Message):
    await message.answer("Привет! Отправь мне новое задание!")

# Команда для создания нового задания
async def new_task_handler(message: types.Message):
    # Пример задания (можно сделать ввод через несколько шагов)
    user_id = message.from_user.id
    username = message.from_user.username
    description = "Задание по ремонту"
    price = 500.0

    # Добавление задания в базу данных
    await add_task(user_id, username, description, price)
    await message.answer("Задание добавлено!")

# Команда для просмотра всех заданий
async def tasks_handler(message: types.Message):
    tasks = await get_tasks()
    if tasks:
        for task in tasks:
            task_info = f"Задание: {task[2]}\nЦена: {task[3]} рублей\n\n"
            await message.answer(task_info)
    else:
        await message.answer("Нет заданий.")

# Команда для рассылки задания исполнителям
async def send_tasks_handler(message: types.Message):
    tasks = await get_tasks()
    if tasks:
        executors = await get_executors()
        for task in tasks:
            task_info = f"Задание: {task[2]}\nЦена: {task[3]} рублей\n\n"
            for executor in executors:
                # Отправка задания каждому исполнителю
                await message.bot.send_message(executor, task_info)
        await message.answer("Задания отправлены всем исполнителям!")
    else:
        await message.answer("Нет заданий для отправки.")
