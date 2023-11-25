from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from config import TOKEN
from aiogram import *
import logging
import sqlite3
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

conn = sqlite3.connect('car_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY,
        car_number TEXT,
        brand TEXT,
        model TEXT,
        year INTEGER
    )
''')
conn.commit()

# additional_cars_data = [
#     ('10BM32', 'Mercedes-Benz', 'E-Class', 2020),
#     ('OO23IU', 'BMW', '5 Series', 2021),
#     ('IKU543', 'Audi', 'A4', 2019),
#     ('677FGH', 'Lexus', 'RX', 2022),
#     ('QWERTY7', 'Tesla', 'Model S', 2021),
#     ('OO777OO', 'Toyota', 'Camry', 2018),
#     ('YUY664', 'Ford', 'Focus', 2020),
#     ('YYTG123', 'Honda', 'Civic', 2019),
#     ('А654ЕТ', 'Nissan', 'Altima', 2021),
#     ('32WASD', 'Chevrolet', 'Malibu', 2017)
# ]

# for car in additional_cars_data:
#     cursor.execute('INSERT INTO cars (car_number, brand, model, year) VALUES (?, ?, ?, ?)', car)

# conn.commit()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Привет! Этот бот предназначен для проверки автомобиля. \n нажмите на /check_car что бы найти машину по номеру ",)

@dp.message_handler(commands=['check_car'])
async def cmd_check_car(message: types.Message):
    await message.answer("Введите номер машины для проверки:")

    dp.register_message_handler(process_car_number)

async def process_car_number(message: types.Message):
    try:
       
        car_number = message.text

      
        cursor.execute("SELECT * FROM cars WHERE car_number=?", (car_number,))
        car_data = cursor.fetchone()

        if car_data:
            car_info = f"Информация о машине:\n"
            car_info += f"Номер машины: {car_data[1]}\n"
            car_info += f"Марка: {car_data[2]}\n"
            car_info += f"Модель: {car_data[3]}\n"
            car_info += f"Год выпуска: {car_data[4]}\n"

            await message.answer(car_info)
        else:
            await message.answer(f"Машина с номером {car_number} не найдена в базе данных.")
    except Exception as e:
        await message.answer("Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.")
        print(f"Error: {e}")
executor.start_polling(dp,skip_updates=True)