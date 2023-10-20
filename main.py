import asyncio
import logging

from aiogram import Bot, Dispatcher
import yaml
from aiogram.fsm.storage.memory import MemoryStorage
# from bot.middlewares import StartMessageMiddleware, OwnerMessageMiddleware, SubscriberMessageMiddleware
from bot.handlers import start_hanlers, users_handlers, managers_handlers
from dbcontroller.dbcontroller import DataBaseController

DEFAULT_CONFIG = "config.yaml"

db = DataBaseController()

logging.basicConfig(level=logging.INFO)


def parse_config(file):
    with open(file, 'r') as config_file:
        data = yaml.safe_load(config_file)

    return data


async def main():
    try:
        config_data = parse_config(DEFAULT_CONFIG)

        db.init()

        bot = Bot(token=config_data['token'])

        dispatcher = Dispatcher()
        dispatcher.include_routers(start_hanlers.router)

        await dispatcher.start_polling(bot)

        # await bot.session.close()

    except Exception as ex:
        logging.exception(ex)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
