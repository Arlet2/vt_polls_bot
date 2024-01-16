from aiogram import F, types

from main import dp


@dp.message(F.poll)
async def pin_message(message: types.Message):
    await message.pin()
