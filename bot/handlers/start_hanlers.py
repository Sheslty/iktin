import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext

import main
from bot.massages import BotButtons

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    logging.info(f'User {message.from_user.username}:{message.from_user.id} start / restart chat')
    keyboard = [
        [KeyboardButton(text=BotButtons.AUTHORISE_AS_USER), KeyboardButton(text=BotButtons.AUTHORISE_AS_MANAGER)]
    ]

    # TODO: сделать метод получения id пользователей из db в dbcontroller'e и вызвать тут
    users_ids = main.db.get_users_ids()
    if (message.from_user.id,) in users_ids:
        user_buttons = [
            [KeyboardButton(text=BotButtons.CONSIGNMENT_CREATE), KeyboardButton(text=BotButtons.CARGO_TRACKING)]
        ]
        keyboard.extend(user_buttons)

    # TODO: сделать метод получения id менеджеров из db в dbcontroller'e и вызвать тут
    managers_ids = main.db.get_managers_ids()
    if (message.from_user.id,) in managers_ids:
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


# TODO: спросить у пользователя номер договора и пароль и добавить его таблицу
@router.message(F.text == BotButtons.AUTHORISE_AS_USER)
async def process_user_authorise(message: Message):
    await message.answer("NULL")


# TODO: спросить у пользователя логин пароль от менеджер-аккаунта
@router.message(F.text == BotButtons.AUTHORISE_AS_MANAGER)
async def process_manager_authorise(message: Message):
    await message.answer("NULL")

