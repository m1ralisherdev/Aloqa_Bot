
from aiogram import types

from database import cursor, connect
from loader import dp, bot


@dp.message_handler(commands=['reklama'])
async def reklama_command(message: types.Message):
    await message.answer("Iltimos, reklama uchun rasmini yuboring 📸")


@dp.message_handler(content_types=['photo'])
async def reklama_image(message: types.Message):
    photo = message.photo[-1]
    photo_id = photo.file_id
    await message.answer("Rasmdan keyingi ma'lumotlarni kiriting 📝")

    @dp.message_handler(lambda message: True)
    async def reklama_text(message: types.Message):
        text = message.text
        users = cursor.execute("SELECT user_id FROM users_table").fetchall()
        for user in users:
            await bot.send_photo(chat_id=user[0], photo=photo_id, caption=text)

        await message.answer("Reklama muvaffaqiyatli yuborildi!")


@dp.message_handler(commands=['video'])
async def video_command(message: types.Message):
    await message.answer("Iltimos, video noto'ni yuboring 📹")

@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
async def handle_video_note(message: types.Message):
    users = cursor.execute("SELECT user_id FROM users_table").fetchall()
    for user_id in users:
        await bot.send_video_note(chat_id=user_id[0], video_note=message.video_note.file_id)

    await message.answer("Video muvaffaqiyatli yuborildi!")



from datetime import datetime, timedelta

@dp.message_handler(commands=['statistika'])
async def show_statistics(message: types.Message):
    # Hozirgi sanani olish
    today = datetime.now()

    # Bir hafta va bir oy oldingi sanalarni hisoblash
    one_week_ago = today - timedelta(days=7)
    one_month_ago = today - timedelta(days=30)

    # Bir haftada qo'shilganlar sonini hisoblash
    cursor.execute("SELECT COUNT(*) FROM users_table WHERE joined_date >= ?", (one_week_ago.strftime("%Y-%m-%d"),))
    week_count = cursor.fetchone()[0]

    # Bir oyda qo'shilganlar sonini hisoblash
    cursor.execute("SELECT COUNT(*) FROM users_table WHERE joined_date >= ?", (one_month_ago.strftime("%Y-%m-%d"),))
    month_count = cursor.fetchone()[0]

    # Natijani foydalanuvchiga yuborish
    await message.answer(f"Oxirgi 1 hafta ichida qo'shilganlar soni: {week_count}\n"
                         f"Oxirgi 1 oy ichida qo'shilganlar soni: {month_count}")

# Ushbu kodni botga qo'shing va /statistika komandasini chaqirganingizda foydalanuvchilar sonini ko'rasiz.
