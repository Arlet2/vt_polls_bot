from aiogram import Router

from handlers import shutdown, poll, meow, quiz
from handlers import bingo, warn

router = Router()

router.include_routers(bingo.router,
                       quiz.router,
                       meow.router,
                       poll.router,
                       shutdown.router,
                       warn.router)
