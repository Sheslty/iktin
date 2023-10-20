import sqlite3

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.massages import BotButtons

import dbcontroller.dbcontroller

router = Router()


@router.message(F.text == BotButtons.AUTHORISE_AS_USER)
async def sub_add(message: Message, state: FSMContext):
    await message.reply(f"Введите username пользователя в телеграм для добавления в подписчики.")
