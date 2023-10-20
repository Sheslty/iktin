import asyncio
import logging

from aiogram import Bot, Dispatcher
import yaml
from aiogram.fsm.storage.memory import MemoryStorage
# from bot.middlewares import StartMessageMiddleware, OwnerMessageMiddleware, SubscriberMessageMiddleware
# from bot.handlers import owner_handler, start_handler, sub_handler
from dbcontroller.dbcontroller import DataBaseController

DEFAULT_CONFIG = "config.yaml"

db = DataBaseController()

logging.basicConfig(level=logging.INFO)


def parse_config(file):
    with open(file, 'r') as config_file:
        data = yaml.safe_load(config_file)


async def main():
    try:
        config_data = parse_config(DEFAULT_CONFIG)

        db.init()

        bot = Bot(token=token)

        dispatcher = Dispatcher()
        dispatcher.include_routers()

        await dispatcher.start_polling(bot)
        await bot.session.close()

    except Exception as ex:
        logging.exception(ex)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
