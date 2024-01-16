from aiogram import types
from aiogram.filters import Command

from main import dp


@dp.message(Command("meow"))
async def meow(message: types.Message):
    await message.answer('meow :3')
