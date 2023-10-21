from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from datatypes import SessionData
from dbcontroller import db_objects_factory


# class StartMessageMiddleware(BaseMiddleware):
#     def __init__(self, session_data: SessionData):
#         self.client_session_data = session_data
#
#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#         event: Message,
#         data: Dict[str, Any]
#     ) -> Any:
#
#         await data['state'].update_data(session_data=self.client_session_data)
#         return await handler(event, data)
