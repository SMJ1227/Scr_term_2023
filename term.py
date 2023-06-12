import requests
import json
from tkinter import *
import tkinter.ttk
import spam
import io
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk, ImageFilter
import matplotlib.pyplot as plt
from googlemaps import Client

plt.rcParams['font.family'] = 'Malgun Gothic'
# Google Maps API 클라이언트 생성

gmaps = Client(key=Google_API_Key)
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

#프레임1
def display_exchange_rate_koreaexim():
    scrollbar.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    for i, row_name in enumerate(header):
        label = tkinter.Label(scrollable_frame, text=row_name, font=("Helvetica", 14, "bold"), borderwidth=2, relief="solid", width=13, height=2)
        label.grid(row=0, column=i + 2)
    for i, currency_info in enumerate(data_list):
        for j, value in enumerate(currency_info[:-1]):
            value_str = str(value).replace(' ', '/')  # ' '를 '/'로 치환
            label = tkinter.Label(scrollable_frame, text=value_str, font=("Helvetica", 12), borderwidth=2, relief="solid", width=17, height=2)
            label.grid(row=i + 1, column=j + 2)

def messagebox_graph():
    exchange_rates = []
    currency_names = []

    for item in data_list:
        currency_name = item[0].replace(' ', '/')  # 국가/통화명
        exchange_rate = float(item[2].replace(',', ''))  # 매매 기준율 (쉼표 제거 후 float로 변환)
        currency_names.append(currency_name)
        exchange_rates.append(exchange_rate)

    plt.figure(num='매매 기준율', figsize=(10, 6))
    # 그래프 그리기
    bars = plt.bar(currency_names, exchange_rates)
    plt.xlabel('국가/통화명')
    plt.ylabel('매매 기준율')
    plt.title('매매 기준율')
    plt.xticks(rotation=90)
    plt.tight_layout()
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, str(height), ha='center', va='bottom')
    plt.show()

frame1 = Frame(window)
notebook.add(frame1, text='나라별 환율 정보')
col_count = 1

Button(frame1, text='한국수출입은행', command=display_exchange_rate_koreaexim).pack()
Button(frame1, text='그래프 생성', command=messagebox_graph).pack()

canvas = Canvas(frame1)
scrollbar = Scrollbar(frame1, orient='vertical', command=canvas.yview)
scrollable_frame = Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)

#프레임2
def update_map():
    selected_index = currency_listbox_2.curselection()
    if selected_index == '위안화':
        selected_country = '중국'
    elif selected_index == '유로':
        selected_country = '유럽'
    else:
        selected_country = currency_listbox_2.get(selected_index)
    geocode_result = gmaps.geocode(selected_country)
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        zoom = 3
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size=400x400&maptype=roadmap"
        # 나라 위치에 마커 추가
        marker_url = f"&markers=color:red%7C{latitude},{longitude}"
        map_url += marker_url
        response = requests.get(map_url+'&key='+Google_API_Key)
        image = Image.open(io.BytesIO(response.content))
        photo = ImageTk.PhotoImage(image)
        map_label.configure(image=photo)
        map_label.image = photo

def toggle_star():
    selected_currency_index = currency_listbox_2.curselection()
    if selected_currency_index:
        selected_currency_info = data_list[selected_currency_index[0]]
        current_image = star_button['image']
        if selected_currency_info[5]:
            selected_currency_info[5] = False
            star_button.config(image=black_star_image)
            star_list.remove(selected_currency_info[0])
        elif not selected_currency_info[5]:
            selected_currency_info[5] = True
            star_button.config(image=yellow_star_image)
            star_list.append(selected_currency_info[0])

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
    # 맵 이미지 업데이트
    update_map()

def update_star_list(event):
    currency_listbox_5.delete(0, END)  # 기존 아이템 모두 삭제
    currency_names_5 = [currency_info.replace(' ', '/') for currency_info in star_list]
    for currency_name in currency_names_5:
        currency_listbox_5.insert(END, currency_name)
notebook.bind("<<NotebookTabChanged>>", update_star_list)

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
map_label = Label(frame2)
map_label.grid(row=1, column=4, rowspan=14)

black_star_image = PhotoImage(file='blackstar.png', width=100, height=100)
yellow_star_image = PhotoImage(file='yellowstar.png', width=100, height=100)

star_button = Button(frame2, image=black_star_image, command=toggle_star)
star_button.grid(row=0, column=4, sticky=E)

#프레임3
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
                converted_amount = float(spam.division(input_amount, exchange_rate))
                if extracted_currency in ['옌', '루피아']:
                    e3.config(text=f"{converted_amount * 100:.4f} {extracted_currency}")
                else:
                    e3.config(text=f"{converted_amount:.4f} {extracted_currency}")
            except ValueError:
                e3.config(text='입력값 오류')
        except ValueError:
            e3.config(text='환율 오류')
    else:
        e3.config(text='')


frame3 = Frame(window)
notebook.add(frame3, text='매매 기준율')
currency_names_3 = [currency_info[0].replace(' ', '/') for currency_info in data_list]
currency_listbox_3 = Listbox(frame3, selectmode=SINGLE, height=len(currency_names_3))
for currency_name in currency_names_3:
    currency_listbox_3.insert(END, currency_name)
currency_listbox_3.grid(row=0, column=0, rowspan=3, sticky=W)
currency_listbox_3.bind('<<ListboxSelect>>', update_exchange_rate)  # 리스트박스 선택 이벤트에 update_exchange_rate 함수 바인딩

Label(frame3, text='매매 기준율', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=0, column=1)
Label(frame3, text='환전액', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=1, column=1)
Label(frame3, text='한국수출입은행', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=0, column=4)

e1 = Label(frame3, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
e1.grid(row=0, column=2)
e2 = Entry(frame3, justify=CENTER, borderwidth=1, relief="solid")
e2.grid(row=1, column=2)
e3 = Label(frame3, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
e3.grid(row=0, column=5)

Button(frame3, text='계산하기', command=calculate_exchange_rate).grid(row=2, column=5, sticky=E)

#프레임4
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
                converted_amount_ttb = float(spam.division(input_amount, ttb_rate))
                converted_amount_tts = float(spam.division(input_amount, tts_rate))
                if extracted_currency in ['옌', '루피아']:
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
Label(frame4, text='한국수출입은행', font=("Helvetica", 14, "bold"), justify=CENTER, borderwidth=1, relief="solid").grid(row=2, column=4)

f0 = Label(frame4, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
f0.grid(row=0, column=2)
f1 = Label(frame4, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
f1.grid(row=2, column=2)
f2 = Entry(frame4, justify=CENTER, borderwidth=1, relief="solid")
f2.grid(row=4, column=2)
f3 = Label(frame4, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
f3.grid(row=0, column=5)
f5 = Label(frame4, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
f5.grid(row=2, column=5)

Button(frame4, text='계산하기', command=calculate_tt).grid(row=4, column=5, sticky=E)

# 프레임5
data_star_list = []

def update_star_list():
    # star_list의 값을 기준으로 data_list와 비교하여 일치하는 값의 다른 데이터를 data_star_list에 저장
    for star_currency_name in star_list:
        for star_currency_info in star_list:
            star_currency_name = star_currency_info[0].replace('/', ' ')  # /를 공백으로 바꾼 값
            for data in data_list:
                if data[0] == star_currency_name:
                    data_star_list.append([data[0], data[1], data[2], data[3], data[4], data[5]])

def update_star_data(event):
    selected_currency_index = currency_listbox_5.curselection()
    print(data_star_list)
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
            l1.config(text=str(currency_code_info))
            currency_name_info = sel_currency_name
            l2.config(text=str(currency_name_info))
            exchange_rate_info = sel_exchange_rate
            l3.config(text=str(exchange_rate_info))
            ttb_info = float(sel_ttb)
            l4.config(text=str(ttb_info))
            tts_info = float(sel_tts)
            l5.config(text=str(tts_info))
            # 국기 이미지 업데이트
            image_path = selected_currency_info[0] + ".png"
            img = Image.open(image_path)
            # 라벨의 크기에 맞게 이미지 크기 조절
            label_width = l6.winfo_width()
            label_height = l6.winfo_height()
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
            l6.config(image=None)  # 기존의 이미지 객체 제거
            l6.config(image=tk_img)
            l6.image = tk_img  # 이미지가 Garbage Collected 되지 않도록 변수에 대입
        except ValueError:
            l1.config(text='국가/통화명 오류')
            l2.config(text='통화 코드 오류')
            l3.config(text='매매 기준율 오류')
            l4.config(text='ttb 오류')
            l5.config(text='tts 오류')
    else:
        l1.config(text='')
        l2.config(text='')
        l3.config(text='')
        l4.config(text='')
        l5.config(text='')

frame5 = Frame(window)
notebook.add(frame5, text='즐겨찾기')
currency_names_5 = [currency_info[0].replace(' ', '/') for currency_info in star_list]
currency_listbox_5 = Listbox(frame5, selectmode=SINGLE, height=len(currency_names_5))
for currency_info in star_list:
    currency_name = currency_info[0].replace(' ', '/')
    currency_listbox_5.insert(END, currency_name)  # 전체 문자열 추가
currency_listbox_5.grid(row=0, column=0, rowspan=6, sticky=W)
currency_listbox_5.bind('<<ListboxSelect>>', update_star_data)  # 리스트박스 선택 이벤트에 update_data 함수 바인딩

for i, row_name in enumerate(header):
    label = tkinter.Label(frame5, text=row_name, font=("Helvetica", 14, "bold"), borderwidth=2, relief="solid", width=13, height=2)
    label.grid(row=i, column=2)
l1 = Label(frame5, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
l1.grid(row=0, column=3)
l2 = Label(frame5, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
l2.grid(row=1, column=3)
l3 = Label(frame5, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
l3.grid(row=2, column=3)
l4 = Label(frame5, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
l4.grid(row=3, column=3)
l5 = Label(frame5, bg='white', justify=CENTER, width=20, height=1, borderwidth=1, relief="solid")
l5.grid(row=4, column=3)
photo_flag_frame5 = PhotoImage(file='bg.png', width=150, height=100)
l6 = Label(frame5, image=photo_flag_frame5)
l6.grid(row=0, column=4)


window.mainloop()
