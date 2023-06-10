import tkinter as tk
import tkinter.ttk as ttk

import canvas as canvas
import requests
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
import io
from googlemaps import Client
from matplotlib.figure import Figure

zoom = 13

# 공공데이터 API 키
api_key = "79c17274ed8d431996adaa9ce6c574fd"
# real_key = "AIzaSyBGD2TN0A_nRLExYVnu3xVgdLa5GQRE6D4"

# 경기도 도서 관련 업체 현황 데이터
url = "https://openapi.gg.go.kr/GgCertflyRegionBkstr"
params = {
    "KEY":api_key,
    "numOfRows":357     # 최대 357개의 도서 관련 업체 데이터 요청
}

response = requests.get(url, params=params)
root = ET.fromstring(response.content)
items = root.findall(".//row")

bookstores = []

for item in items:
    bookstore = {
        "name":item.findtext("BKSTR_NM"),               # 도서관 이름
        "address":item.findtext("REFINE_ROADNM_ADDR"),  # 도서관 주소
        "lat":item.findtext("REFINE_WGS84_LAT"),        # 위도
        "lng":item.findtext("REFINE_WGS84_LOGT"),       # 경도
        "sigun":item.findtext("SIGUN_NM"),              # 시군명
    }
    bookstores.append(bookstore)

# 시군별 서점 정보 딕셔너리에 저장 -> {'시군명' : 서점 수}
sigun_bookstore_num = {}

for bookstore in bookstores:
    if sigun_bookstore_num.get(bookstore['sigun']):
        sigun_bookstore_num[bookstore['sigun']] += 1
    else:
        sigun_bookstore_num[bookstore['sigun']] = 1


# Google Maps API 클라이언트 생성 (한달에 $20 까지 무료)
# https://console.cloud.google.com/apis/credentials
Google_API_Key = 'AIzaSyBGD2TN0A_nRLExYVnu3xVgdLa5GQRE6D4'
gmaps = Client(key=Google_API_Key)

# 경기도 지도 생성
GG_center = gmaps.geocode("시흘시")[0]['geometry']['location']
GG_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={GG_center['lat']},{GG_center['lng']}&zoom={zoom}&size=640x480&maptype=roadmap"

# 경기도 시군별 서점 위치 마커 추가
for bookstore in bookstores:
    if bookstore['lat'] and bookstore['lng']:
        lat, lng = float(bookstore['lat']), float(bookstore['lng'])
        marker_url = f"&markers=color:red%7c{lat},{lng}"
        GG_map_url += marker_url

# tkinter GUI 생성
root = tk.Tk()
root.title("경기도 시군별 서점 정보")

# 시군 선택 콤보박스 생성
selected_sigun = tk.StringVar()
selected_sigun.set("시흥시")      # 초기값 설정
sigun_options = set([bookstore['sigun'] for bookstore in bookstores])
sigun_combo = ttk.Combobox(root, textvariable=selected_sigun, values=list(sigun_options))
sigun_combo.pack()

# 서점 목록 표시 함수
def show_bookstores():
    bookstore_list.delete(0, tk.END)

    bookstore_key = list(sigun_bookstore_num.keys())
    bookstore_value = list(sigun_bookstore_num.values())

    for i in range(16):
        bookstore_list.insert(tk.END, f"{bookstore_key[i]}")

    canvas.delete('all')

    max_bookstore_count = max(bookstore_value)
    bar_width = 20
    x_gap = 30
    x0 = 20
    y0 = 250

    for i in range(16):
        x1 = x0 + i * (bar_width + x_gap)
        y1 = y0 - 200 * bookstore_value[i] / max_bookstore_count
        canvas.create_rectangle(x1, y1, x1 + bar_width, y0, fill = 'blue')
        canvas.create_text(x1 + bar_width/2 , y0+100, text=bookstore_key[i], anchor='n', angle=90)
        canvas.create_text(x1 + bar_width/2, y1-10, text=bookstore_value[i], anchor='s')

def update_map():
    global zoom
    sigun_name = selected_sigun.get()

    sigun_center = gmaps.geocode(f"{sigun_name} ")[0]['geometry']['location']
    sigun_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={sigun_center['lat']},{sigun_center['lng']}&zoom={zoom}&size=640x480&maptype=roadmap"

    bookstores_in_sigun = [bookstore for bookstore in bookstores if bookstore['sigun'] == sigun_name]
    for bookstore in bookstores_in_sigun:
        if bookstore['lat'] and bookstore['lng']:
            lat, lng = float(bookstore['lat']), float(bookstore['lng'])
            marker_url = f"&markers=color:red%7C{lat},{lng}"
            sigun_map_url += marker_url

    # 지도 이미지 업데이트
    response = requests.get(sigun_map_url+'&key='+Google_API_Key)
    image = Image.open(io.BytesIO(response.content))
    photo = ImageTk.PhotoImage(image)
    map_label.configure(image=photo)
    map_label.image = photo

    # 지도 목록 업데이트
    show_bookstores()

def on_sigun_select(event):
    update_map()

def zoom_in():
    global zoom
    zoom += 1
    update_map()

def zoom_out():
    global zoom
    if zoom > 1:
        zoom -= 1
    update_map()

# 캔버스 생성
canvas = tk.Canvas(root, width=800, height=400)
canvas.pack()

# 서점 목록 리스트박스 생성
bookstore_list = tk.Listbox(root, width=30)
bookstore_list.pack(side=tk.LEFT, fill=tk.BOTH)

# # 스크롤바 생성
# scrollbar = tk.Scrollbar(root)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# # 스크롤바와 서점 목록 연결
# bookstore_list.config(yscrollcommand=scrollbar.set)
# scrollbar.config(command=bookstore_list.yview)

#경기도 지도 이미지 다운로드
response = requests.get(GG_map_url+'&key='+Google_API_Key)
image = Image.open(io.BytesIO(response.content))
photo = ImageTk.PhotoImage(image)

#지도 이미지 라벨 생성
map_label = tk.Label(root, image=photo)
map_label.pack()

# 확대/축소 버튼 생성
zoom_in_button = tk.Button(root, text="확대(+)", command=zoom_in)
zoom_in_button.pack(side=tk.LEFT)

zoom_out_button = tk.Button(root, text="축소(-)", command=zoom_out)
zoom_out_button.pack(side=tk.LEFT)

sigun_combo.bind("<<ComboboxSelected>>", on_sigun_select)

update_map()

root.mainloop()