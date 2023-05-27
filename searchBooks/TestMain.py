import tkinter
from tkinter import *
from io import BytesIO
from tkinter import font
from PIL import Image,ImageTk
import urllib
import urllib.request
import internetbook

class SearchBookGUI:
    bookImageHeight = 300
    def getBookDataFromTITLE(self):
        print('버튼 눌림')
        self.canvas.delete()
        title = (self.searchEntry.get())
        bookData = internetbook.getBookDataFromTitle(title)
        self.bookListFrame = tkinter.Frame(self.window)
        self.bookListFrame.pack()
        with urllib.request.urlopen(bookData['image']) as u:        # image 출력
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        re_im = im.resize((int(SearchBookGUI.bookImageHeight * im.size[0] / im.size[1]),
                           SearchBookGUI.bookImageHeight))
        self.image = ImageTk.PhotoImage(re_im)
        self.imageLabel = Label(self.bookListFrame, image=self.image)
        self.imageLabel.grid(row=0, column=0, rowspan=3)
        self.titleLabel = Label(self.bookListFrame, text=bookData['title'],font=self.fontstyleBig)
        self.titleLabel.grid(row=0, column=1, columnspan=3, sticky=W)
        self.authorLabel = Label(self.bookListFrame, text='작가: '+bookData['author'],anchor=S, font=self.fontstyleMedium)
        self.authorLabel.grid(row=1, column=1, sticky=W)
        self.publisherLabel = Label(self.bookListFrame, text='출판사: '+bookData['publisher'],
                                    foreground='gray', anchor=S, font=self.fontstyleMedium)
        self.publisherLabel.grid(row=1, column=2,sticky=W)
        self.discountLabel = Label(self.bookListFrame, text='가격: '+bookData['discount'],
                                   foreground='#1c2e75', anchor=S, font=self.fontstyleMedium)
        self.discountLabel.grid(row=1, column=3,sticky=W)
        self.text = bookData['description']
        self.text = self.text.replace("\n", " / ")
        self.text = self.text[:200] + ' ... '
        self.discripterLabel = Label(self.bookListFrame, text=self.text,
                                     justify=LEFT,
                                     anchor=S, font=self.fontstyleSmall, wraplength=700)
        self.discripterLabel.grid(row=2, column=1, columnspan=3, sticky=W)


    def __init__(self):
        self.window = Tk()
        self.window.title('read a book')
        self.window.geometry('1000x800')
        self.fontstyleBig = font.Font(self.window, size=20, weight='bold', family='맑은 고딕')
        self.fontstyleMedium = font.Font(self.window, size=15, weight='bold', family='맑은 고딕')
        self.fontstyleSmall = font.Font(self.window, size=10, weight='bold', family='맑은 고딕')
        self.bookLabels = []
        self.searchFrame = tkinter.Frame(self.window)
        self.searchFrame.pack(side='top')
        self.canvas = Canvas(self.searchFrame, bg='white', width=400, height=300)
        self.searchLabel = Label(self.searchFrame, text="책 제목으로 검색", font=self.fontstyleBig)
        self.searchLabel.pack(side='left')
        self.searchEntry = Entry(self.searchFrame, font=self.fontstyleBig)
        self.searchEntry.pack(side='left')
        self.searchButton = Button(self.searchFrame, text="검색", font=self.fontstyleBig, command=self.getBookDataFromTITLE)
        self.searchButton.pack(side='left')

        self.window.mainloop()

SearchBookGUI()