from aiogram import Router, types, F
from aiogram.filters import Command

import config
from main import bot

router = Router()


@router.message(Command("quiz"))
async def quiz_creation(message: types.Message):
    if len(message.text) > config.quiz_theme_max_length:
        await message.reply(f"Название должно быть короче {config.quiz_theme_max_length} символов!")
        return
    if message.text.strip() == "":
        await message.reply("Название должно быть не пустым")
        return
    message = await message.reply("quiz: \b" + message.text[5:].strip())
    await message.pin()


@router.message(F.reply_to_message.text.startswith("quiz:"))
async def quiz_answer(message: types.Message):
    if len(message.text) > config.quiz_answer_max_length:
        await message.reply(f"Ответ должен быть короче {config.quiz_answer_max_length} символов!")
        return
    if message.text.strip() == "":
        await message.reply("Ответ должен быть не пустым")
        return
    await bot.edit_message_text(message.reply_to_message.text + "\n - " + message.text,
                                message.chat.id,
                                message.reply_to_message.message_id)

