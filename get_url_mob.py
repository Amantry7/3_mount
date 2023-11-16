import requests
import re
respone = requests.get('https://vt.tiktok.com/ZSN5FLHme')
html_content = respone.text


video_id_math = re.search(r'"id":"(\d+)"', html_content)

if video_id_math:
    video_id = video_id_math.group(1)
    print('ID видео найдено: ', video_id )
else: 
    print("ID не найден")
