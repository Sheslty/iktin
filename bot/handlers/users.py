from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from datetime import datetime
from aiogram.filters.callback_data import CallbackData
from aiogram_inline_paginations.paginator import Paginator
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Bot

from bot.messages import BotButtons
from datatypes import Package, PretensionStatus
from dbcontroller.models import TgPretension, TgUserAccount, Order, TgManager
import bot.keyboards as keyboards
from bot.keyboards import PretensionCallbacks

from typing import Optional


router = Router()


# --- Start Consignment create section
class PretensionCreateForm(StatesGroup):
    waiting_for_pretension_info = State()

@router.message(F.text == BotButtons.PRETENSION_CREATE)
async def process_pretension_create(message: Message):
    keyboard = keyboards.pretension_type_choose
    await message.answer("Выберите причину претензии", reply_markup=keyboard)


@router.callback_query(F.data.startswith('pretension_'))
async def pretension_type_choose(callback: types.CallbackQuery, state: FSMContext):
    pretension_type = None
    if PretensionCallbacks.PRETENSION_TERM in callback.data:
        pretension_type = "Нарушение сроков доставки"
    elif PretensionCallbacks.PRETENSION_BROKE_ITEM in callback.data:
        pretension_type = "Порча вложения"
    elif PretensionCallbacks.PRETENSION_LOST_ITEM in callback.data:
        pretension_type = "Утеря вложения"
    elif PretensionCallbacks.PRETENSION_BROKE_ITEM in callback.data:
        pretension_type = "Повреждение упаковки"

    await state.update_data(pretension_type=pretension_type)
    await callback.message.answer('Опишите вашу претензию подробнее')
    await state.set_state(PretensionCreateForm.waiting_for_pretension_info)


@router.message(PretensionCreateForm.waiting_for_pretension_info)
async def pretension_info_chosen(message: Message, state: FSMContext):
    managers_data = await state.get_data()
    pretension_type = managers_data['pretension_type']
    pretension_message = message.text

    TgPretension.create(
        user_id=message.from_user.id, status=PretensionStatus.WAIT, _type=pretension_type,
        message=pretension_message, creation_datetime=datetime.now()
    )

    await message.answer("Ваша претензия записана и в ближайшее время будет рассмотрена менеджером.")
# --- End Consignment create section


# --- Start Invoice create section
class InvoiceStates(StatesGroup):
    waiting_for_packages_number = State()
    waiting_for_description = State()
    waiting_for_common_cost = State()
    waiting_for_package_cost = State()
    waiting_for_package_sizes = State()


@router.message(F.text == BotButtons.CREATE_INVOICE)
async def process_create_invoice(message: Message, state: FSMContext):
    keyboard = keyboards.delivery_type_choose
    await message.answer("Выберите режим отправки", reply_markup=keyboard,
                         state=state)


@router.callback_query(F.data.startswith('deliver'))
async def delivery_type(callback: types.CallbackQuery, state: FSMContext):
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
    await state.set_state(InvoiceStates.waiting_for_packages_number)
    await callback.message.answer('Укажите количество посылок',
                                  reply_markup=types.ForceReply())


@router.message(InvoiceStates.waiting_for_packages_number)
async def packages_number(message: Message, state: FSMContext):
    try:
        packages = [Package(None) for _ in range(int(message.text))]
        data = {'packages': packages}
        await state.update_data(data)
        await state.set_state(InvoiceStates.waiting_for_description)
        await message.answer('Введите описание содержание посылок',
                             state=state)
    except ValueError:
        await state.set_state(InvoiceStates.waiting_for_packages_number)
        await message.answer('Количество посылок должно быть числом',
                             state=state)


@router.message(InvoiceStates.waiting_for_description)
async def description(message: Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        for i in range(len(state_data['packages'])):
            state_data['packages'][i].description = message.text
        await state.set_state(InvoiceStates.waiting_for_package_sizes)
        await message.answer('Введите данные о каждой посылки в формате '
                             '"длина-ширина-высота-вес|..."', state=state)
    except Exception as ex:
        await message.answer("Введённые данные некорректны")
        await state.clear()


@router.message(InvoiceStates.waiting_for_package_sizes)
async def package_sizes(message: Message, state: FSMContext):
    try:
        state_data = await state.get_data()
        sizes = message.text.split('|')
        for i in range(len(state_data['packages'])):
            tmp = list(map(int, sizes[i].split('-')))
            state_data['packages'][i].length = tmp[0]
            state_data['packages'][i].width = tmp[1]
            state_data['packages'][i].height = tmp[2]
            state_data['packages'][i].weight = tmp[3]
        await state.set_state(InvoiceStates.waiting_for_common_cost)
        await message.answer('Введите общую стоимость', state=state)

    except Exception as ex:
        await message.answer("Введённые данные некорректны")
        await state.clear()

@router.message(InvoiceStates.waiting_for_common_cost)
async def common_cost(message: Message, state: FSMContext):
    try:
        cost = int(message.text)
        await state.update_data({'common_cost': cost})
        await state.set_state(InvoiceStates.waiting_for_package_cost)
        await message.answer('Введите стоимость каждой посылки в формате '
                             'стоимость|..."', state=state)

    except Exception as ex:
        await message.answer("Введённые данные некорректны")
        await state.clear()


@router.message(InvoiceStates.waiting_for_package_cost)
async def common_cost(message: Message, state: FSMContext):
    state_data = await state.get_data()
    sizes = list(map(int, message.text.split('|')))
    for i in range(len(state_data['packages'])):
        state_data['packages'][i].cost = sizes[i]
    # TODO: keyboard payment
    keyboard = keyboards.payment_type_choose
    await message.answer("Выберите способ оплаты", reply_markup=keyboard,
                         state=state)


@router.callback_query(F.data.startswith('payment'))
async def way_of_payment(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    way_of_payment = "Оплата получателем"
    if "payment_contract" in callback.data:
        way_of_payment = "Оплата по договору"

    common_cost = state_data['common_cost']
    packages = state_data['packages']
    message = str(packages) + f"Общая цена {common_cost}"
    await callback.message.answer(message)
    await state.clear()

# --- End Invoice create section


class OrderCallbackFactory(CallbackData, prefix='orders'):
    name: str
    longitude: Optional[float] = None
    latitude: Optional[float] = None


@router.message(F.text == BotButtons.CARGO_TRACKING)
async def process_cargo_tracking(message: Message, state: FSMContext):
    user_id = TgUserAccount.get(tg_id=message.from_user.id).user_id
    order_list = Order.select().where(Order.user_id == user_id)
    builder = InlineKeyboardBuilder()

    for el in order_list:
        builder.button(text=f"№{el.id}, '{el.name[:20]}'",
                       callback_data=OrderCallbackFactory(name=el.name[:15],
                                                          longitude=el.longitude,
                                                          latitude=el.latitude))

    builder.adjust(1)
    paginator = Paginator(data=builder.as_markup(), size=5, dp=router)

    await message.answer(
        text='Выберете заказ:',
        reply_markup=paginator()
    )


@router.callback_query(OrderCallbackFactory.filter())
async def callback_location_order(
        callback: types.CallbackQuery,
        callback_data: OrderCallbackFactory,
        bot: Bot
):
    if callback_data.longitude is None or callback_data.latitude is None:
        return await callback.message.answer(f"У данного товара не указана локация")
    await bot.send_location(callback.message.chat.id,
                            longitude=callback_data.longitude,
                            latitude=callback_data.latitude)
    await callback.message.delete()


@router.message(F.text == BotButtons.START_CHAT_MANAGER)
async def calling_the_manager(message: Message):
    query = (TgUserAccount.select(TgUserAccount.manager_id).where(TgUserAccount.tg_id == message.from_user.id))
    manager = TgManager.get_by_id(query)
    await message.answer(f"Связываем вас с администратором @{manager.tg_username}")

