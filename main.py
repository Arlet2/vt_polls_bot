import asyncio
import os

from aiogram import Bot, Dispatcher, types, F

dp = Dispatcher()

async def main():
    await dp.start_polling(bot)


@dp.message(F.poll)
async def pin_message(message: types.Message):
    await message.pin()

if __name__ == '__main__':
    token = os.getenv("VT_POLLS_API_TOKEN")
    if token == "":
        print("empty token")
        exit()
    bot = Bot(token)
    asyncio.run(main())
