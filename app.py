from aiogram import executor
from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.users.check_payments import check_expired_users

async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
    
    scheduler = AsyncIOScheduler()
    scheduler.start()
    
    await check_expired_users()
    
    scheduler.add_job(check_expired_users, "interval", hours=24)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
