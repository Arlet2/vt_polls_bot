from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command("meow"))
async def meow(message: types.Message):
    await message.answer('meow <3')
