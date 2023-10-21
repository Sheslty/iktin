import sqlite3

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.messages import BotButtons

import dbcontroller.dbcontroller

router = Router()


# TODO: спросить у пользователя все данные про
@router.message(F.text == BotButtons.CONSIGNMENT_CREATE)
async def process_consignment_create(message: Message, state: FSMContext):
    await message.reply(f"")


# TODO: отслеживание заказа
@router.message(F.text == BotButtons.CONSIGNMENT_CREATE)
async def process_cargo_tracking(message: Message, state: FSMContext):
    await message.reply(f"")
