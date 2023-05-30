import requests
import json
from tkinter import *
import tkinter.ttk
from tkinter import messagebox

#한국수출입은행
url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=aczTjwLTrbV7vvKgVuQj1Vtb1uLoTepd&searchdate=20230525&data=AP01'
response = requests.get(url)
data = response.json()

# Access and print specific elements from JSON data
data_list = []

for item in data:
    currency_code = item['cur_unit']# 통화 코드
    currency_name = item['cur_nm']# 국가/통화명
    exchange_rate = item['deal_bas_r']# 매매 기준율
    ttb = item['ttb']# 송금 받을때
    tts = item['tts']# 송금 보낼때
    data_list.append([currency_name, currency_code, exchange_rate, ttb, tts])

header = ['국가/통화명', '통화 코드', '매매 기준율', '송금 받을때', '송금 보낼때']

window = Tk()
window.title('환율 검색 프로그램')

notebook = tkinter.ttk.Notebook(window, width=850, height=400)
notebook.pack()

def calculate_exchange_rate():
    selected_currency_index = currency_listbox_3.curselection()
    if selected_currency_index:
        selected_currency_info = data_list[selected_currency_index[0]]
        currency_name = selected_currency_info[0]
        currency_code = selected_currency_info[1]
        extracted_currency = currency_name.split(' ')[-1].strip('()')
        exchange_rate_str = selected_currency_info[2]
        exchange_rate_str = exchange_rate_str.replace(',', '')  # 쉼표 제거
        try:
            exchange_rate = float(exchange_rate_str)
            input_amount_str = e2.get()
            input_amount_str = input_amount_str.replace(',', '')  # 쉼표 제거
            try:
                input_amount = float(input_amount_str)
                converted_amount = input_amount / exchange_rate
                if extracted_currency == '옌' or '루피아':
                    e3.config(text=f"{float(converted_amount) * 100:.6f} {extracted_currency}")
                else:
                    e3.config(text=f"{float(converted_amount):.6f} {extracted_currency}")
            except ValueError:
                e3.config(text='입력값 오류')
        except ValueError:
            e3.config(text='환율 오류')
    else:
        e3.config(text='')

def calculate_tt():
    selected_currency_index = currency_listbox_4.curselection()
    if selected_currency_index:
        selected_currency_info = data_list[selected_currency_index[0]]
        currency_name = selected_currency_info[0]
        currency_code = selected_currency_info[1]
        extracted_currency = currency_name.split(' ')[-1].strip('()')
        ttb_str = selected_currency_info[3]
        ttb_str = ttb_str.replace(',', '')  # 쉼표 제거
        tts_str = selected_currency_info[4]
        tts_str = tts_str.replace(',', '')  # 쉼표 제거
        try:
            ttb_rate = float(ttb_str)
            tts_rate = float(tts_str)
            input_amount_str = f2.get()
            input_amount_str = input_amount_str.replace(',', '')  # 쉼표 제거
            try:
                input_amount = float(input_amount_str)
                converted_amount_ttb = input_amount / ttb_rate
                converted_amount_tts = input_amount / tts_rate
                if extracted_currency == '옌' or '루피아':
                    f3.config(text=f"{float(converted_amount_ttb) * 100:.6f} {extracted_currency}")
                    f5.config(text=f"{float(converted_amount_tts) * 100:.6f} {extracted_currency}")
                else:
                    f3.config(text=f"{float(converted_amount_ttb):.6f} {extracted_currency}")
                    f5.config(text=f"{float(converted_amount_tts):.6f} {extracted_currency}")
            except ValueError:
                f3.config(text='입력값 오류')
                f5.config(text='입력값 오류')
        except ValueError:
            f3.config(text='환율 오류')
            f5.config(text='환율 오류')
    else:
        f3.config(text='')
        f5.config(text='')

def update_data(event):
    for i, row_name in enumerate(header):
        label = tkinter.Label(frame2, text=row_name, font=("Helvetica", 14, "bold"), borderwidth=2,
                              relief="solid", width=13, height=2)
        label.grid(row=i, column=2)

def update_exchange_rate(event):
    selected_currency_index = currency_listbox_3.curselection()
    if selected_currency_index:
        selected_currency_info = data_list[selected_currency_index[0]]
        exchange_rate_str = selected_currency_info[2]
        exchange_rate_str = exchange_rate_str.replace(',', '')  # 쉼표 제거
        try:
            exchange_rate = float(exchange_rate_str)
            e1.config(text=str(exchange_rate))
        except ValueError:
            e1.config(text='매매 기준율 오류')
    else:
        e1.config(text='')

def update_tt(event):
    selected_currency_index = currency_listbox_4.curselection()
    if selected_currency_index:
        selected_currency_info = data_list[selected_currency_index[0]]
        ttb_str = selected_currency_info[3]
        ttb_str = ttb_str.replace(',', '')  # 쉼표 제거
        tts_str = selected_currency_info[4]
        tts_str = tts_str.replace(',', '')  # 쉼표 제거
        try:
            ttb = float(ttb_str)
            f0.config(text=str(ttb))
            tts = float(tts_str)
            f1.config(text=str(tts))
        except ValueError:
            f0.config(text='ttb 오류')
            f1.config(text='tts 오류')
    else:
        f0.config(text='')
        f1.config(text='')

#프레임1
frame1 = Frame(window)
notebook.add(frame1, text='나라별 환율 정보')
col_count = 1

canvas = Canvas(frame1)
scrollbar = Scrollbar(frame1, orient='vertical', command=canvas.yview)
scrollable_frame = Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)

v = IntVar()
from tkinter import messagebox

def display_exchange_rate_koreaexim():
    selected_bank = v.get()
    if selected_bank == 1:
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)
        for i, row_name in enumerate(header):
            label = tkinter.Label(scrollable_frame, text=row_name, font=("Helvetica", 14, "bold"), borderwidth=2,
                                  relief="solid", width=13, height=2)
            label.grid(row=0, column=i + 2)
        for i, currency_info in enumerate(data_list):
            for j, value in enumerate(currency_info):
                value_str = str(value).replace(' ', '/')  # ' '를 '/'로 치환
                label = tkinter.Label(scrollable_frame, text=value_str, font=("Helvetica", 12), borderwidth=2,
                                      relief="solid", width=17, height=2)
                label.grid(row=i + 1, column=j + 2)
# 라디오 버튼 생성
Radiobutton(frame1, text='한국수출입은행', variable=v, value=1, command=display_exchange_rate_koreaexim).pack()
Radiobutton(frame1, text='하나은행', variable=v, value=2, command=display_exchange_rate_koreaexim).pack()

#프레임2
frame2 = Frame(window)
notebook.add(frame2, text='나라 검색')
currency_names_2 = [currency_info[0] for currency_info in data_list]
currency_listbox_2 = Listbox(frame2, selectmode=SINGLE, height=len(currency_names_2))

for currency_name in currency_names_2:
    currency_listbox_2.insert(END, currency_name)
currency_listbox_2.grid(row=0, column=0, rowspan=6, sticky=W)
currency_listbox_2.bind('<<ListboxSelect>>', update_data)  # 리스트박스 선택 이벤트에 update_data 함수 바인딩

#프레임3
frame3 = Frame(window)
notebook.add(frame3, text='매매 기준율')
currency_names_3 = [currency_info[0] for currency_info in data_list]
currency_listbox_3 = Listbox(frame3, selectmode=SINGLE, height=len(currency_names_3))
for currency_name in currency_names_3:
    currency_listbox_3.insert(END, currency_name)
currency_listbox_3.grid(row=0, column=0, rowspan=3, sticky=W)
currency_listbox_3.bind('<<ListboxSelect>>', update_exchange_rate)  # 리스트박스 선택 이벤트에 update_exchange_rate 함수 바인딩

Label(frame3, text='매매 기준율', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=0, column=1)
Label(frame3, text='환전액', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=2, column=1)
Label(frame3, text='한국수출입은행', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=0, column=4)
Label(frame3, text='하나은행', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=1, column=4)

e1 = Label(frame3, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
e1.grid(row=0, column=2)
e2 = Entry(frame3, justify=CENTER, borderwidth=1, relief="solid")
e2.grid(row=2, column=2)
e3 = Label(frame3, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
e3.grid(row=0, column=5)
e4 = Label(frame3, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
e4.grid(row=1, column=5)

Button(frame3, text='계산하기', command=calculate_exchange_rate).grid(row=2, column=5, sticky=E)

#프레임4
frame4 = Frame(window)
notebook.add(frame4, text='전신환 환율')
currency_names_4 = [currency_info[0] for currency_info in data_list]
currency_listbox_4 = Listbox(frame4, selectmode=SINGLE, height=len(currency_names_4))
for currency_name in currency_names_4:
    currency_listbox_4.insert(END, currency_name)
currency_listbox_4.grid(row=0, column=0, rowspan=6, sticky=W)
currency_listbox_4.bind('<<ListboxSelect>>', update_tt)  # 리스트박스 선택 이벤트에 update_tt 함수 바인딩

Label(frame4, text='송금받으실때(판매시)', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=0, column=1)
Label(frame4, text='송금보내실때(구매시)', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=2, column=1)
Label(frame4, text='환전액', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=4, column=1)
Label(frame4, text='한국수출입은행', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=0, column=4)
Label(frame4, text='하나은행', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=1, column=4)
Label(frame4, text='한국수출입은행', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=2, column=4)
Label(frame4, text='하나은행', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=3, column=4)

f0 = Label(frame4, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
f0.grid(row=0, column=2)
f1 = Label(frame4, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
f1.grid(row=2, column=2)
f2 = Entry(frame4, justify=CENTER, borderwidth=1, relief="solid")
f2.grid(row=4, column=2)
f3 = Label(frame4, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
f3.grid(row=0, column=5)
f4 = Label(frame4, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
f4.grid(row=1, column=5)
f5 = Label(frame4, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
f5.grid(row=2, column=5)
f6 = Label(frame4, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
f6.grid(row=3, column=5)

Button(frame4, text='계산하기', command=calculate_tt).grid(row=4, column=5, sticky=E)


frame5 = Frame(window)
notebook.add(frame5, text='즐겨찾기')
Label(frame5, text='즐겨찾기', fg='green', font='helvetica 48').pack()

window.mainloop()
