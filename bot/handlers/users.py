import sqlite3

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import bot.keyboards as keyboards

from bot.messages import BotButtons

router = Router()


@router.message(F.text == BotButtons.CONSIGNMENT_CREATE)
async def process_consignment_create(message: Message):
    keyboard = keyboards.consignment_type_choose
    await message.answer("Выберите причину претензии", reply_markup=keyboard)


@router.message(F.text == BotButtons.CREATE_INVOICE)
async def process_create_invoice(message: Message, state: FSMContext):
    keyboard = keyboards.delivery_type_choose
    await message.answer("Выберите режим отправки", reply_markup=keyboard,
                         state=state)


@router.callback_query(F.data.startswith('cons_term'))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "term":
        await callback.message.edit_text(f"Бог поможет")
    elif action == "broke_item":
        await callback.message.edit_text(f"Бог поможет")
    elif action == "lost_item":
        await callback.message.edit_text(f"Бог поможет")
    elif action == "broke_box":
        await callback.message.edit_text(f"Бог поможет")

    await callback.answer()


@router.callback_query(F.data.startswith('deliver'))
async def delivery_type_callback(callback: types.CallbackQuery,
                                 state: FSMContext):
    if 'door_door' in callback.data:
        a = state
        await callback.message.edit_text()
    elif 'warehouse_door' in callback.data:
        await callback.message.edit_text(f"Бог поможет")
    elif 'door_warehouse' in callback.data:
        await callback.message.edit_text(f"Бог поможет")
    elif 'warehouse_warehouse' in callback.data:
        await callback.message.edit_text(f"Бог поможет")

    await callback.answer()


# TODO: отслеживание заказа
@router.message(F.text == BotButtons.CONSIGNMENT_CREATE)
async def process_cargo_tracking(message: Message, state: FSMContext):
    await message.reply(f"")
