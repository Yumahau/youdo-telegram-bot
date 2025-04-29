import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from handlers import register_handlers

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def main():
    # Инициализация бота
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрация всех хендлеров
    register_handlers(dp)

    # Запуск long-polling
    await dp.start_polling(bot)

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())
