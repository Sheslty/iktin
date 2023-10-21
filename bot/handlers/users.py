import sqlite3

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.messages import BotButtons

router = Router()


def get_consignment_type_choose_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="Нарушение сроков доставки", callback_data="cons_term"),
            types.InlineKeyboardButton(text="Порча вложения", callback_data="cons_broke_item")
        ],
        [
            types.InlineKeyboardButton(text="Утеря вложения", callback_data="cons_lost_item"),
            types.InlineKeyboardButton(text="Повреждение упаковки", callback_data="cons_broke_box")
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(F.text == BotButtons.CONSIGNMENT_CREATE)
async def process_consignment_create(message: Message):
    keyboard = get_consignment_type_choose_kb()
    await message.answer("Выберите причину претензии", reply_markup=keyboard)


def get_delivery_type():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="дверь-дверь",
                callback_data="deliver_door_door"
            ),
            types.InlineKeyboardButton(
                text="склад-дверь",
                callback_data="deliver_warehouse_door"
            ),
            types.InlineKeyboardButton(
                text="дверь-склад",
                callback_data="deliver_door_warehouse"
            ),
            types.InlineKeyboardButton(
                text="склад-склад",
                callback_data="deliver_warehouse_warehouse"
            )
        ]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(F.text == BotButtons.CREATE_INVOICE)
async def process_create_invoice(message: Message, state: FSMContext):
    keyboard = get_delivery_type()
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
