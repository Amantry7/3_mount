import requests
import schedule
import time

def perform_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('logs.txt', 'a', encoding='utf-8') as file:
            file.write(response.text + '\n')
    else:
        print('ERROR')

def main():
    url = 'https://stopgame.ru/news'
    schedule.every(10).seconds.do(perform_request, url)
    schedule.every(60).seconds.do(perform_request, url)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
