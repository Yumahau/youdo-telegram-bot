import asyncio
from aiogram import Bot, Dispatcher
from handlers import register_handlers
import os

TOKEN = os.getenv("BOT_TOKEN") or "716023088:AAGpwBdCKZjcFQ21qE7jowaXps2_zIVbVWw"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
