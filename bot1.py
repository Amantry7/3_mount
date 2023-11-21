from aiogram import Bot,Dispatcher,types,executor
from config import TOKEN
import requests, os
import random

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f"Здравструйте {message.from_user.full_name} ")
    await message.answer("Отправьте ссылку видео которую хотите скачать")
# https://www.tiktok.com/@geeks_osh/video/7293896300020403474
# https://www.tiktok.com/@geeks_osh/video/7293896300020403474?is_from_webapp=1&sender_device=pc&web_id=7289042945105217029
# https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id=7285981472740101378



@dp.message_handler(commands='info')
async def info(message: types.Message):
    await message.answer("Подождите немного...")
    get_id_video = message.text.split('?')
    current_id = get_id_video[0].split('/')[5]
    
    video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()
    
    if 'aweme_list' in video_api:
        aweme = video_api['aweme_list'][0]
        desc_video = aweme.get('desc', 'Описание отсутствует')
        author = aweme.get('author', 'Автор неизвестен')
        
        await message.answer(f"Описание: {desc_video}")
        await message.answer(f"Автор: {author}")
    else:
        await message.answer("Не удалось получить информацию о видео.")

@dp.message_handler()
async def dowload_send_video(message: types.Message):
    await message.answer("Скачиваю видео...")
    if 'https://www.tiktok.com' in message.text or 'https://vt.tiktok.com' in message.text:
        await message.answer("Скачать видео")
        try:
            if 'https://www.tiktok.com' in message.text:
                current_id = message.text.split('?')[0].split('/')[5]
            elif 'https://vt.tiktok.com' in message.text:
                current_id = message.text.split('/')[3]
        except IndexError:
            await message.answer("Неправильная ссылка на видео")
            return

        video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()
        video_url = video_api.get('aweme_list')[0].get('video').get('play_addr').get('url_list')[0]
        if video_url:
            title_video = video_api.get('aweme_list')[0].get('desc')

            title_video = ''.join(c for c in title_video if c.isalnum() or c.isspace())

            print("скачиваем видео...")
            try:
                os.makedirs('video', exist_ok=True)
                with open(f'video/{current_id}.mp4', 'wb') as video_file:
                    video_file.write(requests.get(video_url).content)
                print('Видео успешно скачано в папку video')

                # Отправляем видео пользователю
                with open(f'video/{current_id}.mp4', 'rb') as send_file:
                    await message.answer_video(send_file)
            except Exception as error:
                print(f'Ошибка при скачивании видео: {error}')
                await message.answer(f"Ошибка при скачивании видео: {error}")
        else:
            await message.answer("Не удалось получить информацию о видео")
    else:
        await message.answer("Неправильная ссылка на видео")

executor.start_polling(dp)