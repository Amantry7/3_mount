from aiogram import Bot ,Dispatcher,types,executor
from config import TOKEN
import logging, requests, aioschedule, asyncio


bot = Bot(TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Hi")
    
async def send_message():
    await bot.send_message(-4037053389, "Hello Python")
async def scheduler():
    aioschedule.every(1).seconds.do(send_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
async def on_start(parameter):
    asyncio.create_task(scheduler())
    
executor.start_polling(dp,skip_updates=True, on_startup=on_start)