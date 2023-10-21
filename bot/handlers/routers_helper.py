import logging

import telethon.errors
from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest

from datatypes import SessionData
from dbcontroller.dbcontroller import DataBaseController
from logging import getLogger
log = getLogger('owner_handler')


async def get_user_id(username, session_data: SessionData):
    async with TelegramClient(
            session_data.session_username,
            session_data.api_id,
            session_data.api_hash) as client:
        try:
            user = await client(GetFullUserRequest(username))
        except telethon.errors.UsernameInvalidError as ex:
            logging.warning(ex)
            raise
        except ValueError as ex:
            logging.error(ex)
            raise
        user_id = user.full_user.id
        return user_id
