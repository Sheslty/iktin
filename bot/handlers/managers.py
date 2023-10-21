from aiogram import Router, F
from bot.messages import BotButtons
from aiogram.types import Message

router = Router()


@router.message(F.text == BotButtons.GET_USERS_FOR_MANAGER)
async def process_get_users_for_manager(message: Message):
    await message.answer("NULL")

