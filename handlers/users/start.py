import asyncio
import sqlite3
from datetime import datetime

from aiogram import types


from database import cursor, connect
from keyboards.default.buttons import start_menu, Kurslarim, Konsultatsiya
from keyboards.inline.til import narx

from loader import dp, bot



# @dp.message_handler(CommandStart())
# async def bot_start(message: types.Message):
#     #if bor bo`lsa xush kelibsiz botimizga
#     #else til tanlang inline 2 ta button uzbek rus
#     #agar admin  aykana video jo`natsa agar hammaga shu video jo`natilsin
#     #admin /reklama bossa agar avval rasm keyin pastida text kiritsin rasm va caption hammaga bir vaqttda jo`natilsin usernalrni databasedagi idlar orqali jo`natasilar
#     # botda birkunda qo`shilgan  odamlar soni 1 hafta va 1 oyda qancha qo`shilganlar soni bittasa /statistika komandasi orqali ko`rsatilsin
#     #bot gurux uchun birmartalik link yaratsin va faqat 1 ta odam qo`shilsa agar link expire bo`lsin
#dumaloq video  kurslarim / konsultatsiya / pullik kitobim /adinga murojaat qilish /
#
#
#     await message.answer(f"Salom, {message.from_user.full_name}!")

@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    cursor.execute("SELECT * FROM users_table WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        await message.answer(f"Xush kelibsiz, {full_name}!")
    else:
        joined_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO users_table (user_id, full_name, joined_date) VALUES (?, ?, ?)",
                       (user_id, full_name, joined_date))
        connect.commit()
        await message.answer(f"Xush kelibsiz, {full_name}!")

    video_note_id = "DQACAgIAAxkBAAIN62cc4R_66R5xeLb3RZqeD-dnwP-vAAKpVQACdjfpSCfKHuhajvEJNgQ"

    await message.answer_video_note(video_note=video_note_id)

    await message.answer("Quyidagi tugmalardan birini tanlang:", reply_markup=start_menu)

@dp.message_handler(text="📔Kurslarim")
async def handle_kurslarim(message: types.Message):
    await message.answer("Quyidagi tugmalardan birini tanlang:", reply_markup=Kurslarim)


@dp.message_handler(text="Jinsiy Tarbiya")
async def handle_jinsiy_tarbiya(message: types.Message):
    video_note_id = "DQACAgIAAxkBAAIN62cc4R_66R5xeLb3RZqeD-dnwP-vAAKpVQACdjfpSCfKHuhajvEJNgQ"
    await message.answer_video_note(video_note=video_note_id, reply_markup=narx)



@dp.message_handler(text="🗣Konsultatsiyaga yozilish")
async def konsultatsiya(message: types.Message):
    await message.answer("Quyidagi tugmalardan birini tanlang:", reply_markup=Konsultatsiya)







