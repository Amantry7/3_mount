from config import TOKEN
import random
from aiogram import Bot, Dispatcher,types, executor

bot = Bot(TOKEN)
dp = Dispatcher(bot)

async def on_start(_):
    print("готово")

num = random.randint(1,3)    

@dp.message_handler(commands=['play']) 
async def send_play(message:types.Message): 
    await message.answer("Я загодал число от 1 - 3")  
    
@dp.message_handler(text=['1']) 
async def choic(message:types.Message):  
    
    if num == 1:
        await message.reply('Правильно вы отгодали')
        await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
    elif num != 1:
        await message.reply('Вы не отгадали')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')
     
     
@dp.message_handler(text=['2']) 
async def choic(message:types.Message):  
    global num
    if num == 2:
        await message.reply('Правильно вы отгодали')
        await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
    elif num != 2: 
        await message.reply('Вы не отгадали')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')
         
@dp.message_handler(text=['3']) 
async def choic(message:types.Message):  
    global num
    if num == 3:
        await message.reply('Правильно вы отгодали')
        await message.answer_photo('https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg')
    elif num != 3: 
        await message.reply('Вы не отгадали')
        await message.answer_photo('https://media.makeameme.org/created/sorry-you-lose.jpg')
         
executor.start_polling(dp, on_startup=on_start)
