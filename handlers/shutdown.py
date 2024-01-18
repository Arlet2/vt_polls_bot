import os
import time

from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command("shutdown"))
async def meow(message: types.Message):
    if str(message.from_user.id) != os.getenv("FATHER_ID"):
        return
    print("Turning off...")
    await message.answer('turning off....')
    time.sleep(60 * 5)
    print("Turning on...")
