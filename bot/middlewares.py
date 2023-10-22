from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from datatypes import SessionData
from bot.messages import BotMessages
from dbcontroller.models import TgUserAccount, TgManager


def _is_manager(manager_id):
    manager_ids = TgManager.select()
    existing_managers_ids = [user.tg_id for user in manager_ids]
    if manager_id in existing_managers_ids:
        return True
    return False


def _is_user(user_id):
    user_ids = TgUserAccount.select()
    existing_users_ids = [user.tg_id for user in user_ids]
    if user_id in existing_users_ids:
        return True
    return False


class ManagerMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        manager_id = event.from_user.id
        if _is_manager(manager_id):
            return await handler(event, data)

        await event.answer(BotMessages.NO_PERMISSION)


class UserMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        user_id = event.from_user.id
        if _is_user(user_id):
            return await handler(event, data)

        await event.answer(BotMessages.NO_PERMISSION)
