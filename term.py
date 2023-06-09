import requests
import json
from tkinter import *
import tkinter.ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter

#한국수출입은행
url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey=aczTjwLTrbV7vvKgVuQj1Vtb1uLoTepd&searchdate=20230609&data=AP01'
response = requests.get(url)
data = response.json()

# Access and print specific elements from JSON data
data_list = []
star_list = []

for item in data:
    currency_code = item['cur_unit']# 통화 코드
    currency_name = item['cur_nm']# 국가/통화명
    exchange_rate = item['deal_bas_r']# 매매 기준율
    ttb = item['ttb']# 송금 받을때
    tts = item['tts']# 송금 보낼때
    star = False
    data_list.append([currency_name, currency_code, exchange_rate, ttb, tts, star])

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
    selected_currency_index = currency_listbox_2.curselection()
    if selected_currency_index:
        selected_currency_info = data_list[selected_currency_index[0]]
        sel_currency_code = selected_currency_info[0]
        sel_currency_name = selected_currency_info[1]
        sel_exchange_rate = selected_currency_info[2]
        sel_exchange_rate = sel_exchange_rate.replace(',', '')  # 쉼표 제거
        sel_ttb = selected_currency_info[3]
        sel_ttb = sel_ttb.replace(',', '')  # 쉼표 제거
        sel_tts = selected_currency_info[4]
        sel_tts = sel_tts.replace(',', '')  # 쉼표 제거
        try:
            currency_code_info = sel_currency_code
            g1.config(text=str(currency_code_info))
            currency_name_info = sel_currency_name
            g2.config(text=str(currency_name_info))
            exchange_rate_info = sel_exchange_rate
            g3.config(text=str(exchange_rate_info))
            ttb_info = float(sel_ttb)
            g4.config(text=str(ttb_info))
            tts_info = float(sel_tts)
            g5.config(text=str(tts_info))
            # 국기 이미지 업데이트
            image_path = selected_currency_info[0] + ".png"
            img = Image.open(image_path)
            # 라벨의 크기에 맞게 이미지 크기 조절
            label_width = g6.winfo_width()
            label_height = g6.winfo_height()
            image_width, image_height = img.size
            # 최소 너비와 최소 높이 설정
            min_width = 150
            min_height = 100
            # 이미지의 가로 세로 비율에 맞게 크기 조절
            if image_width / image_height > label_width / label_height:
                resized_img = img.resize(
                    (max(label_width, min_width), int(max(label_width * image_height / image_width, min_height))),
                    Image.LANCZOS)
            else:
                resized_img = img.resize(
                    (int(max(label_height * image_width / image_height, min_width)), max(label_height, min_height)), Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(resized_img)  # 이미지를 Tkinter에서 사용할 수 있는 형식으로 변환
            g6.config(image=None)  # 기존의 이미지 객체 제거
            g6.config(image=tk_img)
            g6.image = tk_img  # 이미지가 Garbage Collected 되지 않도록 변수에 대입
            # 별 이미지 업데이트
            if selected_currency_info[5]:
                star_button.config(image=yellow_star_image)
            else:
                star_button.config(image=black_star_image)
        except ValueError:
            g1.config(text='국가/통화명 오류')
            g2.config(text='통화 코드 오류')
            g3.config(text='매매 기준율 오류')
            g4.config(text='ttb 오류')
            g5.config(text='tts 오류')
    else:
        g1.config(text='')
        g2.config(text='')
        g3.config(text='')
        g4.config(text='')
        g5.config(text='')

def toggle_star():
    selected_currency_index = currency_listbox_2.curselection()
    if selected_currency_index:
        selected_currency_info = data_list[selected_currency_index[0]]
        current_image = star_button['image']
        if selected_currency_info[5]:
            selected_currency_info[5] = False
            star_button.config(image=black_star_image)
            star_list.remove(selected_currency_info[0])
            print(star_list)
        elif not selected_currency_info[5]:
            selected_currency_info[5] = True
            star_button.config(image=yellow_star_image)
            star_list.append(selected_currency_info[0])
            print(star_list)

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
currency_names_2 = [currency_info[0].replace(' ', '/') for currency_info in data_list]
currency_listbox_2 = Listbox(frame2, selectmode=SINGLE, height=len(currency_names_2))

for currency_name in currency_names_2:
    currency_listbox_2.insert(END, currency_name)
currency_listbox_2.grid(row=0, column=0, rowspan=6, sticky=W)
for i, row_name in enumerate(header):
    label = tkinter.Label(frame2, text=row_name, font=("Helvetica", 14, "bold"), borderwidth=2,
                          relief="solid", width=13, height=2)
    label.grid(row=i, column=2)
currency_listbox_2.bind('<<ListboxSelect>>', update_data)  # 리스트박스 선택 이벤트에 update_data 함수 바인딩

g1 = Label(frame2, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
g1.grid(row=0, column=3)
g2 = Label(frame2, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
g2.grid(row=1, column=3)
g3 = Label(frame2, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
g3.grid(row=2, column=3)
g4 = Label(frame2, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
g4.grid(row=3, column=3)
g5 = Label(frame2, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
g5.grid(row=4, column=3)
photo_flag = PhotoImage(file='bg.png', width=150, height=100)
g6 = Label(frame2, image=photo_flag)
g6.grid(row=0, column=4)

black_star_image = PhotoImage(file='blackstar.png', width=100, height=100)
yellow_star_image = PhotoImage(file='yellowstar.png', width=100, height=100)

star_button = Button(frame2, image=black_star_image, command=toggle_star)
star_button.grid(row=0, column=5, sticky=E)

#프레임3
frame3 = Frame(window)
notebook.add(frame3, text='매매 기준율')
currency_names_3 = [currency_info[0].replace(' ', '/') for currency_info in data_list]
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
currency_names_4 = [currency_info[0].replace(' ', '/') for currency_info in data_list]
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

# 프레임5
frame5 = Frame(window)
notebook.add(frame5, text='즐겨찾기')

currency_names_5 = [currency_info[0].replace(' ', '/') for currency_info in star_list]
currency_listbox_5 = Listbox(frame5, selectmode=SINGLE, height=len(currency_names_5))
for currency_info in star_list:
    currency_name = currency_info[0].replace(' ', '/')
    currency_listbox_5.insert(END, currency_name)  # 전체 문자열 추가
currency_listbox_5.grid(row=0, column=0, rowspan=6, sticky=W)

for i, row_name in enumerate(header):
    label = tkinter.Label(frame5, text=row_name, font=("Helvetica", 14, "bold"), borderwidth=2, relief="solid", width=13, height=2)
    label.grid(row=i, column=2)

def update_star_list(event):
    currency_listbox_5.delete(0, END)  # 기존 아이템 모두 삭제
    currency_names_5 = [currency_info.replace(' ', '/') for currency_info in star_list]
    for currency_name in currency_names_5:
        currency_listbox_5.insert(END, currency_name)
notebook.bind("<<NotebookTabChanged>>", update_star_list)


window.mainloop()
