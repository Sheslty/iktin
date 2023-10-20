import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from bot.handlers.routers_helper import refresh_all_users
from aiogram.fsm.context import FSMContext

import main

from bot.massages import BotButtons

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    logging.info(f'User {message.from_user.username}:{message.from_user.id} start / restart chat')
    default_buttons = [
        [BotButtons.AUTHORISE_AS_USER, BotButtons.AUTHORISE_AS_MAANGER]
    ]
    kb = default_buttons

    # # TODO: сделать метод получения id пользователей из db в dbcontroller'e и вызвать тут
    users_ids =
    if (message.from_user.id,) in users_ids:
        sub_buttons = [
            [KeyboardButton(text=BotButtons.DAYS_TO_EXPIRE), KeyboardButton(text=BotButtons.RENEW_SUBSCRIPTION)]
        ]
        kb.extend(sub_buttons)
    #
    # # TODO: сделать метод получения id менеджеров из db в dbcontroller'e и вызвать тут
    # managers_ids =
    # if (message.from_user.id,) in managers_ids:
    #     user_data = await state.get_data()
    #     await refresh_all_users(main.db, user_data['session_data'])
    #     manager_ = [
    #
    #     ]
    #     kb.extend(manager_)

    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите действие.'
    )
    await message.answer("Привет👋. Я бот", reply_markup=keyboard)


# TODO: спросить у пользователя номер договора и пароль и добавить его таблицу
@router.message(F.text == BotButtons.AUTHORISE_AS_USER)
async def process_user_authorise(message: Message, state: FSMContext):
    pass


# TODO:
@router.message(Command("start"))
async def process_manager_authorise(message: Message, state: FSMContext):
    pass

