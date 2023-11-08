from aiogram import Bot, Dispatcher,types, executor
from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot)
async def on_start(_):
    print("готово")
@dp.message_handler(commands=["start"])
async def send_start(message:types.Message): 
    await message.answer("Hello мир Привет геекс Python")
    await message.delete()
    
@dp.message_handler(commands=['help'])
async def seng_help(message:types.Message): 
    await message.answer('Чем я  могу помочь ?')  
    await message.delete()  
    
@dp.message_handler(text=["Привет", "привет"])
async def hi(message:types.Message): 
    await message.reply("Привет как ты")

@dp.message_handler(commands=['test'])
async def send_test(message:types.Message): 
    await message.reply('тестовое сообшение')
    await message.answer_location(40.51962150364045, 72.80315285125309) 
    await message.answer_photo('https://www.pravilamag.ru/upload/img_cache/e5a/e5a582538319f19cb8cfef8ff6d0f310_ce_640x427x0x140_cropped_666x444.webp')
    await message.answer_contact('+996500102907', 'аман', 'омурзаков')
executor.start_polling(dp, on_startup=on_start)