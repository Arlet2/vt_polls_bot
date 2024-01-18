import asyncio
import os

from aiogram import Bot, Dispatcher

import handlers

dp = Dispatcher()


async def main():
    token = os.getenv("VT_POLLS_API_TOKEN")
    if token == "":
        print("empty token")
        exit()
    bot = Bot(token)
    print("Bot was started")
    dp.include_routers(handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
