from aiogram import Router

from handlers import bingo, meow, poll, shutdown, warn

router = Router()

router.include_routers(bingo.router,
                       meow.router,
                       poll.router,
                       shutdown.router,
                       warn.router)
