import pandas as pd
import requests
import re
import os
import schedule
from datetime import datetime, time as dt_time
from dotenv import load_dotenv
from time import sleep
from bs4 import BeautifulSoup as bs4

def kabuSearch():
    df = pd.read_excel('kabu_list.xlsx', engine='openpyxl')

    codes = df["code"]

    getPrices = df["getPrice"]

    url = 'https://kabutan.jp/stock/?code='

    for index,code in enumerate(codes):
        full_url = url + str(code)
        res = requests.get(full_url)
        soup = bs4(res.text, "html.parser")
        price_element = soup.find("span", {'class': 'kabuka'})
        price_par = soup.select("#stockinfo_i1 > div.si_i1_2 > dl > dd:nth-child(3) > span")
        price_par_number = re.findall(r'[\d,]+\.?\d*', price_par[0].contents[0])
        company = soup.select("#stockinfo_i1 > div.si_i1_1 > h2")
        if price_element:
            price_text = price_element.text
            price_numbers = re.findall(r'[\d,]+\.?\d*', price_text)
            if price_par_number[0]:
                if 5 < float(price_par_number[0]):
                    # print(f"{company[0].contents[2]}({code})に5%以上の値動きがあります")
                    if price_numbers:
                        price = price_numbers[0].replace(',', '')
                        if 300 <= float(price) - float(getPrices[index]) or -300 >= float(price) - float(getPrices[index]):
                            # print("300円以上の値動きがあります")
                            lineNotify(f"{company[0].contents[2]}({code})に5%以上の値動きがあります。\n300円以上の値動きがあります。\n{full_url}")
                        else:
                            lineNotify(f"{company[0].contents[2]}({code})に5%以上の値動きがあります。\n{full_url}")
                    else:
                        # print(f"価格情報が見つかりませんでした: {code}")
                        lineNotify("プログラムにエラーがあります")
        else:
            # print(f"価格情報が見つかりませんでした: {code}")
            lineNotify("プログラムにエラーがあります")

        print("スクレイビング実行")

def lineNotify(message):
    load_dotenv()
    line_notify_token = os.environ['LINE_TOKEN']
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'{message}'}
    requests.post(line_notify_api, headers = headers, data = data)

def run_scheduled_job():
    now = datetime.now()
    # 現在が平日かつ9時から17時の間であるかをチェック
    if now.weekday() < 5 and dt_time(9, 0) <= now.time() <= dt_time(17, 0):
        kabuSearch()

schedule.every(1).minutes.do(run_scheduled_job)
    
while(True):
    schedule.run_pending()
    sleep(1)
