# from datetime import datetime
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from aiogram import Bot, Dispatcher
# import sqlite3
# import logging
#
# from loader import bot
#
# CHANNEL_ID = '+6gPHUyGB571mOTVi'  # O'zgartiring sizning kanal ID
#
#
#
#
# def connect_db():
#     conn = sqlite3.connect('subscriptions.db')
#     return conn
#
# # Obuna maqomini tekshirish va yangilash funksiyasi
# async def check_subscriptions():
#     conn = connect_db()
#     cursor = conn.cursor()
#     today = datetime.now().date()
#
#     # Faol obunalar bilan foydalanuvchilarni olish
#     cursor.execute("SELECT user_id, left_date FROM subscriptions WHERE status = 'joined'")
#     users = cursor.fetchall()
#
#     for user_id, left_date_str in users:
#         left_date = datetime.strptime(left_date_str, '%Y-%m-%d').date()
#
#         # Agar obuna muddati tugagan bo'lsa
#         if today >= left_date:
#             # Ma'lumotlar bazasida statusni 'left' ga o'zgartirish
#             cursor.execute("UPDATE subscriptions SET status = 'left' WHERE user_id = ?", (user_id,))
#             conn.commit()
#
#             # Foydalanuvchini kanaldan qora ro'yxatga olmasdan chiqarish
#             try:
#                 await bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=user_id, until_date=today)
#                 await bot.unban_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
#                 logging.info(f"Foydalanuvchi {user_id} kanaldan chiqarildi.")
#             except Exception as e:
#                 logging.error(f"Foydalanuvchini {user_id} chiqarishda xato: {e}")
#
#     conn.close()
#
# # Vazifani rejalashtirish
# scheduler = AsyncIOScheduler()
# scheduler.add_job(check_subscriptions, 'interval', days=1)
# scheduler.start()
#
