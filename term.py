'''#notebook 예제
from tkinter import *
import tkinter.ttk
import requests
import xml.etree.ElementTree as ET

# 환율조회
url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
# 공공데이터포털에서 발급받은 디코딩되지 않은 인증키 입력
authkey = "aczTjwLTrbV7vvKgVuQj1Vtb1uLoTepd"
queryParams = {'authkey': authkey, 'searchdate': '2023-05-24', 'data': 'AP01'}

response = requests.get(url, params=queryParams)
print(response.content)
root = ET.fromstring(response.content)


window = Tk()
window.title('tkinter notebook')
notebook = tkinter.ttk.Notebook(window, width=800, height=600)
notebook.pack()

# frame1 = Frame(window)
# notebook.add(frame1, text='페이지1')
# header = ['stnId', 'tmFc', 'wfSv1', 'wn', 'wr']
# 
# for i, col_name in enumerate(header):
#     label = tkinter.Label(frame1, text=col_name, font=("Helvetica", 14, "bold"), borderwidth=1, relief="raised")
#     label.grid(row=i, column=0)
# 
# col_count = 1
# for item in root.iter('item'):
#     stnId = item.findtext('stnId')
#     tmFc = item.findtext("tmFc")
#     wfSv1 = item.findtext("wfSv1")
#     wn = item.findtext("wn")
#     wr = item.findtext("wr")
#     data = [stnId, tmFc, wfSv1, wn, wr]
#     for i, value in enumerate(data):
#         label = tkinter.Label(frame1, text=value, font=("Helvetica", 12), borderwidth=10, relief="ridge")
#         label.grid(row=i, column=col_count)
#     col_count += 1

frame2 = Frame(window)
notebook.add(frame2, text='페이지2')
Label(frame2, text='페이지2의 내용', fg='yellow', font='helvetica 48').pack()

frame3 = Frame(window)
notebook.add(frame3, text='페이지3')
Label(frame3, text='페이지3의 내용', fg='green', font='helvetica 48').pack()

frame4 = Frame(window)
notebook.add(frame4, text='페이지4')
Label(frame4, text='페이지4의 내용', fg='blue', font='helvetica 48').pack()

window.mainloop()
'''
'''
from urllib.request import urlopen
url = ' https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=aczTjwLTrbV7vvKgVuQj1Vtb1uLoTepd&searchdate=20180102&data=AP01'
res_body = urlopen(url).read()
print(res_body.decode('utf-8'))
'''
import requests
import json

url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=aczTjwLTrbV7vvKgVuQj1Vtb1uLoTepd&searchdate=20180102&data=AP01'
response = requests.get(url)
data = response.json()

# Access and print specific elements from JSON data
for item in data:
    currency_code = item['cur_unit']
    currency_name = item['cur_nm']
    exchange_rate = item['deal_bas_r']
    print(f"'''Currency: {currency_name} ({currency_code}), Exchange Rate: {exchange_rate}")

