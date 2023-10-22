from aiogram import Router, F
from bot.messages import BotButtons
from aiogram.types import Message
from dbcontroller.models import TgUserAccount, TgManager

router = Router()


def beautiful_list(el: str):
    return f"<li><a href='#'>{el}</a></li>"


@router.message(F.text == BotButtons.GET_USERS_FOR_MANAGER)
async def process_get_users_for_manager(message: Message):
    _id = (TgManager.select(TgManager.id).where(TgManager.tg_id == message.from_user.id))[0]
    users_list = (TgUserAccount.select().where(TgUserAccount.manager_id == _id))
    usernames = [user.tg_username for user in users_list]
    if not usernames:
        answer = "У вас пока нет пользователей"
    else:
        answer = str(usernames)
    await message.answer(answer, parse_mode="HTML")

