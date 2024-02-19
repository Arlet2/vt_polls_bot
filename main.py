import asyncio
import os

import redis
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import handlers

load_dotenv()

token = os.getenv("VT_POLLS_API_TOKEN")
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")

if not token or not redis_port or not redis_host:
    print(token)
    print(redis_port)
    print(redis_host)
    print("Put token and redis connection credentials in .env")
    exit(1)


dp = Dispatcher()
bot = Bot(token)
redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


async def main():
    global bot
    print("Bot was started")
    dp.include_routers(handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
