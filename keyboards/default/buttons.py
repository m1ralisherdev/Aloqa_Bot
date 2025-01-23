from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            # KeyboardButton(text="📔 Kurslarim"),
            KeyboardButton(text='📚 Jinsiy Tarbiya'),
            KeyboardButton(text="📞 Admin bilan bog'lanish"),
        ],
        # [
        #     # KeyboardButton(text='🗣 Konsultatsiyaga yozilish'),
        #     KeyboardButton(text="📞 Admin bilan bog'lanish"),
        # ],
        [
            KeyboardButton(text="📔 Kurslarim"),
            KeyboardButton(text="🧕🏻 Men Haqimda")
        ]
    ],
    resize_keyboard=True)

Kurslarim = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Siz Baxtli Bo'lasiz 💖"),
        ],
        [
            KeyboardButton(text='Professional kurs'),
        ],
        [
            KeyboardButton(text='Ayol Terapiya  (KANAL)'),
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

contact_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('📞 Telefon raqam', request_contact=True)
        ]
    ], resize_keyboard=True
)
