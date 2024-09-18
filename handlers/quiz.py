from aiogram import Router, types, F
from aiogram.filters import Command

import config
from main import bot, mongo_connector

router = Router()

quiz_usage = """
Команда /quiz позволяет устраивать опросы прямо в чате!\n
Чтобы создать опрос напишите /quiz <тема опроса>\n
Чтобы оставить ответ, ответьте на сообщение бота с квизом!\n
Чтобы оставить голос за конкретный ответ поставьте реакцию 👍 на ответ"""


def create_poll_message(quiz: dict) -> str:
    return f"quiz: {quiz['name']}\n" + "\n".join([
        f"- {option['name']} " + "👍" * int(option['value'])
        for option
        in sorted(quiz["options"], key=lambda option: option["value"], reverse=True)
    ])


def is_emoji_in_reaction(emoji: str, message_reactions):
    return emoji in map(lambda x: x.emoji, message_reactions)


@router.message(Command("quiz"))
async def quiz_creation(message: types.Message):
    if len(message.text) > config.quiz_theme_max_length:
        await message.reply(f"Название должно быть короче {config.quiz_theme_max_length} символов!")
        return
    quiz_name = message.text[len("/quiz"):].strip()
    if quiz_name == "":
        await message.reply(quiz_usage)
        return
    sent_message = await message.reply(create_poll_message({
        "name": quiz_name,
        "options": []
    }))
    await mongo_connector.create_quiz(message.chat.id, sent_message.message_id, quiz_name)
    await sent_message.pin()


@router.message(F.reply_to_message.text.startswith("quiz:"))
async def quiz_answer(message: types.Message):
    if len(message.text) > config.quiz_answer_max_length:
        await message.reply(f"Ответ должен быть короче {config.quiz_answer_max_length} символов!")
        return
    quiz_answer_text = message.text.strip().rstrip("👍").rstrip()
    if quiz_answer_text == "":
        await message.reply("Ответ должен быть не пустым")
        return
    quiz_message = message.reply_to_message
    if await mongo_connector.is_option_exists(quiz_message.chat.id, quiz_message.message_id, quiz_answer_text):
        await message.reply("Такой вариант ответа уже есть!")
        return
    await mongo_connector.create_quiz_option(message.chat.id,
                                             quiz_message.message_id,
                                             quiz_answer_text,
                                             message.message_id)
    quiz = await mongo_connector.get_quiz_by_quiz_message_id(quiz_message.chat.id, quiz_message.message_id)
    await bot.edit_message_text(create_poll_message(quiz),
                                quiz_message.chat.id,
                                quiz_message.message_id)


@router.message_reaction(F.func(lambda msg: is_emoji_in_reaction("👍", msg.new_reaction))
                         | F.func(lambda msg: is_emoji_in_reaction("👍", msg.old_reaction)))
async def message_reaction_handler(message_reaction: types.MessageReactionUpdated):
    quiz = await mongo_connector.get_quiz_by_answer_message_id(message_reaction.chat.id, message_reaction.message_id)
    if not quiz:
        return
    if is_emoji_in_reaction("👍", message_reaction.new_reaction):
        await mongo_connector.cast_vote(quiz["chat_id"],
                                        quiz["message_id"],
                                        message_reaction.message_id)
    elif is_emoji_in_reaction("👍", message_reaction.old_reaction):
        await mongo_connector.retract_vote(quiz["chat_id"],
                                           quiz["message_id"],
                                           message_reaction.message_id)
    quiz = await mongo_connector.get_quiz_by_quiz_message_id(quiz["chat_id"],
                                                             quiz["message_id"])
    await bot.edit_message_text(create_poll_message(quiz),
                                quiz["chat_id"],
                                quiz["message_id"])
