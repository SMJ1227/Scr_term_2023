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

url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=aczTjwLTrbV7vvKgVuQj1Vtb1uLoTepd&searchdate=20230526&data=AP01'
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
    #bkpr = item['bkpr'] # 장부 가격
    data_list.append([currency_name, currency_code, exchange_rate, ttb, tts])
    # print(f"국가/통화명: {currency_name} ({currency_code}), 기준 환율: {exchange_rate}, 송금 받을때: {ttb}, 송금 보낼때: {tts}")
    # (연환가료율)"yy_efee_r":"0",(10일환가료율)"ten_dd_efee_r":"0",(서울외국환중개기준)"kftc_bkpr":"291","kftc_deal_bas_r":"291.7",

window = Tk()
window.title('환율 검색 프로그램')

notebook = tkinter.ttk.Notebook(window, width=850, height=600)
notebook.pack()


frame1 = Frame(window)
notebook.add(frame1, text='나라 검색')
Label(frame1, text='나라 검색', fg='green', font='helvetica 48').pack()

frame2 = Frame(window)
notebook.add(frame2, text='나라별 환율 정보')
col_count = 1
header = ['국가/통화명', '통화 코드', '기준 환율', '송금 받을때', '송금 보낼때']

canvas = Canvas(frame2)
scrollbar = Scrollbar(frame2, orient='vertical', command=canvas.yview)
scrollable_frame = Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side='right', fill='y')
canvas.pack(side='left', fill='both', expand=True)

for i, row_name in enumerate(header):
    label = tkinter.Label(scrollable_frame, text=row_name, font=("Helvetica", 14, "bold"), borderwidth=1, relief="raised", width=13, height=2)
    label.grid(row=0, column=i+2)

for i, currency_info in enumerate(data_list):
    for j, value in enumerate(currency_info):
        label = tkinter.Label(scrollable_frame, text=str(value), font=("Helvetica", 12), borderwidth=3, relief="ridge", width=17, height=2)
        label.grid(row=i+1, column=j+2)  # Start from column 2 to avoid overlapping with the header
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
notebook.add(frame3, text='환전하기')
Label(frame3, text='환전액').grid(row=0, column=0, sticky=W)
Label(frame3, text='기준 환율').grid(row=1, column=0, sticky=W)
Label(frame3, text='').grid(row=2, column=0, sticky=W)
Label(frame3, text='미래가치').grid(row=3, column=0, sticky=W)

e1 = Entry(frame3, justify=RIGHT)
e1.grid(row=0, column=1)
e2 = Entry(frame3, justify=RIGHT)
e2.grid(row=1, column=1)
e3 = Entry(frame3, justify=RIGHT)
e3.grid(row=2, column=1)

label = Label(frame3, text='')
label.grid(row=3, column=1, sticky=E)

#Button(window, text='계산하기'.grid(row=6, column=1, sticky=E)) #,command=self.compute)

#Label(frame3, text='기준환율', fg='green', font='helvetica 48').pack()

frame1 = Frame(window)
notebook.add(frame1, text='송금 환율')
Label(frame1, text='송금 받을때 : \n송금 보낼때 : ', fg='blue', font='helvetica 48').pack()

frame5 = Frame(window)
notebook.add(frame5, text='즐겨찾기')
Label(frame5, text='즐겨찾기', fg='green', font='helvetica 48').pack()

window.mainloop()