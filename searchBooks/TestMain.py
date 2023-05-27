import tkinter
from tkinter import *
from io import BytesIO
from tkinter import font
from PIL import Image,ImageTk
import urllib
import urllib.request
import internetbook

class MainGUI:
    def getBookDataFromTITLE(self):
        title = (self.searchEntry.get())
        url = internetbook.getBookDataFromTitle(title)
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        image = ImageTk.PhotoImage(im)
        Label(self.window, image=image).place(x=200, y=200)

    def __init__(self):
        self.window = Tk()
        self.window.title('read a book')
        self.window.geometry('1000x800')
        self.fontstyle = font.Font(self.window, size=20, weight='bold', family='맑은 고딕')
        self.bookLabels = []
        self.searchFrame = tkinter.Frame(self.window)
        self.searchFrame.pack(side='top')
        self.canvas = Canvas(self.searchFrame, bg='white', width=400, height=300)
        self.searchLabel = Label(self.searchFrame, text="책 제목으로 검색", font=self.fontstyle)
        self.searchLabel.pack(side='left')
        self.searchEntry = Entry(self.searchFrame, font=self.fontstyle)
        self.searchEntry.pack(side='left')
        self.searchButton = Button(self.searchFrame, text="검색", font=self.fontstyle, command=self.getBookDataFromTITLE)
        self.searchButton.pack(side='left')

        self.window.mainloop()

MainGUI()