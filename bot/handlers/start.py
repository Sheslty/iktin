import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from peewee import fn, JOIN
from bot.messages import BotButtons
from dbcontroller.models import TgUserAccount, TgManager, UserAccount, Manager

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    logging.info(
        f'User {message.from_user.username}:{message.from_user.id} start / restart chat')
    keyboard = [
        [KeyboardButton(text=BotButtons.AUTHORISE_AS_USER),
         KeyboardButton(text=BotButtons.AUTHORISE_AS_MANAGER)]
    ]
    existing_users = TgUserAccount.select()
    existing_users_ids = [user.tg_id for user in existing_users]
    if message.from_user.id in existing_users_ids:
        user_buttons = [
            [
                KeyboardButton(text=BotButtons.PRETENSION_CREATE),
                KeyboardButton(text=BotButtons.CARGO_TRACKING),
                KeyboardButton(text=BotButtons.CREATE_INVOICE),
                KeyboardButton(text=BotButtons.START_CHAT_MANAGER)
            ]
        ]
        keyboard.extend(user_buttons)

    existing_managers = TgManager.select()
    existing_manager_ids = [manager.tg_id for manager in existing_managers]
    if message.from_user.id in existing_manager_ids:
        manager_buttons = [
            [
                KeyboardButton(text=BotButtons.GET_USERS_FOR_MANAGER),
                KeyboardButton(text=BotButtons.PRETENSIONS_PROCESSING),
            ]
        ]
        keyboard.extend(manager_buttons)

    keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие.'
    )
    await message.answer("Привет👋. Я бот", reply_markup=keyboard)


# -- User authorize section --
class UserAuthorisationForm(StatesGroup):
    waiting_for_contract_number = State()
    waiting_for_password = State()


@router.message(F.text == BotButtons.AUTHORISE_AS_USER)
async def process_user_authorise(message: Message, state: FSMContext):
    await message.reply(f"Введите номер вашего контракта")
    await state.set_state(UserAuthorisationForm.waiting_for_contract_number)


@router.message(UserAuthorisationForm.waiting_for_contract_number)
async def contract_number_chosen(message: Message, state: FSMContext):
    await state.update_data(contract_number=message.text)
    await message.reply(f"Введите пароль")

    await state.set_state(UserAuthorisationForm.waiting_for_password)


def __get_free_manager():
    query = (TgManager
             .select(TgManager.id)
             .join(TgUserAccount, JOIN.LEFT_OUTER)
             .group_by(TgUserAccount.manager_id)
             .order_by(fn.COUNT(TgUserAccount.id)))
    free_managers = [manager for manager in query]

    if len(free_managers):
        return free_managers[0]

    return TgManager.select(TgManager.id).limit(1)


@router.message(UserAuthorisationForm.waiting_for_password)
async def user_password_chosen(message: Message, state: FSMContext):
    try:
        user_data = await state.get_data()
        chosen_password = message.text
        chosen_contract_number = int(user_data['contract_number'])
    except Exception as e:
        await message.answer("Некорректные данные")
        await state.clear()
        return

    free_manager = __get_free_manager()
    user_accounts_creds = UserAccount.select()
    for user in user_accounts_creds:
        if chosen_contract_number == user.contract_number and chosen_password == user.password:
            TgUserAccount.create(tg_id=message.from_user.id, tg_username=message.from_user.username,
                                 user_id=user.id, manager_id=free_manager)
            await message.answer(
                text=f"Ваш аккаунт связан с ([contract:{chosen_contract_number}]:[password:{chosen_password}])"
            )
            await state.clear()
            return

    await message.answer(
        text=f"Пользовательских аккаунтов с указанными данными ({chosen_contract_number}:{chosen_password}) не найдено"
    )
    await state.clear()
    return


# -- End User authorize section --
class ManagerAuthorisationForm(StatesGroup):
    waiting_for_managers_login = State()
    waiting_for_managers_password = State()


# -- Manager authorize section --
@router.message(F.text == BotButtons.AUTHORISE_AS_MANAGER)
async def process_user_authorise(message: Message, state: FSMContext):
    await message.reply(f"Введите логин")
    await state.set_state(ManagerAuthorisationForm.waiting_for_managers_login)


@router.message(ManagerAuthorisationForm.waiting_for_managers_login)
async def manager_login_chosen(message: Message, state: FSMContext):
    await state.update_data(managers_login=message.text)
    await message.reply(f"Введите пароль")

    await state.set_state(ManagerAuthorisationForm.waiting_for_managers_password)


@router.message(ManagerAuthorisationForm.waiting_for_managers_password)
async def manager_password_chosen(message: Message, state: FSMContext):
    try:
        managers_data = await state.get_data()
        chosen_login = managers_data['managers_login']
        chosen_password = message.text
    except Exception as e:
        await message.answer("Некорректные данные")
        await state.clear()
        return

    managers_accounts_creds = Manager.select()
    for manager in managers_accounts_creds:
        if chosen_login == manager.login and chosen_password == manager.password:
            TgManager.create(tg_id=message.from_user.id,
                             tg_username=message.from_user.username,
                             manager_id=manager.id)
            await message.answer(
                text=f"Ваш аккаунт менеджера связан с ([login:{chosen_login}]:[password:{chosen_password}])"
            )
            await state.clear()
            return

    await message.answer(
        text=f"Менеджерских аккаунтов с указанными данными ({chosen_login}:{chosen_password}) не найдено"
    )
    await state.clear()
# -- End Manager authorize section --
