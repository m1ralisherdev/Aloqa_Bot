from aiogram import Bot

bot = Bot(token='6401855105:AAGUkgOmQzVCt91hsHVwyRyI4ez3V19bx5o')

async def get_chat_id():
    chat = await bot.get_chat('+6gPHUyGB571mOTVi')  # Kanalning username'ini kiritish
    print(chat.id)

# Bu funksiyani asyncio orqali chaqirish mumkin
import asyncio
asyncio.run(get_chat_id())
