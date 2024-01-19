from aiogram import F, types, Router

router = Router()


@router.message(F.poll)
async def pin_message(message: types.Message):
    await message.pin()
