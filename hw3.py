import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3

from config import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Подключение к базе данных SQLite
conn = sqlite3.connect('bank_bot.db')
cursor = conn.cursor()

# Создание таблицы пользователей, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        balance REAL DEFAULT 0, 
        number_balance INTEGER
    )
''')
conn.commit()

storage = MemoryStorage()
dp.storage = storage

# Клавиатура для команды /start
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/balance')).add(KeyboardButton('/transfer')).add(KeyboardButton('/deposit'))

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        # Если пользователя нет в базе данных, добавь его
        cursor.execute('INSERT INTO users (user_id, username, number_balance) VALUES (?, ?, ?)', (user_id, message.from_user.username, message.from_user.id))
        conn.commit()

    # Формирование чека о пользователе
    user_info = f"Ваш номер счета: {message.from_user.id}\n"
    user_info += f"Никнейм: {message.from_user.username}"

    # Отправка чека о пользователе
    await message.answer(f"Информация о вас .\n\n{user_info}", reply_markup=start_keyboard)

    await message.answer("Привет! Этот бот Оптима банк \n/balance - посмотреть баланс \n/deposit - пополнить баланс \n/transfer - перевести на другой счет", reply_markup=start_keyboard)

@dp.message_handler(commands=['balance'])
async def cmd_balance(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()

    if balance:
        await message.answer(f"Твой текущий баланс: {balance[0]}")
    else:
        await message.answer("У тебя нет счета. Для создания счета используй команду /start")

class DepositState(StatesGroup):
    amount = State()

@dp.message_handler(commands='deposit')
async def cmd_deposit(message: types.Message):
    await message.answer("Введите сумму для пополнения баланса:")
    await DepositState.amount.set()

@dp.message_handler(state=DepositState.amount)
async def deposit_amount(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()[0]

    try:
        amount = float(message.text)
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной.")

        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
        conn.commit()

        await message.answer(f"Баланс успешно пополнен на {amount}")

    except ValueError as e:
        await message.answer(f"Ошибка: {e}")
        await state.finish()

class TransferState(StatesGroup):
    amount = State()
    recipient_balance = State()

@dp.message_handler(commands=['transfer'])
async def transfer_command(message: types.Message):
    await message.answer('Введите сумму перевода:')
    await TransferState.amount.set()

@dp.message_handler(state=TransferState.amount)
async def process_amount(message: types.Message, state: FSMContext):
    amount = float(message.text)
    await state.update_data(amount=amount)
    await message.answer('Введите ID пользователя или номер счета получателя:')
    await TransferState.recipient_balance.set()

@dp.message_handler(state=TransferState.recipient_balance)
async def process_recipient_balance(message: types.Message, state: FSMContext):
    recipient_balance_data = int(message.text)
    data = await state.get_data()
    amount = data.get('amount')
    result = process_transfer(message.from_user.id, recipient_balance_data, amount)

    if result:
        await message.answer('Перевод выполнен успешно!')
        await message.answer(f'Сумма перевода: {amount} руб.')
        await message.answer(f'Получатель: {recipient_balance_data}')
    else:
        await message.answer('Ошибка при выполнении перевода. Пожалуйста, проверьте данные получателя.')

    await state.finish()

def process_transfer(sender_id, recipient_balance_data, amount):
    conn = sqlite3.connect('bank_bot.db')
    cursor = conn.cursor()

    try:
        conn.execute('BEGIN TRANSACTION')

        cursor.execute('SELECT balance FROM users WHERE user_id = ?',
        (sender_id,))
        sender_balance = cursor.fetchone()[0]

        # Check if the sender has sufficient balance
        if sender_balance >= amount:
            # Update sender's balance by subtracting the transfer amount
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, sender_id))

            # Check if the recipient exists
            cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (recipient_balance_data,))
            recipient_exists = cursor.fetchone()

            if recipient_exists:
                # Update recipient's balance by adding the transfer amount
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, recipient_balance_data))

                # Commit the transaction
                conn.execute('COMMIT')

                return True
            else:
                return False  # Recipient not found
        else:
            return False  # Insufficient balance

    except Exception as e:
        # Rollback the transaction in case of an error
        conn.execute('ROLLBACK')
        print(f'Error: {e}')
        return False

    finally:
        # Close the database connection
        conn.close()

# Error handling
async def error_handler(update, exception):
    logging.exception(exception)
    await update.message.reply("Произошла ошибка. Пожалуйста, повторите попытку позже.")

# Start the bot
executor.start_polling(dp, skip_updates=True)
