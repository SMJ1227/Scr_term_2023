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
from tkinter import *
import tkinter.ttk

url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=aczTjwLTrbV7vvKgVuQj1Vtb1uLoTepd&searchdate=20230525&data=AP01'
response = requests.get(url)
data = response.json()

# Access and print specific elements from JSON data
data_list = []

for item in data:
    currency_code = item['cur_unit'] # 통화 코드
    currency_name = item['cur_nm'] # 국가/통화명
    exchange_rate = item['deal_bas_r'] # 기준 환율
    ttb = item['ttb'] # 송금 받을때
    tts = item['tts'] # 송금 보낼때
    bkpr = item['bkpr'] # 장부 가격
    data_list.append([currency_name, currency_code, exchange_rate, ttb, tts, bkpr])
    print(f"국가/통화명: {currency_name} ({currency_code}), 기준 환율: {exchange_rate}, 송금 받을때: {ttb}, 송금 보낼때: {tts}")
    # (연환가료율)"yy_efee_r":"0",(10일환가료율)"ten_dd_efee_r":"0",(서울외국환중개기준)"kftc_bkpr":"291","kftc_deal_bas_r":"291.7",

window = Tk()
window.title('환율 검색 프로그램')

notebook = tkinter.ttk.Notebook(window, width=800, height=600)
notebook.pack()

frame1 = Frame(window)
notebook.add(frame1, text='나라별 환율 정보')
col_count = 1

# 통화 정보 출력
for i, currency_info in enumerate(data_list):
    for j, value in enumerate(currency_info):
        label = tkinter.Label(frame1, text=str(value), font=("Helvetica", 12), borderwidth=3, relief="ridge")
        label.grid(row=i, column=j+1)  # j+1을 사용하여 첫 번째 열은 헤더와 겹치지 않도록 설정
col_count += 1

# frame2 = Frame(window)
# notebook.add(frame2, text='페이지2')
# # 구 선택 콤보박스 생성
# selected_con = tkinter.StringVar()
# selected_con.set("한국")  # 초기값 설정
# gu_options = set([data_list[currency_name].split()[1] for hospital in hospitals])
# gu_combo = ttk.Combobox(root, textvariable=selected_gu, values=list(gu_options))
# gu_combo.pack()
# Label(frame2, text='페이지2의 내용', fg='yellow', font='helvetica 48').pack()

frame3 = Frame(window)
notebook.add(frame3, text='페이지3')
Label(frame3, text='페이지3의 내용', fg='green', font='helvetica 48').pack()

frame4 = Frame(window)
notebook.add(frame4, text='페이지4')
Label(frame4, text='페이지4의 내용', fg='blue', font='helvetica 48').pack()

window.mainloop()