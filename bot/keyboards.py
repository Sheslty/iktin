from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# --- Consignment keyboards section
class PretensionCallbacks:
    PRETENSION_TERM = "pretension_term"
    PRETENSION_BROKE_ITEM = "pretension_broke_item"
    PRETENSION_LOST_ITEM = "pretension_lost_item"
    PRETENSION_BROKE_BOX = "pretension_broke_box"


pretension_type_choose = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Нарушение сроков доставки", callback_data=PretensionCallbacks.PRETENSION_TERM),
            InlineKeyboardButton(text="Порча вложения", callback_data=PretensionCallbacks.PRETENSION_BROKE_ITEM)
        ],
        [
            InlineKeyboardButton(text="Утеря вложения", callback_data=PretensionCallbacks.PRETENSION_LOST_ITEM),
            InlineKeyboardButton(text="Повреждение упаковки", callback_data=PretensionCallbacks.PRETENSION_BROKE_BOX)
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
