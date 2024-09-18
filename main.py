import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import handlers
from dao.MongoConnector import MongoConnector

load_dotenv()

token = os.getenv("VT_POLLS_API_TOKEN")

dp = Dispatcher()
bot = Bot(token)
mongo_connector = MongoConnector()
logging.basicConfig(level=logging.INFO)

async def main():
    global bot
    dp.include_routers(handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
