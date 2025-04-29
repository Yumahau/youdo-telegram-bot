from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from db import add_task, get_open_tasks, update_task_status
from config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.utils import executor

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я помогу тебе с поиском и созданием задач.")

@dp.message_handler(commands=['add_task'])
async def add_new_task(message: types.Message):
    task_info = message.text.split(" ", 2)
    if len(task_info) < 3:
        await message.reply("Чтобы создать задание, напишите команду в формате: /add_task цена описание")
        return

    price = task_info[1]
    description = task_info[2]

    await add_task(message.from_user.id, message.from_user.username, description, price)
    await message.reply(f"Задание добавлено! Цена: {price}, Описание: {description}")

@dp.message_handler(commands=['list_tasks'])
async def list_open_tasks(message: types.Message):
    tasks = await get_open_tasks()
    if not tasks:
        await message.reply("Нет открытых заданий.")
        return

    for task in tasks:
        task_message = f"Задание от @{task[1]}: {task[2]}\nЦена: {task[3]} рублей\n"
        await message.reply(task_message)

@dp.message_handler(commands=['take_task'])
async def take_task(message: types.Message):
    task_id = int(message.text.split(" ")[1])

    tasks = await get_open_tasks()
    task = next((t for t in tasks if t[0] == task_id), None)

    if task:
        await update_task_status(task_id, 'in_progress')
        await message.reply(f"Вы взяли задание от @{task[1]}: {task[2]} на сумму {task[3]} рублей.")
    else:
        await message.reply("Задание не найдено.")

@dp.message_handler(commands=['complete_task'])
async def complete_task(message: types.Message):
    task_id = int(message.text.split(" ")[1])

    tasks = await get_open_tasks()
    task = next((t for t in tasks if t[0] == task_id), None)

    if task:
        await update_task_status(task_id, 'completed')
        await message.reply(f"Задание от @{task[1]} выполнено!")
    else:
        await message.reply("Задание не найдено.")

async def on_start():
    await bot.set_webhook("https://your-heroku-app-url.com/webhook")
    await dp.start_polling()

