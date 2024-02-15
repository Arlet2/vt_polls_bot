from aiogram import F, types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main import bot

router = Router()

warnMarkupBuilder = InlineKeyboardBuilder()
warnMarkupBuilder.add(types.InlineKeyboardButton(
    text="warn",
    callback_data="warn")
)
warnMarkup = warnMarkupBuilder.as_markup()


@router.message(F.text.startswith('!warn'))
async def warn(message: types.Message):
    command_data = message.text.split(maxsplit=1)
    if len(command_data) != 2:
        await message.reply("использование: !warn <nickname>")
        return
    await message.reply(f"предупреждаем {command_data[1]}? (0/7)",
                        reply_markup=warnMarkup)


@router.callback_query(F.data == 'warn')
async def warn_callback(callback: types.CallbackQuery):
    message = callback.message.text.split('\n')
    users = message[1:]             # get users list
    count = int(message[0][-4])     # get number of votes
    if callback.from_user.first_name not in users:
        message[0] = message[0][:-5] + f"({count + 1}/7)"
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
