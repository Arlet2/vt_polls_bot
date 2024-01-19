import asyncio
import os
from itertools import product
from textwrap import wrap

from aiogram import types, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import FSInputFile
from matplotlib import pyplot as plt

router = Router()


class InvalidCommandSyntax(Exception):
    """Raised when usage of command is invalid"""
    pass


message_usage = """
Шаблон для использования команды /bingo:
/bingo [заголовок]
- Клетка 1
- Клетка 2
- Клетка 3

- Клетка 4
- Клетка 5
- Клетка 6

- Клетка 7
- Клетка 8
- Клетка 9

Строки отделяются пустой строкой, на каждой строке должно быть одинаковое количество клеток. 
Максимальная длина фразы в клетке - 50 символов.
Максимальная длина заголовка - 100 символов."""


def create_table(header: str, rows: [[str]], file_name: str):
    if len(header) > 100:
        raise InvalidCommandSyntax
    # header = header.replace(r"$", r"\$")
    column_count, row_count = len(rows), len(rows[0])
    for i, j in product(range(column_count), range(row_count)):
        if len(rows[i][j]) > 50:
            raise InvalidCommandSyntax
        rows[i][j] = '\n'.join(wrap(rows[i][j].replace(r"$", r"\$"), 15))

    fig, ax = plt.subplots()
    ax.set_title(header, fontsize=20)
    ax.set_axis_off()
    table = ax.table(
        cellText=rows,
        cellLoc='center',
        loc='upper left')
    table.scale(row_count // 4 + 1, 7)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for i, j in product(range(column_count), range(row_count)):
        table[i, j].set_text_props(wrap=True)
    plt.savefig(fname=file_name, bbox_inches='tight', dpi=100)
    plt.close(fig)


@router.message(Command("bingo"))
async def bingo(message: types.Message):
    try:
        first_line, body = message.text.split("\n", maxsplit=1)
        header = ""
        if first_line.find(" ") != -1:
            header = first_line[first_line.find(" ") + 1:]
        rows = list(map(lambda l: l.lstrip("- ").split("\n- "), body.split("\n\n")))
        if len(set(map(len, rows))) != 1:  # Check if we have same amount of cells in each row
            raise InvalidCommandSyntax
        file_name = os.path.join("bingo_img", f"{message.chat.id}_{message.from_user.id}.png")
        create_table(header, rows, file_name)
        try:
            await asyncio.wait_for(message.reply_photo(FSInputFile(file_name)), timeout=5)
        finally:
            os.remove(file_name)
        return

    except (InvalidCommandSyntax, ValueError):
        await message.reply(message_usage)
    except (TelegramBadRequest, TimeoutError):
        await message.reply("Бинго слишком велико!")


if __name__ == "__main__":
    create_table("Header1 ",
                 [['Это типичная строка на 50 символов ааааааааааааааа', 'три'] * 2]*4,
                 os.path.join("..", "bingo_img", "test.png"))
