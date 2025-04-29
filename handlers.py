from aiogram import types
from db import get_executors

async def register_handlers(dp):
    @dp.message_handler(commands=['start'])
    async def handle_start(message: types.Message):
        await on_start(message)

    @dp.message_handler(commands=['tasks'])
    async def handle_tasks(message: types.Message):
        await handle_tasks(message)

    @dp.message_handler(commands=['new_task'])
    async def handle_new_task(message: types.Message):
        await handle_new_task(message)
