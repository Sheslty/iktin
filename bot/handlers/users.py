from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.messages import BotButtons
from datatypes import Package, Item


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
    data = {'delivery_type': None}
    if 'door_door' in callback.data:
        data['delivery_type'] = 'дверь-дверь'
    elif 'warehouse_door' in callback.data:
        data['delivery_type'] = 'склад-дверь'
    elif 'door_warehouse' in callback.data:
        data['delivery_type'] = 'дверь-склад'
    elif 'warehouse_warehouse' in callback.data:
        data['delivery_type'] = 'склад-склад'
    await state.update_data(data)
    buttons = None  # TODO: create new keyboard
    await callback.message.answer('Укажите количество посылок',
                                  reply_markup=buttons, state=state)


@router.callback_query(F.data == 'packages_number')
async def packages_number_callback(callback: types.CallbackQuery,
                                 state: FSMContext):
    try:
        packages_number = int(callback.message.text)
        packages = [Package(None, []) for _ in range(packages_number)]
        data = {'packages': packages}
        await state.update_data(data)
        buttons = None  # TODO: create new keyboard
        await callback.message.answer('Введите описание вложений в посылках',
                                      reply_markup=buttons, state=state)
    except ValueError:
        await callback.message.answer('Количество посылок должно быть числом',
                                      state=state)


@router.callback_query(F.data == 'description')
async def description_callback(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    for package in range(state_data['packages']):
        await callback.message.answer('Введите описание вложений в посылках',
                                      reply_markup=buttons, state=state)
    await state.update_data(data)
    buttons = None  # TODO: create new keyboard
    await callback.message.answer('Введите ',
                                  reply_markup=buttons, state=state)


@router.callback_query(F.data == 'sizes')
async def sizes_callback(callback: types.CallbackQuery, state: FSMContext):
    data = {'description': str(callback.message.text)}
    await state.update_data(data)
    buttons = None  # TODO: create new keyboard
    for place in state:

    await callback.message.answer('Введите габариты вложений',
                                  reply_markup=buttons, state=state)


# TODO: отслеживание заказа
@router.message(F.text == BotButtons.CONSIGNMENT_CREATE)
async def process_cargo_tracking(message: Message, state: FSMContext):
    await message.reply(f"")
