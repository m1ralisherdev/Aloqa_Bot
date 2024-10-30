from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
import logging
import hashlib
import time
import re

logging.basicConfig(level=logging.INFO)

# Bot tokeni
TOKEN = '6401855105:AAGUkgOmQzVCt91hsHVwyRyI4ez3V19bx5o'
ADMIN_CODE = '202413'
admin_users = {1091591701}
course_links = {
    "18+ kurs": "https://example.com",
    "Professional kurs": "",
    "<<Душа и тело>>": "",
    "<<Vaginizm va unga yechim!>> Psixoterapevtik kurs": ""
}
course_info = {
    "18+ kurs": "18+ kurs haqida ma'lumot",
    "Professional kurs": "Professional kurs haqida ma'lumot",
    "<<Душа и тело>>": "Информация о курсе <<Душа и тело>>",
    "<<Vaginizm va unga yechim!>> Psixoterapevtik kurs": "Vaginizm va unga yechim! kurs haqida ma'lumot"
}
course_payment_terms = {
    "18+ kurs": "",
    "Professional kurs": "",
    "<<Душа и тело>>": ""
}
course_coming_soon = {
    "18+ kurs": "Tez orada.",
    "Professional kurs": "Tez orada.",
    "<<Душа и тело>>": "Tez orada."
}
course_ids = {
    "course1": "18+ kurs",
    "course2": "Professional kurs",
    "course3": "<<Душа и тело>>",
    "course4": "<<Vaginizm va unga yechim!>> Psixoterapevtik kurs"
}
pending_payments = {}
user_tokens = {}
payments = {}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Foydalanuvchiga token yaratish
def generate_token(user_id, course):
    token = hashlib.sha256(f'{user_id}{course}{time.time()}'.encode()).hexdigest()
    user_tokens[token] = {"user_id": user_id, "course": course, "timestamp": time.time()}
    return token

# Tokenni tekshirish
def check_token(token):
    if token in user_tokens:
        return user_tokens[token]
    return None

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("👤Men haqimda"))
    keyboard.add(KeyboardButton("📚Kurslar"))
    keyboard.add(KeyboardButton("📞Admin"))
    await message.answer(
        'Assalomu alaykum😊\n\nMening rasmiy Telegram botimga xush kelibsiz! '
        'Bu yerda siz maxsus yopiq kurslar, vebinar va seminarlar uchun toʻlovni amalga oshirishingiz mumkin.\n\n'
        'Oʻzingizga kerakli boʻlimni tanlang⬇️', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "👤Men haqimda")
async def about_me(message: types.Message):
    try:
        with open('test.jpg', 'rb') as photo:
            await message.answer_photo(photo, caption=(
                "Men Nadia Abdullaxodjayeva Abdukadirovna, koʻp yillik tajribaga ega reproduktiv psixologman.\n\n"
                "Toshkent davlat pedagogika universitetida tahsil olganman. Psixologiya yoʻnalishi boʻyicha "
                "bakalavr va magistr darajasiga egaman.\n\n"
                "Ushbu oliygoh qoshidagi Mutaxassislarni qayta tayyorlash maktabining psixologiya kursida "
                "doimiy malaka oshiraman. Onlayn amaliy psixologiya institutida 1,5 yil davomida amaliy "
                "psixologiya va seksologiya yoʻnalishlarida tahsil olganman.\n\n"
                "Hozirda Nadiaʼs School nomli reproduktiv psixologiya maktabiga asos solganman. "
                "3000 soatdan ortiq terapevtik kurslar oʻtkazganman.\n\n"
                "“Bepushtlik bilan ogʻrigan ayollarning psixologik xususiyatlari”, “Jinsiy tarbiya” kitoblari va "
                "“Vaginizmning ilmiy asosi — bu birlamchi bepushtlikka olib keluvchi omil” maqolasi muallifiman."
            ))
    except Exception as e:
        await message.answer("Rasm yuklashda xatolik: {}".format(e))

@dp.message_handler(lambda message: message.text == "📚Kurslar")
async def courses(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("🔞18+ kurs", callback_data='info_18+ kurs'))
    keyboard.add(InlineKeyboardButton("📔Professional kurs", callback_data='info_Professional kurs'))
    keyboard.add(InlineKeyboardButton("💦<<Душа и тело>> курс", callback_data='info_<<Душа и тело>>'))
    keyboard.add(InlineKeyboardButton("✅<<Vaginizm va unga yechim!>> Psixoterapevtik kurs", callback_data='info_<<Vaginizm va unga yechim!>> Psixoterapevtik kurs'))
    try:
        with open('test.jpg', 'rb') as photo:
            await message.answer_photo(photo, caption='Kursni tanlang:', reply_markup=keyboard)
    except Exception as e:
        await message.answer("Rasm yuklashda xatolik: {}".format(e))

@dp.message_handler(lambda message: message.text == "📞Admin")
async def admin_contact(message: types.Message):
    await message.answer('Administrator bilan boglanish uchun shu yerga yozing: @nadia_admini')
    await message.answer('Administrator bilan boglanish uchun telefon raqam: +998 95 049 33 33')

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('info_'))
async def handle_callback_query(query: types.CallbackQuery):
    course = query.data.split('info_')[1]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Orqaga", callback_data='back_to_courses'))
    await query.message.answer(f'"{course}" haqida ma\'lumot: {course_info.get(course, "Malumot topilmadi.")}', reply_markup=keyboard)
    await query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back_to_courses')
async def back_to_courses(query: types.CallbackQuery):
    await courses(query.message)

@dp.message_handler(content_types=['photo'])
async def photo_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in pending_payments:
        course = pending_payments[user_id]
        payments[user_id] = course
        for admin in admin_users:
            await bot.send_photo(
                admin,
                photo=message.photo[-1].file_id,
                caption=f'Yangi to\'lov tasdiqlash uchun:\nFoydalanuvchi: {message.from_user.full_name}\nKurs: {course}'
            )
        await message.answer('Toʻlov qabul qilindi, tez orada ma\'lumot beramiz.')
        del pending_payments[user_id]
    else:
        await message.answer('Kurs uchun toʻlov qilishni tanlamadingiz.')

# Botni boshlash
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
