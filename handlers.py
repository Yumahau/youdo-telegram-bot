from aiogram import types
from db import add_task, get_tasks, get_executors
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

@router.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer("Привет! Отправь мне новое задание!")

# Команда для создания задания
@router.message(F.text == "/new_task")
async def new_task_handler(message: types.Message):
    # Пример задания (здесь можно сделать диалог для ввода данных)
    user_id = message.from_user.id
    username = message.from_user.username
    description = "Задание по ремонту"
    price = 500.0

    await add_task(user_id, username, description, price)
    await message.answer("Задание добавлено!")

# Команда для просмотра всех заданий
@router.message(F.text == "/tasks")
async def tasks_handler(message: types.Message):
    tasks = await get_tasks()
    if tasks:
        for task in tasks:
            task_info = f"Задание: {task[2]}\nЦена: {task[3]} рублей\n\n"
            await message.answer(task_info)
    else:
        await message.answer("Нет заданий.")

# Команда для рассылки задания исполнителям
@router.message(F.text == "/send_tasks")
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
