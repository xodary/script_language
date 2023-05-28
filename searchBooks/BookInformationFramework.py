import GlobalWindow
from tkinter import font
from tkinter import *
from tkinter.scrolledtext import ScrolledText

GUI = None
def enter():
    global GUI
    GUI = BookInformationGUI()
    GUI.enter()
def exit():
    GUI.exit()


def pause():
    GUI.pause()


def resume():
    GUI.resume()

class BookInformationGUI:
    def enter(self):
        self.BookInfoFrame = Frame(GlobalWindow.window)
        self.BookInfoFrame.grid(row=0, column=0)
        self.imageLabel = Label(self.BookInfoFrame, image=self.myBook.getImage(500))
        self.imageLabel.grid(row=0, column=0, rowspan=6)
        self.titleLabel = Label(self.BookInfoFrame, text=self.myBook.getTitle(),
                                font=self.fontstyleBig, background='#E4F3F6')
        self.titleLabel.grid(row=0, column=1, sticky=W)
        self.authorLabel = Label(self.BookInfoFrame, text='작가: '+self.myBook.getAuthor(),
                                 anchor=S, font=self.fontstyleMedium)
        self.authorLabel.grid(row=1, column=1, sticky=W)
        self.publisherLabel = Label(self.BookInfoFrame, text='출판사: '+self.myBook.getPublisher(),
                                    foreground='gray', anchor=S, font=self.fontstyleMedium)
        self.publisherLabel.grid(row=2, column=1, sticky=W)
        self.discountLabel = Label(self.BookInfoFrame, text='가격: ' + self.myBook.getDiscount(),
                                   foreground='#1c2e75', anchor=S, font=self.fontstyleMedium)
        self.discountLabel.grid(row=3, column=1, sticky=W)
        self.discriptionFrame = Frame(self.BookInfoFrame)
        self.discriptionFrame.grid(row=4, column=1, sticky=W)
        self.scrollbar = Scrollbar(self.discriptionFrame)
        self.discripterLabel = ScrolledText(self.discriptionFrame, yscrollcommand=self.scrollbar,
                                    font=self.fontstyleSmall, width=50, height=10)
        self.discripterLabel.insert('end', self.myBook.getDescription())
        self.discripterLabel.pack(side='left')

    def exit(self):
        pass

    def resume(self):
        pass

    def exit(self):
        pass

    def __init__(self):
        self.fontstyleBig = font.Font(GlobalWindow.window, size=20, weight='bold', family='맑은 고딕')
        self.fontstyleMedium = font.Font(GlobalWindow.window, size=15, weight='bold', family='맑은 고딕')
        self.fontstyleSmall = font.Font(GlobalWindow.window, size=10, weight='bold', family='맑은 고딕')
        self.myBook = GlobalWindow.book