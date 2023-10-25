import asyncio
import os
import time

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

dp = Dispatcher()

async def main():
    await dp.start_polling(bot)


@dp.message(F.poll)
async def pin_message(message: types.Message):
    await message.pin()


@dp.message(Command("meow"))
async def meow(message: types.Message):
    await message.answer('meow :3')

@dp.message(Command("shutdown"))
async def meow(message: types.Message):
    if str(message.from_user.id) != os.getenv("FATHER_ID"):
        return
    print("Turning off...")
    await message.answer('turning off....')
    time.sleep(60 * 5)
    print("Turning on...")

if __name__ == '__main__':
    token = os.getenv("VT_POLLS_API_TOKEN")
    if token == "":
        print("empty token")
        exit()
    bot = Bot(token)
    print("Bot was started")
    asyncio.run(main())
