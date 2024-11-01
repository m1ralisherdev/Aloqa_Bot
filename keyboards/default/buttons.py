from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📔Kurslarim")
        ],
        [
            KeyboardButton(text='🗣Konsultatsiyaga yozilish'),
        ],
        [
            KeyboardButton(text='📚Jinsiy Tarbiya'),
        ],

        [
            KeyboardButton(text="📞Adminga bilan bog'lanish"),
        ],

    ],
    resize_keyboard=True)


Kurslarim = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="Jinsiy Tarbiya"),
        ],
        [
            KeyboardButton(text='Professional kurs'),
        ],
        [
            KeyboardButton(text='Geysha sirlari'),
        ],


    ],
    resize_keyboard=True
)

Konsultatsiya = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1 martalik konsultatsiya"),
        ],
        [
            KeyboardButton(text='Psixoterapiya'),
        ],
        [
            KeyboardButton(text='Vaginizm va unga yechim terapiyasi'),
        ],


    ],
    resize_keyboard=True
)
