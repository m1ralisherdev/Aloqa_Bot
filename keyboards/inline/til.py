from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


til = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru")
        ]
    ]
)


narx = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="💳To'lov qilish", callback_data="to'lov")
        ]
    ]
)