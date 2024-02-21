from aiogram import Router, types, F
from aiogram.filters import Command

import config
from main import bot, redis

router = Router()

quiz_usage = """
Команда /quiz позволяет устраивать опросы прямо в чате!\n
Чтобы создать опрос напишите /quiz <тема опроса>\n
Чтобы оставить ответ, ответьте на сообщение бота с квизом!\n
Чтобы оставить голос за конкретный ответ поставьте реакцию 👍 на ответ"""

def redis_key_for_quiz_answers(message_id: int, chat_id: int) -> str:
    return f"quiz:{chat_id}:{message_id}"


def redis_key_for_quiz_name(message_id: int, chat_id: int) -> str:
    return f"quiz_name:{chat_id}:{message_id}"


def redis_key_for_answer_data(message_id: int, chat_id: int) -> str:
    return f"quiz_answer:{chat_id}:{message_id}"


def create_poll_message(quiz_name: str, quiz_answers: dict[str, int]) -> str:
    return f"quiz: {quiz_name}\n" + "\n".join([
        f"- {answer} " + "👍" * (int(count) - 1)
        for answer, count
        in sorted(quiz_answers.items(), key=lambda x: x[1], reverse=True)
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
    sent_message = await message.reply(create_poll_message(quiz_name, dict()))
    redis.set(redis_key_for_quiz_name(sent_message.message_id, sent_message.chat.id),
              quiz_name)
    await sent_message.pin()


@router.message(F.reply_to_message.text.startswith("quiz:"))
async def quiz_answer(message: types.Message):
    if len(message.text) > config.quiz_answer_max_length:
        await message.reply(f"Ответ должен быть короче {config.quiz_answer_max_length} символов!")
        return
    quiz_answer_text = message.text.strip()
    if quiz_answer_text == "":
        await message.reply("Ответ должен быть не пустым")
        return
    quiz_message = message.reply_to_message
    if not redis.exists(redis_key_for_quiz_name(quiz_message.message_id, quiz_message.chat.id)):
        await message.reply("Ошибка на сервере(, обратитесь к администратору")
        return
    if redis.hset(redis_key_for_quiz_answers(quiz_message.message_id, quiz_message.chat.id),
                  quiz_answer_text,
                  1) == 0:
        await message.reply("Такой вариант ответа уже есть!")
        return
    quiz_name = redis.get(redis_key_for_quiz_name(quiz_message.message_id, quiz_message.chat.id))
    quiz_answers = redis.hgetall(redis_key_for_quiz_answers(quiz_message.message_id, quiz_message.chat.id))
    redis.hset(redis_key_for_answer_data(message.message_id, message.chat.id),
               mapping={
                   "message_id": message.reply_to_message.message_id,
                   "quiz_answer": quiz_answer_text
               })
    await bot.edit_message_text(create_poll_message(quiz_name, quiz_answers),
                                message.chat.id,
                                message.reply_to_message.message_id)


@router.message_reaction(F.func(lambda msg: redis.exists(redis_key_for_answer_data(msg.message_id, msg.chat.id)))
                         & (F.func(lambda msg: is_emoji_in_reaction("👍", msg.new_reaction))
                            | F.func(lambda msg: is_emoji_in_reaction("👍", msg.old_reaction))))
async def message_reaction_handler(message_reaction: types.MessageReactionUpdated):
    message_id = redis.hget(redis_key_for_answer_data(message_reaction.message_id, message_reaction.chat.id),
                            "message_id")
    quiz_answer = redis.hget(redis_key_for_answer_data(message_reaction.message_id, message_reaction.chat.id),
                             "quiz_answer")
    if is_emoji_in_reaction("👍", message_reaction.new_reaction):
        redis.hincrby(
            redis_key_for_quiz_answers(message_id, message_reaction.chat.id),
            quiz_answer,
            1
        )
    elif is_emoji_in_reaction("👍", message_reaction.old_reaction):
        redis.hincrby(
            redis_key_for_quiz_answers(message_id, message_reaction.chat.id),
            quiz_answer,
            -1
        )
    quiz_name = redis.get(redis_key_for_quiz_name(message_id, message_reaction.chat.id))
    quiz_answers = redis.hgetall(redis_key_for_quiz_answers(message_id, message_reaction.chat.id))
    await bot.edit_message_text(create_poll_message(quiz_name, quiz_answers),
                                message_reaction.chat.id,
                                message_id)
