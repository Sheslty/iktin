import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

import main
from bot.messages import BotButtons
from dbcontroller.models import TgUserAccount, Manager

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    logging.info(f'User {message.from_user.username}:{message.from_user.id} start / restart chat')
    keyboard = [
        [KeyboardButton(text=BotButtons.AUTHORISE_AS_USER), KeyboardButton(text=BotButtons.AUTHORISE_AS_MANAGER)]
    ]
    existing_users = TgUserAccount.select()
    existing_users_ids = [user.tg_id for user in existing_users]
    if message.from_user.id in existing_users_ids:
        user_buttons = [
            [KeyboardButton(text=BotButtons.CONSIGNMENT_CREATE), KeyboardButton(text=BotButtons.CARGO_TRACKING)]
        ]
        keyboard.extend(user_buttons)

    existing_managers = Manager.select()
    existing_manager_ids = [manager.tg_id for manager in existing_managers]
    if message.from_user.id in existing_manager_ids:
        manager_buttons = [
            [KeyboardButton(text=BotButtons.GET_LINKED_USERS)]
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


@router.message(UserAuthorisationForm.waiting_for_password)
async def user_password_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    chosen_password = message.text
    chosen_contract_number = user_data['contract_number']

    user_accounts_creds = main.db.get_user_accounts_creds()
    for (contract_number, password) in user_accounts_creds:
        if chosen_contract_number == contract_number and chosen_password == password:

            await message.answer(
                text=f"Ваш аккаунт связан (пока нет) с ([contract:{chosen_contract_number}]:[password{chosen_password}])"
            )

    await message.answer(
        text=f"Пользовательских аккаунтов с указанными данными ({chosen_contract_number}:{chosen_password}) не найдено"
    )
# -- End User authorize section --


# -- Manager authorize section --
# TODO: спросить у пользователя логин пароль от менеджер-аккаунта
@router.message(F.text == BotButtons.AUTHORISE_AS_MANAGER)
async def process_manager_authorise(message: Message):
    await message.answer("NULL")
# -- End Manager authorize section --
