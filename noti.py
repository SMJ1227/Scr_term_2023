import sys
import time
import json
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

TOKEN = '5903562083:AAHhAOKyZenvr4TQhKYSko9lZLqRM23Cim4'
MAX_MSG_LENGTH = 300
url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=aczTjwLTrbV7vvKgVuQj1Vtb1uLoTepd&searchdate=20230609&data=AP01'
bot = telepot.Bot(TOKEN)

def getData():
    data_list = []
    try:
        response = urlopen(url)
        json_raw = response.read().decode('utf-8')
        json_data = json.loads(json_raw)
        for item in json_data:
            currency_code = item['cur_unit']  # 통화 코드
            currency_name = item['cur_nm']  # 국가/통화명
            exchange_rate = item['deal_bas_r']  # 매매 기준율
            ttb = item['ttb']  # 송금 받을때
            tts = item['tts']  # 송금 보낼때
            data = {
                '통화 코드': currency_code,
                '나라이름 통화명': currency_name.replace(' ', '/'),
                '매매 기준율': exchange_rate,
                '송금 받을때': ttb,
                '송금 보낼때': tts
            }
            data_list.append(data)
        return data_list
    except Exception as e:
        traceback.print_exc()
        print(str(e))


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(param='대한민국'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, param)
        data_list = getData()
        msg = ''
        for r in data_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")' % (user, r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print(str(datetime.now()).split('.')[0], r)
                if len(r + msg)+1 > MAX_MSG_LENGTH:
                    sendMessage(user, msg)
                    msg = r + '\n'
                else:
                    msg += r + '\n'
        if msg:
            sendMessage(user, msg)
    conn.commit()

if __name__ == '__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print('[', today, ']received token :', TOKEN)

    pprint(bot.getMe())

    run(current_month)
