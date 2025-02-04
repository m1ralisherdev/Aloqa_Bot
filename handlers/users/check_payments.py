import asyncio
from aiogram import types
from ..payments.payme import check_transactions
from loader import dp, bot
from aiogram.types import *
from data.config import CHANNEL_ID
from datetime import datetime, timedelta
from database import get_name_user,add_payment_data


@dp.callback_query_handler(lambda a: a.data.startswith('checkid_'),state="*")
async def send_link_channel(call: types.CallbackQuery):
    check_id = call.data.split('_')[1]
    status_payment = check_transactions(check_id=check_id)
    tolandi_btn = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("✅ To'landi", callback_data="pay_success")
    tolandi_btn.add(btn1)

    if await get_name_user(call.from_user.id) is not None:
        user_name = await get_name_user(call.from_user.id)
    else:
        user_name = call.from_user.first_name

    if status_payment:
        joined_date = datetime.now()
        lefted_date = joined_date + timedelta(days=20)
        await add_payment_data(user_name,call.from_user.id,check_id,joined_date,lefted_date)
        await call.message.edit_reply_markup(reply_markup=tolandi_btn)
        link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            expire_date=datetime.now() + timedelta(days=10),
            member_limit=1,
            name=user_name
        )
        await bot.send_message(chat_id=call.from_user.id,text=f"Kanalga ulanish uchun havola:\n{link.invite_link}")
        await asyncio.sleep(10 * 24 * 60 * 60)  # 10 kun (soniyalarda)
        try:
            await bot.ban_chat_member(CHANNEL_ID, call.from_user.id)  # Foydalanuvchini chiqarib yuborish
            await bot.unban_chat_member(CHANNEL_ID, call.from_user.id)  # Foydalanuvchini qayta qo‘shish imkoniyatini berish
            channel_name = await bot.get_chat(CHANNEL_ID)
            print(f"Foydalanuvchi {channel_name.title} kanalidan chiqarildi.")
        except Exception as e:
            print(f"Foydalanuvchini chiqarishda xatolik yuz berdi: {e}")

    else:
        await call.answer("❗️ To'lov amalga oshmadi\niltimos to'lab qayta tekshiring !", show_alert=True, cache_time=5)


@dp.callback_query_handler(lambda b: b.data.startswith('pay_success'))
async def show_alert_button(call: types.CallbackQuery):

    await call.answer("✅ To'lov tasdiqlandi", show_alert=True,cache_time=5)