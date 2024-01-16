from aiogram import F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from main import dp


warnMarkupBuilder = InlineKeyboardBuilder()
warnMarkupBuilder.add(types.InlineKeyboardButton(
    text="warn",
    callback_data="warn")
)
warnMarkup = warnMarkupBuilder.as_markup()


@dp.message(F.text.startswith('!warn'))
async def warn(message: types.Message):
    command_data = message.text.split(maxsplit=1)
    if len(command_data) != 2:
        await message.reply("использование: !warn <nickname>")
        return
    await message.reply(f"предупреждаем {command_data[1]}? (0/7)",
                        reply_markup=warnMarkup)
