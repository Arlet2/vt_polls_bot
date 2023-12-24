import asyncio
import os
import time

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

dp = Dispatcher()


warnMarkupBuilder = InlineKeyboardBuilder()
warnMarkupBuilder.add(types.InlineKeyboardButton(
    text="warn",
    callback_data="warn")
)
warnMarkup = warnMarkupBuilder.as_markup()


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


@dp.message(F.text.startswith('!warn'))
async def warn(message: types.Message):
    command_data = message.text.split(maxsplit=1)
    if len(command_data) != 2:
        await message.reply("использование: !warn <nickname>")
        return
    await message.reply(f"предупреждаем {command_data[1]}? (0/7)",
                        reply_markup=warnMarkup)


@dp.callback_query(F.data == 'warn')
async def warn_callback(callback: types.CallbackQuery):
    message = callback.message.text.split('\n')
    users = message[1:]             # get users list
    count = int(message[0][-4])     # get number of votes
    if callback.from_user.first_name not in users:
        message[0] = message[0][:-5] + f"({count+1}/7)"
        if len(message) == 1:
            message.append("список людей которые его ненавидят:")
        message.append(f"{callback.from_user.first_name}")
        await bot.edit_message_text('\n'.join(message),
                                    callback.message.chat.id,
                                    callback.message.message_id,
                                    reply_markup=warnMarkup if count < 6 else None)
        await callback.answer('спасибо что проголосовали')
    else:
        await callback.answer('вы уже проголосовали')


if __name__ == '__main__':
    token = os.getenv("VT_POLLS_API_TOKEN")
    if token == "":
        print("empty token")
        exit()
    bot = Bot(token)
    print("Bot was started")
    asyncio.run(main())
