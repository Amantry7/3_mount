from bs4 import BeautifulSoup
import requests

def pasind_akipress():
    url = 'https://akipress.org/'
    response = requests.get(url=url)
    print(response)
    soup = BeautifulSoup(response.text,'lxml')
    # print(soup)
    all_nems =soup.find_all('a', class_="newslink")
    n = 0
    print(all_nems)
    for new in all_nems:
        n += 1
        print(f"{n} {new.text}")
        with open('news.txt','a+', encoding='UTF-8') as news_txt: 
            news_txt.write(f"{n} {new.text}\n")
        
# pasind_akipress()

def persing_suplak():
    num = 0
    for page in range(1,7):
        url = 'https://www.sulpak.kg/f/noutbuki?page=page'
        respone = requests.get(url=url)
        # print(respone)
        soup = BeautifulSoup(respone.text,'lxml')
        # print(soup)
        all_laptops = soup.find_all('div', class_='product__item-name' )
        all_price = soup.find_all('div', class_='product__item-price')
        print(all_price)
       
        for laptop, price in zip(all_laptops, all_price):
            num += 1
            print(num,")", laptop.text, "".join(price.text.split()))
        
persing_suplak()

from aiogram import Bot,Dispatcher,executor,types
from config import TOKEN
from bs4 import BeautifulSoup
import logging, os, requests

bot = Bot(TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.info)

@dp.message_handler(commands='start')
async def start(message:types.MEsaсдуфк)

@dp.message_hadler(commads="laptops")
async def send_laptops(message:types.Message):
    num = 0
    for page in range(1,7):
        url = 'https://www.sulpak.kg/f/noutbuki?page={page}'
        respone = requests.get(url=url)
        # print(respone)
        soup = BeautifulSoup(respone.text,'lxml')
        # print(soup)
        all_laptops = soup.find_all('div', class_='product__item-name' )
        all_price = soup.find_all('div', class_='product__item-price')
        print(all_price)
        
        for laptop, price in zip(all_laptops, all_price):
            num += 1
            print(num,")", laptop.text, "".join(price.text.split()))
            await message.answer(f"{num} {laptop.text} {price.text}")
    await message.answer('Все наши ноутбуки')