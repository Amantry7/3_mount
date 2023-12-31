from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from logging import basicConfig, INFO
import os, requests, re
from config import TOKEN

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer(f"Привет {message.from_user.full_name}, я бот для скачивание видео из тик тока без ваденого знака ")
    await message.answer('Отправте ссылку из тик тока')
@dp.message_handler()
async def get_message_url(message:types.Message):
    if 'tiktok.com' in message.text:
        await message.reply(f"ваша ссылка из тиктока {message.text}")
        input_url = message.text
        respone = requests.get(input_url)
        html_content = respone.text


        video_id_math = re.search(r'"id":"(\d+)"', html_content)

        if video_id_math:
            video_id = video_id_math.group(1)
            print('ID видео найдено: ', video_id )
        else: 
            print("ID не найден")
        video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}').json()
        print(type(video_api))
        video_url = video_api.get("aweme_list")[0].get("video").get("play_addr").get("url_list")[0]
        print(video_url)
        if video_url:
            await message.answer("Скачиваем видео...")
            title_video = video_api.get("aweme_list")[0].get("desc")
            print(title_video)
            try:
                with open(f'video/{title_video}.mp4', 'wb') as video_file:
                    video_file.write(requests.get(video_url).content)
                await message.answer(f"Видео {title_video} успешно скачан :)")
                with open(f'video/{title_video}.mp4', 'rb') as send_video_file:
                    await message.answer_video(send_video_file)
            except Exception as error:
                await message.answer(f"Error: {error}")
    else:
        await message.answer("Неправильная ссылка на видео TikTok")

executor.start_polling(dp, skip_updates=True)