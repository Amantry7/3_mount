from aiogram import Bot, Dispatcher,executor,types
from logging import basicConfig, INFO
from config import *
import sqlite3
from aiogram.types import *


connection = sqlite3.connect('client.db')
cursor = connection.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS users(
               id INT,
               username VARCHAR(200),
               first_name VARCHAR(200),
               last_name VARCHAR(200),
               cread VARCHAR(200)
               );""")

cursor.execute("""
                CREATE TABLE IF NOT EXISTS receipt(
                    payment_code int, 
                    first_name VARCHAR(200),
                    last_name VARCHAR(200),
                    direction VARCHAR(200),
                    amount VARCHAR(200),
                    date VARCHAR(200)
                    );
                    """)
bot = Bot(TOKEN)
dp = Dispatcher(bot)
basicConfig(level=INFO)

start_buttons = [
    types.KeyboardButton('o нас'),
    types.KeyboardButton('Адрес'),
    types.KeyboardButton('Контакты'),
    types.KeyboardButton('Курсы'),
    
]
sk = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)


@dp.message_handler(commands=['start'])
async def send_start(message:types.Message):
    await message.answer('Добро пожаловать в Geeks', reply_markup=sk)
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id};")

    connection.commit()

@dp.message_handler(text=['o нас'])
async def send_onas(message:types.Message):
    await message.reply('Geeks это айти курсы в Бишкеке, Карабалте и Оше созданы в 2019')
 

@dp.message_handler(text=['Адрес'])
async def send_фдрес(message:types.Message):
    await message.reply('Наш адрес \nMырзалды Аматова 1B (БЙ темирис)')  
    await message.answer_location(40.51962150364045, 72.80315285125309) 
    
    
@dp.message_handler(text=['Контакты'])
async def send_kantek(message:types.Message):
    await message.reply('наши контакты')
    await message.reply_contact("+996500102907", 'Aman', 'Omurzakov')

cb = [
    types.KeyboardButton('Backent'),
    types.KeyboardButton('Frontend'),
    types.KeyboardButton('UX/UI'),
    types.KeyboardButton('Android'), 
    types.KeyboardButton('Назад')
   
]
ck = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*cb)



@dp.message_handler(text=['Курсы'])
async def send_kyrs(message:types.Message):
    await message.reply('Наши курсы',reply_markup=ck)
    
    
    
@dp.message_handler(text=['Назад'])
async def send_nazad(message:types.Message):
    await send_start(message)
    
    
@dp.message_handler(text=['Backent'])
async def beck(messege:types.Message):
    await messege.answer("Backent - это серверная сторона сайта которую мы не видем ")
 
@dp.message_handler(text=['Frontend'])
async def Frontend(messege:types.Message):
    await messege.answer("Frontend - это лицевая часть сайта которую мы видем ") 
      

@dp.message_handler(text=['UX/UI'])
async def ux(messege:types.Message):
    await messege.answer("UX/UI - это дизайн сайта или приложение  ")
    
@dp.message_handler(text=['Android'])
async def Android(messege:types.Message):
    await messege.answer("Android - это популятрная оперецоная система которую используют многие комнапии ")
executor.start_polling(dp)

