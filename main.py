import asyncio
import os

from aiogram import Bot, Dispatcher

dp = Dispatcher()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    token = os.getenv("VT_POLLS_API_TOKEN")
    if token == "":
        print("empty token")
        exit()
    bot = Bot(token)
    print("Bot was started")
    asyncio.run(main())
