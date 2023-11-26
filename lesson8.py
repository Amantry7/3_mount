import schedule
import time 
import requests
# def job():
#     print('Working ....', time.ctime())
    
# def notifical_12_2():
#     print('у вас сегондя урок') 


def current():
    url = "https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    respone = requests.get(url=url).json()
    print(respone['price'])
    
def write():
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    respone = requests.get(url=url).json()
    with open('btc.txt', 'a+') as logs:
        logs.write(f"{respone['price']} {time.ctime()} \n")
# schedule.every(3).seconds.do(current)

# file = open("btc.txt", 'w')

schedule.every(1).seconds.do(current)
# schedule.every().saturday.at("13:45").do(job)
# schedule.every().saturday.at("16:31", 'Asia/Bishkek').do(no`tifical_12_2)
# schedule.every(2).seconds.do(job)
# schedule.every(4).seconds.do(notifical_12_2)

while True: 
    schedule.run_pending()
    time.sleep(1)
    