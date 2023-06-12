import tkinter as tk
import tkinter.ttk as ttk

import telepot

import SearchFramework

import canvas as canvas
import requests
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
import io
from googlemaps import Client
from matplotlib.figure import Figure

import GlobalWindow
import framework

zoom = 13

GUI = None

def enter():
    global GUI
    GUI = MapGUI()

def exit():
    GUI.exit()

class MapGUI:

    def exit(self):
        self.root.destroy()
    
    def __init__(self):
        self.fontstyleBig = tk.font.Font(GlobalWindow.window, size=30, weight='bold', family='맑은 고딕')
        self.fontstyleMedium = tk.font.Font(GlobalWindow.window, size=20, weight='bold', family='맑은 고딕')
        self.fontstyleSmall = tk.font.Font(GlobalWindow.window, size=10, weight='bold', family='맑은 고딕')
        # 공공데이터 API 키
        self.api_key = "79c17274ed8d431996adaa9ce6c574fd"
        # real_key = "AIzaSyBGD2TN0A_nRLExYVnu3xVgdLa5GQRE6D4"
    
        # 경기도 도서 관련 업체 현황 데이터
        url = "https://openapi.gg.go.kr/GgCertflyRegionBkstr"
        params = {
            "KEY":self.api_key,
            "numOfRows":357     # 최대 357개의 도서 관련 업체 데이터 요청
        }
    
        self.response = requests.get(url, params=params)
        self.root = ET.fromstring(self.response.content)
        self.items = self.root.findall(".//row")
    
        self.bookstores = []

        for item in self.items:
            bookstore = {
                "name": item.findtext("BKSTR_NM"),  # 도서관 이름
                "raddress": item.findtext("REFINE_ROADNM_ADDR"),  # 도서관 도로명 주소
                "laddress": item.findtext("REFINE_LOTNO_ADDR"),  # 도서관 지번 주소
                "lat": item.findtext("REFINE_WGS84_LAT"),  # 위도
                "lng": item.findtext("REFINE_WGS84_LOGT"),  # 경도
                "sigun": item.findtext("SIGUN_NM"),  # 시군명
                "number": item.findtext("CAFTRI_TELNO")  # 전화번호
            }
            self.bookstores.append(bookstore)
        
        # 시군별 서점 정보 딕셔너리에 저장 -> {'시군명' : 서점 수}
        self.sigun_bookstore_num = {}
        
        for bookstore in self.bookstores:
            if self.sigun_bookstore_num.get(bookstore['sigun']):
                self.sigun_bookstore_num[bookstore['sigun']] += 1
            else:
                self.sigun_bookstore_num[bookstore['sigun']] = 1
        
        
        # Google Maps API 클라이언트 생성 (한달에 $20 까지 무료)
        # https://console.cloud.google.com/apis/credentials
        self.Google_API_Key = 'AIzaSyBGD2TN0A_nRLExYVnu3xVgdLa5GQRE6D4'
        self.gmaps = Client(key=self.Google_API_Key)
        
        # 경기도 지도 생성
        GG_center = self.gmaps.geocode("시흥시")[0]['geometry']['location']
        GG_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={GG_center['lat']},{GG_center['lng']}&zoom={zoom}&size=640x480&maptype=roadmap"
        
        # 경기도 시군별 서점 위치 마커 추가
        for bookstore in self.bookstores:
            if bookstore['lat'] and bookstore['lng']:
                lat, lng = float(bookstore['lat']), float(bookstore['lng'])
                marker_url = f"&markers=color:red%7c{lat},{lng}"
                GG_map_url += marker_url
        
        # tkinter GUI 생성
        self.root = tk.Frame(GlobalWindow.window)
        self.root.pack()
        
        # 시군 선택 콤보박스 생성
        self.selected_sigun = tk.StringVar()
        self.selected_sigun.set("시흥시")      # 초기값 설정
        self.sigun_options = set([bookstore['sigun'] for bookstore in self.bookstores])
        self.sigun_combo = ttk.Combobox(self.root, textvariable=self.selected_sigun, values=list(self.sigun_options),
                                        font=self.fontstyleMedium)
        self.sigun_combo.pack()

        # 캔버스 생성
        self.canvas = tk.Canvas(self.root, width=800, height=400)
        self.canvas.pack()

        # 서점 목록 리스트박스 생성
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.bookstore_list = tk.Listbox(self.list_frame, width=30, height=20)
        self.bookstore_list.pack()
        self.button_test = tk.Button(self.list_frame, text="서점 위치와 전화번호 찾기", command=self.return_value,
                                     font=self.fontstyleSmall)
        self.button_test.pack()

        self.bkstr_listbox = []
        self.bot = telepot.Bot(token='5805668477:AAE_IXgsIPicwjj_lXBOHCBoaVIxNjVYgrQ')


        # # 스크롤바 생성
        # scrollbar = tk.Scrollbar(self.root)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # # 스크롤바와 서점 목록 연결
        # bookstore_list.config(yscrollcommand=scrollbar.set)
        # scrollbar.config(command=bookstore_list.yview)

        # 경기도 지도 이미지 다운로드
        self.response = requests.get(GG_map_url + '&key=' + self.Google_API_Key)
        self.image = Image.open(io.BytesIO(self.response.content))
        self.photo = ImageTk.PhotoImage(self.image)

        # 지도 이미지 라벨 생성
        self.map_label = tk.Label(self.root, image=self.photo)
        self.map_label.pack()

        # 확대/축소 버튼 생성
        self.zoom_in_button = tk.Button(self.root, text="확대(+)", command=self.zoom_in, font=self.fontstyleMedium)
        self.zoom_in_button.pack(side=tk.LEFT)

        self.zoom_out_button = tk.Button(self.root, text="축소(-)", command=self.zoom_out, font=self.fontstyleMedium)
        self.zoom_out_button.pack(side=tk.LEFT)

        self.sigun_combo.bind("<<ComboboxSelected>>", self.on_sigun_select)

        self.update_map()
        self.goMapButton = tk.Button(self.root, text='메인으로', font=self.fontstyleMedium,
                                  command=self.pressExit, borderwidth=5)
        self.goMapButton.place(x=740, y=5)

    def pressExit(self):
        framework.change_state(SearchFramework)

    def show_bookstores(self):
        self.bookstore_list.delete(0, tk.END)
        self.bkstr_listbox.clear()
        sigun_name = self.selected_sigun.get()
        self.bookstores_in_sigun = [bookstore for bookstore in self.bookstores if bookstore['sigun'] == sigun_name]

        self.bookstore_key = list(self.sigun_bookstore_num.keys())
        self.bookstore_value = list(self.sigun_bookstore_num.values())

        for bookstore in self.bookstores_in_sigun:
            self.bookstore_list.insert(tk.END, f"{bookstore['name']}")
            self.bkstr_listbox.append(bookstore)
            print(self.bkstr_listbox)

        self.canvas.delete('all')

        self.max_bookstore_count = max(self.bookstore_value)
        bar_width = 20
        x_gap = 30
        x0 = 20
        y0 = 250

        for i in range(16):
            x1 = x0 + i * (bar_width + x_gap)
            y1 = y0 - 200 * self.bookstore_value[i] / self.max_bookstore_count
            self.canvas.create_rectangle(x1, y1, x1 + bar_width, y0, fill='blue')
            self.canvas.create_text(x1 + bar_width / 2, y0 + 100, text=self.bookstore_key[i],
                                    anchor='n', angle=90, font=self.fontstyleSmall)
            self.canvas.create_text(x1 + bar_width / 2, y1 - 10, text=self.bookstore_value[i],
                                    anchor='s', font=self.fontstyleSmall)

    def return_value(self):
        print(f'Listbox 선택 항목 위치 반환값: {self.bookstore_list.curselection()}')
        print(self.bkstr_listbox[int(self.bookstore_list.curselection()[0])])
        
        self.chat_id = 6039547412
        # message =
        self.bot.sendMessage(chat_id=self.chat_id,
                             text=self.bkstr_listbox[int(self.bookstore_list.curselection()[0])]['name'])
        self.bot.sendMessage(chat_id=self.chat_id, text='전화 번호 -> ')
        self.bot.sendMessage(chat_id=self.chat_id,
                             text=self.bkstr_listbox[int(self.bookstore_list.curselection()[0])]['number'])
        self.bot.sendMessage(chat_id=self.chat_id, text='지번 주소 -> ')
        self.bot.sendMessage(chat_id=self.chat_id,
                             text=self.bkstr_listbox[int(self.bookstore_list.curselection()[0])]['laddress'])
        self.bot.sendMessage(chat_id=self.chat_id, text='도로명 주소 -> ')
        self.bot.sendMessage(chat_id=self.chat_id,
                             text=self.bkstr_listbox[int(self.bookstore_list.curselection()[0])]['raddress'])
        self.bot.sendMessage(chat_id=self.chat_id, text='------------------------------------')


    def update_map(self):
        global zoom
        sigun_name = self.selected_sigun.get()
    
        sigun_center = self.gmaps.geocode(f"{sigun_name} ")[0]['geometry']['location']
        sigun_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={sigun_center['lat']},{sigun_center['lng']}&zoom={zoom}&size=640x480&maptype=roadmap"
    
        bookstores_in_sigun = [bookstore for bookstore in self.bookstores if bookstore['sigun'] == sigun_name]
        for bookstore in bookstores_in_sigun:
            if bookstore['lat'] and bookstore['lng']:
                lat, lng = float(bookstore['lat']), float(bookstore['lng'])
                marker_url = f"&markers=color:red%7C{lat},{lng}"
                sigun_map_url += marker_url
    
        # 지도 이미지 업데이트
        response = requests.get(sigun_map_url+'&key='+self.Google_API_Key)
        image = Image.open(io.BytesIO(response.content))
        photo = ImageTk.PhotoImage(image)
        self.map_label.configure(image=photo)
        self.map_label.image = photo
    
        # 지도 목록 업데이트
        self.show_bookstores()
    
    def on_sigun_select(self, event):
        self.update_map()
    
    def zoom_in(self):
        global zoom
        zoom += 1
        self.update_map()
    
    def zoom_out(self):
        global zoom
        if zoom > 1:
            zoom -= 1
        self.update_map()

