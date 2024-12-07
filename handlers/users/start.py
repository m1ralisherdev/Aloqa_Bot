from datetime import datetime
from pyexpat.errors import messages
from aiogram import types
from aiogram.dispatcher import FSMContext
from marshmallow.fields import Boolean
from database import cursor, connect
from keyboards.default.buttons import start_menu, Kurslarim, Konsultatsiya, contact_button
from keyboards.inline.til import narx, bonus, bonus_2
from utils.for_excel import create_excel
from data.config import ADMINS, CHANNEL_USERNAME, CHANNEL_ID
from aiogram.dispatcher import FSMContext
from aiogram.types import *

from loader import dp, bot

datas = {}

from database import check_user_data, bazaga_qoshish, update_contact
from states.aloqa_states import BotStates


async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        return False


@dp.message_handler(commands='start',state='*')
async def start_bosganda(message: types.Message, state: FSMContext):
    if " " in message.text:
        param = message.text.split(" ", 1)[1]
        if param == 'start':
            await message.answer_photo(open('media/register_foto.jpg', 'rb'), caption="""Vebinarga ro'yxatdan o'tganingiz uchun tashakkur-" Haqiqiy baxtga yetish uchun 5 qadam"!🔥

10-dekabr "Haqiqiy baxtga yetish uchun 5 qadam" Vebinarga  muvaffaqiyatli ro'yxatdan o'tganingiz bilan tabriklayman!🎉

Vebinar 10-dekabr  kuni YouTube da bo'lib o'tadi. Ammo hozircha - "Gaytlik" ni sovg'a sifatida saqlab oling.

Men sizni Vebinar haqida eslatib boraman  ❤️bizni kuzatishda davom eting.

Men sizga efirning boshlanishini eslataman, shuning uchun xatlarimni kuzatib boring va Telegram botini tekshiring.

Agar siz shaxsiy hayotingizda extiros va baxtli munosabatlarni, energiyanga  boy bolishni istasangiz, sizni….. dekabr  kuni Vebinarga ishtirok etishingiz uchun ishonch hosil qiling! 🔥

Sizning bonusingiz sizni bu erda kutmoqda 👇""", reply_markup=bonus_2)
    await message.answer(f"Assalomu Aleykum {message.from_user.first_name}")
    # await message.answer_video_note(video_note=open('media/start_reklama.mp4', "rb"))

    is_subscribed = await check_subscription(message.from_user.id)

    if not is_subscribed:
        await message.answer(
            """<b>Avval telegram kanalga obuna bo'ling 😊
            
Obuna bo'lgandan so'ng esa <code>tekshirish</code> tugmasini bo'sing ✅
            </b>""",
            reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton("Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_USERNAME}"),
                InlineKeyboardButton("Tekshirish", callback_data="check_subscription")
            )
        )
        return
    await process_user_registration(message)


async def process_user_registration(message: types.Message):
    status = await check_user_data(str(message.from_user.id))
    name = cursor.execute("SELECT ism FROM user_full_data WHERE tg_id = ?", (message.from_user.id,)).fetchone()

    if status:
        await message.delete()
        await message.answer(f"Hurmatli {name[0]}, botimizga xush kelibsiz!", reply_markup=start_menu)
    else:
        await message.delete()
        await message.answer("Botda foydalanish uchun ismingizni kiriting", reply_markup=ReplyKeyboardRemove())
        await BotStates.name_state.set()


@dp.callback_query_handler(text="bonus_2")
async def bonus_22(call: types.CallbackQuery):
    await call.message.answer_document(open('media/Intim-xavfsizlik-qoidalari.pdf', 'rb'))


@dp.callback_query_handler(text="check_subscription")
async def check_subscription_callback(call: types.CallbackQuery):
    is_subscribed = await check_subscription(call.from_user.id)

    if is_subscribed:
        await call.message.edit_text("Rahmat! Siz kanalga obuna bo'lgansiz. Endi botdan foydalanishingiz mumkin.")
        await process_user_registration(call.message)
    else:
        await call.answer("Siz hali kanalga obuna bo'lmagansiz. Iltimos, obuna bo'ling!", show_alert=True)


@dp.message_handler(state=BotStates.name_state, content_types=types.ContentTypes.TEXT)
async def name_saver(message: types.Message, state: FSMContext):
    ism = message.text
    user_id = message.from_user.id
    joined_date = message.date
    result = await bazaga_qoshish(ism=ism, tg_id=user_id, joined_data=joined_date)
    if result == Boolean:
        await message.answer("Siz oldin ro`yxatdan o`tgansiz", reply_markup=start_menu)
        await state.finish()
    else:
        await message.answer(result, reply_markup=contact_button)
        await BotStates.contacter.set()


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=BotStates.contacter)
async def xurshid(message: types.Message, state: FSMContext):
    await update_contact(str(message.from_user.id), str(message.contact.phone_number))
    await message.answer("Siz ro`yxatdan o`tdizngiz", reply_markup=types.ReplyKeyboardRemove())
    message_id = await message.answer("Siz uchun bepul kitobimiz taqdim etiladi", reply_markup=bonus)
    datas[message.from_user.id] = message_id.message_id
    await state.finish()


@dp.callback_query_handler(text="bonus")
async def bonus_ssaa(call: types.CallbackQuery):
    await call.bot.send_document(call.message.chat.id, open('media/bonus.pdf', 'rb'), reply_markup=start_menu)
    await bot.delete_message(call.message.chat.id, datas[call.message.chat.id])


@dp.message_handler(text="📔 Kurslarim")
async def handle_kurslarim(message: types.Message):
    await message.answer("Quyidagi tugmalardan birini tanlang:", reply_markup=Kurslarim)


@dp.message_handler(text="Jinsiy Tarbiya")
async def handle_jinsiy_tarbiya(message: types.Message):
    video_note_id = "DQACAgIAAxkBAAIN62cc4R_66R5xeLb3RZqeD-dnwP-vAAKpVQACdjfpSCfKHuhajvEJNgQ"
    await message.answer_video_note(video_note=video_note_id, reply_markup=narx)


@dp.message_handler(text="🗣 Konsultatsiyaga yozilish")
async def konsultatsiya(message: types.Message):
    await message.answer("Quyidagi tugmalardan birini tanlang:", reply_markup=Konsultatsiya)


@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
async def video_note(message: types.Message):
    if message.from_user.id == 433943:
        video_note_id = message.video_note.file_id
        user_id = cursor.execute("SELECT tg_id FROM user_full_data").fetchall()
        for i in user_id:
            for user in i:
                await bot.send_video_note(user, video_note_id)


@dp.message_handler(commands='reklama')
async def reklama(message: types.Message):
    if message.from_user.id == 433943:
        await message.answer_photo(
            open('media/ss.png', 'rb'),
            caption="Reklama rasim yuboring va text yozib qoldiring")
        from states.aloqa_states import BotStates
        await BotStates.reklama_state.set()


@dp.message_handler(state=BotStates.reklama_state, content_types=types.ContentType.PHOTO)
async def handle_photo_with_caption(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    photo_file_id = photo.file_id

    caption = message.caption
    user_id = cursor.execute("SELECT tg_id FROM user_full_data").fetchall()
    for i in user_id:
        for user in i:
            await bot.send_photo(user, photo_file_id, caption=caption)
    await message.reply("Reklama Foydalanuvchiga yuborildi")
    await state.finish()


@dp.message_handler(commands=["video"],state='*')
async def video_handler(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer("Video reklama uchun video yuboring")
        await BotStates.reklame_video.set()


@dp.message_handler(state=BotStates.reklame_video, content_types=ContentType.VIDEO)
async def video_handler(message: Message, state: FSMContext):
    video = message.video
    try:
        if message.caption:
            caption = message.caption
    except:
        for i in ADMINS:
            await bot.send_message(i, f"Reklama jo`natildi Caption {caption}")

    file_id = video.file_id
    await state.finish()
    user_id = cursor.execute("SELECT tg_id FROM user_full_data").fetchall()
    for i in user_id:
        for user in i:
            await bot.send_video(user, file_id,caption=caption)
    await message.answer("Videoni Foydalanuvchilarga yubordim!")


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def reklama_send(message: types.Message):
    users = cursor.execute("SELECT user_id FROM users_table")
    if message.caption is not None:
        caption = message.caption
        photo = message.photo
        for i in range(len(users)):
            await message.answer_photo(caption=caption, photo=photo)
    else:
        await message.answer_photo(
            photo='data:image/jpeg;base64,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',
            caption="Reklama uchun text yozib qoldiring")
        await message.answer("Siz rasm ostida yozuv joylashtirmadingiz")


@dp.message_handler(commands='stats')
async def get_users_data(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await create_excel()

        await message.answer_document(open('users_data.xlsx', 'rb'))
    else:
        await message.answer("Bu faqat adminlar uchun!!!")


@dp.message_handler(text="Siz Baxtli Bo'lasiz 💖")
async def course_answer1(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="⏳ Tez kunda !!!", reply_markup=start_menu)


@dp.message_handler(text="Professional kurs")
async def course_answer1(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="⏳ Tez kunda !!!", reply_markup=start_menu)


@dp.message_handler(text='📚 Jinsiy Tarbiya')
async def course_answer1(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="⏳ Tez kunda !!!")


@dp.message_handler(text="Geysha sirlari")
async def course_answer1(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text="⏳ Tez kunda !!!", reply_markup=start_menu)


@dp.message_handler(lambda message: message.text == "🧕🏻 Men Haqimda")
async def about_me(message: types.Message):
    try:
        with open('media/nadia.jpg', 'rb') as photo:
            await message.answer_photo(photo, caption=(
                """
🌟 Men Nadia Abdullaxodjayeva Abdukadirovna, koʻp yillik tajribaga ega reproduktiv psixologman.
🎓 Toshkent davlat pedagogika universitetida tahsil olganman. Psixologiya yoʻnalishi boʻyicha bakalavr va magistr darajasiga egaman.

📘 Ushbu oliygoh qoshidagi Mutaxassislarni qayta tayyorlash maktabining psixologiya kursida doimiy malaka oshiraman.
💻 Onlayn amaliy psixologiya institutida 1,5 yil davomida amaliy psixologiya va seksologiya yoʻnalishlarida tahsil olganman.

🏫 Hozirda Nadiaʼs School nomli reproduktiv psixologiya maktabiga asos solganman.
⏳ 3000 soatdan ortiq terapevtik kurslar oʻtkazganman.

📚 Asarlarim:
 • “Bepushtlik bilan ogʻrigan ayollarning psixologik xususiyatlari”
 • “Jinsiy tarbiya”
 • “Vaginizmning ilmiy asosi — bu birlamchi bepushtlikka olib keluvchi omil” maqolasi muallifiman.

                """
            ))
    except Exception as e:
        await message.answer(f"Rasm yuklashda xatolik: {e}")


@dp.message_handler(text="📞 Admin bilan bog'lanish")
async def admin_bilan_boglanish(message: types.Message):
    kanal_btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("@nadia_admini", url="https://t.me/@nadia_admini")
            ]
        ]
    )
    await message.answer("Admin bilan bo'glanish", reply_markup=kanal_btn)
