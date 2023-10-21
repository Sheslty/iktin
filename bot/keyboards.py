from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

consignment_type_choose_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Нарушение сроков доставки", callback_data="cons_term"),
            InlineKeyboardButton(text="Порча вложения", callback_data="cons_broke_item")
        ],
        [
            InlineKeyboardButton(text="Утеря вложения", callback_data="cons_lost_item"),
            InlineKeyboardButton(text="Повреждение упаковки", callback_data="cons_broke_box")
        ]
    ]
)
