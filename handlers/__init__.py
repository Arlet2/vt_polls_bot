from aiogram import Router

from handlers import bingo, meow, poll, shutdown, warn, quiz

router = Router()

router.include_routers(bingo.router,
                       quiz.router,
                       meow.router,
                       poll.router,
                       shutdown.router,
                       warn.router)
