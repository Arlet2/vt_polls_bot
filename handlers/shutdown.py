import os
import time

from aiogram import types
from aiogram.filters import Command

from main import dp


@dp.message(Command("shutdown"))
async def meow(message: types.Message):
    if str(message.from_user.id) != os.getenv("FATHER_ID"):
        return
    print("Turning off...")
    await message.answer('turning off....')
    time.sleep(60 * 5)
    print("Turning on...")
