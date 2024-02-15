import asyncio
import os

from aiogram import Bot, Dispatcher

import handlers

dp = Dispatcher()
token = os.getenv("VT_POLLS_API_TOKEN")
if token == "":
    print("empty token")
    exit()
bot = Bot(token)


async def main():
    global bot
    print("Bot was started")
    dp.include_routers(handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
