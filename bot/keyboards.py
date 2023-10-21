from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# --- Consignment keyboards section
consignment_type_choose = InlineKeyboardMarkup(inline_keyboard=[
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


# --- Invoice keyboards section
delivery_type_choose = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="дверь-дверь", callback_data="deliver_door_door"),
            InlineKeyboardButton(text="склад-склад", callback_data="deliver_warehouse_door")
        ],
        [
            InlineKeyboardButton(text="склад-дверь", callback_data="deliver_door_warehouse"),
            InlineKeyboardButton(text="дверь-склад", callback_data="deliver_warehouse_warehouse")
        ]
    ]
)

payment_type_choose = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Оплата получателем", callback_data="payment_receiver"),
            InlineKeyboardButton(text="Оплата по договору", callback_data="payment_contract")
        ]
    ]
)
