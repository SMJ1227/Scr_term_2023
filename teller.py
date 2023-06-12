import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback
import noti

def AptData(user):
    data_list = noti.getData()  # getData 함수 호출하여 전체 환율 정보를 가져옴
    if data_list:
        msg = "전체 환율 정보:\n\n"
        for data in data_list:
            msg += f"통화 코드:  {data['통화 코드']}\n"
            msg += f"나라이름/통화명:  {data['나라이름 통화명']}\n"
            msg += f"매매 기준율:  {data['매매 기준율']}\n"
            msg += f"송금 받을때:  {data['송금 받을때']}\n"
            msg += f"송금 보낼때:  {data['송금 보낼때']}\n\n"
        noti.sendMessage(user, msg)  # 전체 환율 정보를 sendMessage 함수를 통해 전송
    else:
        noti.sendMessage(user, '오류')

def findIndex(data_list, loc_param):
    for i, r in enumerate(data_list):
        if loc_param in r['나라이름 통화명']:
            return i
    return -1

def replyAptData(user, loc_param):
    data_list = noti.getData()
    index = findIndex(data_list, loc_param)
    print(index)
    msg = loc_param + '의 환율 정보\n'
    for r in data_list:
        if loc_param in r['나라이름 통화명']:
            msg += '통화 코드: {}\n'.format(r['통화 코드'])
            msg += '나라이름/통화명: {}\n'.format(r['나라이름 통화명'])
            msg += '매매 기준율: {}\n'.format(r['매매 기준율'])
            msg += '송금 받을때: {}\n'.format(r['송금 받을때'])
            msg += '송금 보낼때: {}\n'.format(r['송금 보낼때'])
            break
    if msg:
        noti.sendMessage(user, msg)
    else:
        noti.sendMessage(user, '해당하는 나라 정보를 찾을 수 없습니다.')


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return
    text = msg['text']
    args = text.split(' ')
    if text.startswith('전체환율'):
        print('try to 전체환율')
        AptData(chat_id)
    elif text.startswith('나라') and len(args) > 1:
        print('try to 나라', args[1])
        replyAptData(chat_id, args[1])
    else:
        noti.sendMessage(chat_id, """모르는 명령어입니다.\n
        전체환율\n
        환율 나라\n
        중 하나의 명령을 입력하세요.\n """)

today = date.today()
current_month = today.strftime('%Y%m')

print('[', today, ']received token :', noti.TOKEN)

bot = telepot.Bot(noti.TOKEN)
pprint(bot.getMe())

bot.message_loop(handle)

print('Listening...')

while 1:
    time.sleep(10)
