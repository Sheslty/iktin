from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from datetime import datetime

from bot.messages import BotButtons
from datatypes import Package, PretensionStatus
from dbcontroller.models import TgPretension
import bot.keyboards as keyboards
from bot.keyboards import PretensionCallbacks

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
    waiting_for_cost = State()
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
    state_data = await state.get_data()
    for i in range(len(state_data['packages'])):
        state_data['packages'][i].description = message.text
    await state.set_state(InvoiceStates.waiting_for_package_sizes)
    await message.answer('Введите данные о каждой посылки в формате '
                         '"длина-ширина-высота-вес|..."', state=state)


@router.message(InvoiceStates.waiting_for_package_sizes)
async def package_sizes(message: Message, state: FSMContext):
    state_data = await state.get_data()
    sizes = message.text.split('|')
    for i in range(len(state_data['packages'])):
        tmp = sizes[i].split('-')
        state_data['packages'][i].length = tmp[0]
        state_data['packages'][i].width = tmp[1]
        state_data['packages'][i].height = tmp[2]
        state_data['packages'][i].weight = tmp[3]
    await state.set_state(InvoiceStates.waiting_for_cost)
# --- End Invoice create section

# TODO: отслеживание заказа
@router.message(F.text == BotButtons.PRETENSION_CREATE)
async def process_cargo_tracking(message: Message, state: FSMContext):
    await message.reply(f"")
