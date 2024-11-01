import logging
import hashlib
import time
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

TOKEN = '6401855105:AAGUkgOmQzVCt91hsHVwyRyI4ez3V19bx5o'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

ADMIN_CODE = '202413'
admin_users = {1091591701}
admin_chat_id = 1091591701
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
pending_payments = {}
user_tokens = {}

class ConsultationForm(StatesGroup):
    name = State()
    phone_number = State()
    advance_payment = State()
    payment_proof = State()

def generate_token(user_id, course):
    token = hashlib.sha256(f'{user_id}{course}{time.time()}'.encode()).hexdigest()
    user_tokens[token] = {"user_id": user_id, "course": course, "timestamp": time.time()}
    return token

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("👤Men haqimda"))
    keyboard.add(KeyboardButton("📚Kurslar"), KeyboardButton("📝Konsultatsiyaga yozilish"))
    keyboard.add(KeyboardButton("Vaginizm va unga yechim paket"), KeyboardButton("Psixoterapiya"))
    keyboard.add(KeyboardButton("📞Admin"))

    video_note_id = "DQACAgIAAxkBAAIRRWck6YbJa319zK9HcZbbjh9ar-NFAAJDXQACgKgQSUbCVVx8Ne1cNgQ"
    await message.answer_video_note(video_note=video_note_id)
    await message.answer(
        'Assalomu alaykum😊\n\nMening rasmiy Telegram botimga xush kelibsiz! '
        'Bu yerda siz maxsus yopiq kurslar, vebinar va seminarlar uchun toʻlovni amalga oshirishingiz mumkin.\n\n'
        'Oʻzingizga kerakli boʻlimni tanlang⬇️', reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "👤Men haqimda")
async def about_me(message: types.Message):
    try:
        with open('test.jpg', 'rb') as photo:
            await message.answer_photo(photo, caption=(
                "Men Nadia Abdullaxodjayeva Abdukadirovna, koʻp yillik tajribaga ega reproduktiv psixologman...\n"
            ))
    except Exception as e:
        await message.answer(f"Rasm yuklashda xatolik: {e}")

@dp.message_handler(lambda message: message.text == "📚Kurslar")
async def courses(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🔞18+ kurs", callback_data='info_18+ kurs'),
        InlineKeyboardButton("📔Professional kurs", callback_data='info_Professional kurs'),
        InlineKeyboardButton("Geysha Sirlari", callback_data='info_Geysha_sirlari')
    )
    await message.answer("Kursni tanlang:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "📞Admin")
async def admin_contact(message: types.Message):
    await message.answer('Administrator bilan boglanish uchun shu yerga yozing: @nadia_admini\n'
                         'Administrator bilan boglanish uchun telefon raqam: +998 95 049 33 33')

@dp.message_handler(lambda message: message.text == "📝Konsultatsiyaga yozilish")
async def consultations(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("Ro'yxatdan o'tish", callback_data='info_royxatdan_otish'))
    await message.answer("""
Консультациямиз офлайн ва онлайн тарзда болади.

Тулов шартлари:

30 - 40 минут - 790минг сум (1 киши учун)

1 соат - 1.190.000 сум (1 киши учун)

Эр ва Хотинлар учун - 1.390.000 сум 1 соат 

Шартлар:

1 - Исим ва Фамилия
2 - Телефон раками
3 - Олдиндан 50% тулов (офлайн учун) 
4 - Туланган хакида чек
5 - Учрашув манзили хакида келишиб олинади

Кошимча малумот: 

1 - Аванс тулов килингандан кегин, кела ололмасангиз, тулов кайтирилмайди. 

2 - Оффлайн учрашувга кела олмасангиз учрашувдан 2 соат олдин огохлантириш лозим, шунда кабулни бошка кун ва соатга кучириб куямиз!""", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'info_royxatdan_otish')
async def start_registration(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Илтимос, исм ва фамилия киритинг:")
    await ConsultationForm.name.set()

@dp.message_handler(state=ConsultationForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Телефон рақамингизни киритинг:")
    await ConsultationForm.phone_number.set()

@dp.message_handler(state=ConsultationForm.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("To'lov qilish", callback_data='pay_advance'))
    await message.answer("Илтимос, 50% тўловни амалга оширинг:", reply_markup=keyboard)
    await ConsultationForm.advance_payment.set()

@dp.callback_query_handler(lambda c: c.data == 'pay_advance', state=ConsultationForm.advance_payment)
async def ask_for_proof(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Илтимос, тўловни амалга оширганингиз ҳақида чекни юборинг:")
    await ConsultationForm.payment_proof.set()

@dp.message_handler(content_types=['photo'], state=ConsultationForm.payment_proof)
async def process_payment_proof(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id  # Rasm ID sini olish
    await bot.send_photo(chat_id=admin_chat_id, photo=photo_id, caption="Yangi to'lov tasdiqlash uchun.")
    await message.answer("Тўлов чегингиз қабул қилинди. Учрашув манзили ҳақида келишиб олинади.")
    await state.finish()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('info_'))
async def handle_callback_query(query: types.CallbackQuery):
    course = query.data.split('info_')[1]
    keyboard = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("Orqaga", callback_data='back_to_courses'))
    await query.message.answer(f'"{course}" haqida ma\'lumot: {course_info.get(course, "Malumot topilmadi.")}', reply_markup=keyboard)
    await query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back_to_courses')
async def back_to_courses(query: types.CallbackQuery):
    await courses(query.message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
