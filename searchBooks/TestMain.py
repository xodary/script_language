import tkinter
from tkinter import *
from io import BytesIO
from tkinter import font
from PIL import Image,ImageTk
import urllib
import urllib.request

import game_framework
import internetbook
import BookClass
import framework

class SearchBookGUI:
    bookImageHeight = 300

    def enter(self):
        self.searchFrame = tkinter.Frame(self.window)
        self.searchFrame.pack(side='top')
        self.canvas = Canvas(self.searchFrame, bg='white', width=400, height=300)
        self.searchLabel = Label(self.searchFrame, text="책 제목으로 검색", font=self.fontstyleBig)
        self.searchLabel.pack(side='left')
        self.searchEntry = Entry(self.searchFrame, font=self.fontstyleBig)
        self.searchEntry.pack(side='left')
        self.searchButton = Button(self.searchFrame, text="검색", font=self.fontstyleBig,
                                   command=self.getBookDataFromTITLE)
        self.searchButton.pack(side='left')
    def exit(self):
        for frame in self.bookListFrames:
            frame.destroy()
        self.searchFrame.destroy()
    def bookClickUp(self, event):
        print("위쪽 책 선택")
        game_framework.change_state()
    def bookClickDown(self, event):
        print("아래쪽 책 선택")

    def getBookDataFromTITLE(self):
        print('버튼 눌림')
        title = (self.searchEntry.get())
        bookDatas = internetbook.getBookDataFromTitle(title)
        self.images = []
        bookClickFunc = [self.bookClickUp, self.bookClickDown]
        # self.bookListBox = Listbox(self.window)
        # self.bookListBox.pack()
        self.bookList = []
        self.bookListFrames = []
        for idx, bookData in enumerate(bookDatas):
            B = BookClass.Book(bookData)
            self.bookList.append(B)
            self.bookListFrame = Frame(self.window, relief="raised", borderwidth=3)
            self.bookListFrames.append(self.bookListFrame)
            self.bookListFrame.pack()
            self.clickLabels = []
            with urllib.request.urlopen(B.getImage()) as u:        # image 출력
                raw_data = u.read()
            openImage = Image.open(BytesIO(raw_data))
            resizedImage = openImage.resize(
                (int(SearchBookGUI.bookImageHeight * openImage.size[0] / openImage.size[1]),
                               SearchBookGUI.bookImageHeight))
            self.images.append(ImageTk.PhotoImage(resizedImage))
            self.imageLabel = Label(self.bookListFrame, image=self.images[-1])
            self.imageLabel.grid(row=0, column=0, rowspan=3)
            self.clickLabels.append(self.imageLabel)
            title = B.getTitle()[:20] + ' ... '
            self.titleLabel = Label(self.bookListFrame, text=title,font=self.fontstyleBig, background='#E4F3F6')
            self.titleLabel.grid(row=0, column=1, columnspan=3, sticky=W)
            self.clickLabels.append(self.titleLabel)
            author = B.getAuthor()[:5] + ' ... '
            self.authorLabel = Label(self.bookListFrame, text='작가: '+author,anchor=S, font=self.fontstyleMedium)
            self.authorLabel.grid(row=1, column=1, sticky=W)
            self.clickLabels.append(self.authorLabel)
            publisher = B.getPublisher()[:5] + ' ... '
            self.publisherLabel = Label(self.bookListFrame, text='출판사: '+publisher,
                                        foreground='gray', anchor=S, font=self.fontstyleMedium)
            self.publisherLabel.grid(row=1, column=2,sticky=W)
            self.clickLabels.append(self.publisherLabel)
            self.discountLabel = Label(self.bookListFrame, text='가격: '+B.getDiscount(),
                                       foreground='#1c2e75', anchor=S, font=self.fontstyleMedium)
            self.discountLabel.grid(row=1, column=3,sticky=W)
            self.clickLabels.append(self.discountLabel)
            description = B.getDescription().replace("\n", " / ")[:200] + ' ... '
            self.discripterLabel = Label(self.bookListFrame, text=description,
                                         justify=LEFT,
                                         anchor=S, font=self.fontstyleSmall, wraplength=700)
            self.discripterLabel.grid(row=2, column=1, columnspan=3, sticky=W)
            self.clickLabels.append(self.discripterLabel)
            # self.bookListBox.insert(END, self.bookListFrame)
            for label in self.clickLabels:
                label.bind("<Button-1>", bookClickFunc[idx])

    def __init__(self):
        self.window = Tk()
        self.window.title('read a book')
        self.window.geometry('1000x800')
        self.fontstyleBig = font.Font(self.window, size=20, weight='bold', family='맑은 고딕')
        self.fontstyleMedium = font.Font(self.window, size=15, weight='bold', family='맑은 고딕')
        self.fontstyleSmall = font.Font(self.window, size=10, weight='bold', family='맑은 고딕')



        self.window.mainloop()

SearchBookGUI()