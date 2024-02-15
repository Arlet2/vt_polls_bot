from aiogram import Router, types, F
from aiogram.filters import Command

from main import bot

router = Router()


@router.message(Command("quiz"))
async def quiz_creation(message: types.Message):
    if len(message.text) > 105:
        await message.reply("Название должно быть короче 100 символов!")
        return
    message = await message.reply("quiz: \b" + message.text[5:])
    await message.pin()


@router.message(F.reply_to_message.text.startswith("quiz: "))
async def quiz_answer(message: types.Message):
    if len(message.text) > 50:
        await message.reply("Ответ должен быть короче 50 символов!")
        return
    await bot.edit_message_text(message.reply_to_message.text + "\n - " + message.text,
                                message.chat.id,
                                message.reply_to_message.message_id)

