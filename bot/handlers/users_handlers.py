import sqlite3

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import dbcontroller.dbcontroller

router = Router()
