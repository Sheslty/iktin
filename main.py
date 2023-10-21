import asyncio
import logging

from aiogram import Bot, Dispatcher
import yaml
from aiogram.fsm.storage.memory import MemoryStorage
#from bot.middlewares import UserMessageMiddleware, ManagerMessageMiddleware
from bot.handlers import start, users, managers

from datatypes import SessionData
from dbcontroller.db_objects_factory import DbObjectsFactory

DEFAULT_CONFIG = "config.yaml"
db_objects_factory = DbObjectsFactory()
logging.basicConfig(level=logging.INFO)


def parse_config(file):
    with open(file, 'r') as config_file:
        data = yaml.safe_load(config_file)

    return data


async def main():
    try:
        config_data = parse_config(DEFAULT_CONFIG)
        db_objects_factory.init()
        bot = Bot(token=config_data['token'])

        session_data = SessionData(session_username=config_data['session_username'],
                                   api_hash=config_data['api_hash'],
                                   api_id=config_data['api_id'])

        # start_middleware = StartMessageMiddleware(session_data)
        # start_handlers.router.message.middleware(start_middleware)

        # user_middleware = UserMessageMiddleware()
        # users_handlers.router.message.middleware(user_middleware)
        #
        # sub_middleware = ManagerMessageMiddleware()
        # managers_handlers.router.message.middleware(sub_middleware)

        storage = MemoryStorage()
        dispatcher = Dispatcher(storage=storage)
        dispatcher.include_routers(start.router, users.router, managers.router)

        await dispatcher.start_polling(bot)

        # await bot.session.close()

    except Exception as ex:
        logging.exception(ex)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
