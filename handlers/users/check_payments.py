import asyncio
import logging
from aiogram import types
from ..payments.payme import check_transactions
from loader import dp, bot
from aiogram.types import *
from data.config import CHANNEL_ID
from datetime import datetime, timedelta
from database import get_name_user,add_payment_data
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..payments.payme import create_transactions
from database import get_expired_users,update_payment_data

scheduler = AsyncIOScheduler()

async def remove_user_from_channel(user_id):
    try:
        await update_payment_data(user_id)
        await bot.ban_chat_member(chat_id=CHANNEL_ID, 
                                  user_id=int(user_id),
                                  until_date=datetime.now() + timedelta(seconds=31)
                                  )
        await bot.unban_chat_member(chat_id=CHANNEL_ID,
                                    user_id=user_id)
        
        creating_url = create_transactions()
        pay_button = InlineKeyboardMarkup(row_width=1)
        tolov_btn = InlineKeyboardButton("To'lov", url=creating_url[0])
        check_btn = InlineKeyboardButton("Tekshirish", callback_data=f"checkid_{creating_url[1]}")
        pay_button.add(tolov_btn,check_btn)
        
        await bot.send_message(chat_id=user_id,
                               text="Sizning obuna muddatingiz tugadi. Qayta obuna bo'lish uchun to'lovni amalga oshiring.", reply_markup=pay_button)
        
    except Exception as e:
        logging.error(f"Foydalanuvchini chiqarishda xatolik: {e}")
        
        

async def check_expired_users():
    try:
        expired_users = await get_expired_users(datetime.now())
        print(expired_users)
        for user in expired_users:
            await remove_user_from_channel(user)
    except Exception as e:
        logging.error(f"Xatolik: {e}")
    
    

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
    print(status_payment)
    if status_payment:
        joined_date = datetime.now()
        lefted_date = joined_date + timedelta(days=10)
        await add_payment_data(user_name,call.from_user.id,check_id,joined_date,lefted_date)
        await call.message.edit_reply_markup(reply_markup=tolandi_btn)
        link = await bot.create_chat_invite_link(
            chat_id=CHANNEL_ID,
            expire_date=datetime.now() + timedelta(days=10),
            member_limit=1,
            name=user_name
        )
        await bot.send_message(chat_id=call.from_user.id,text=f"Kanalga ulanish uchun havola:\n{link.invite_link}")
        scheduler.add_job(
            remove_user_from_channel,
            'date',
            run_date=lefted_date,
            args=[call.from_user.id]
        )

    else:
        await call.answer("❗️ To'lov amalga oshmadi\niltimos to'lab qayta tekshiring !", show_alert=True, cache_time=5)


@dp.callback_query_handler(lambda b: b.data.startswith('pay_success'))
async def show_alert_button(call: types.CallbackQuery):

    await call.answer("✅ To'lov tasdiqlandi", show_alert=True,cache_time=5)