import tkinter
from tkinter import *
from tkinter import font
import GlobalWindow
import BookInformationFramework
import framework
import internetbook
import BookClass

GUI = None


def enter():
    global GUI
    GUI = SearchBookGUI()
    GUI.enter()


def pause():
    GUI.pause()


def resume():
    GUI.resume()


def exit():
    GUI.exit()


class SearchBookGUI:
    bookImageHeight = 300

    def enter(self):
        bookDatas = internetbook.getBookDataFromTitle('python')
        b = BookClass.Book(bookDatas[0])
        GlobalWindow.myBookList[0].append(b)

        # xml 파일 읽어서 global 변수인 MyBookList에 넣기
        self.searchFrame = tkinter.Frame(GlobalWindow.window)
        self.searchFrame.pack()
        self.searchLabel = Label(self.searchFrame, text="책 제목으로 검색", font=self.fontstyleBig)
        self.searchLabel.pack(side='left')
        self.searchEntry = Entry(self.searchFrame, font=self.fontstyleBig)
        self.searchEntry.pack(side='left')
        self.searchButton = Button(self.searchFrame, text="검색", font=self.fontstyleBig,
                                   command=self.getBookDataFromTITLE)
        self.searchButton.pack(side='left')

        self.myBooklistFrame = tkinter.Frame(GlobalWindow.window)
        self.myBookList = []
        self.myBooklistFrame.pack()
        white = 20
        self.past = Label(self.myBooklistFrame, relief='solid',
                          borderwidth=3, width=55, height=30, bg='#bfd9c6')
        self.past.pack(side="left", padx=white, pady=2 * white)
        self.past.propagate(0)
        self.pastText = Label(self.past, text='과거에\n읽었던 책',
                              font=self.fontstyleBig, bg='#bfd9c6')
        self.pastText.pack(pady=white*2)
        self.imageLabelPast = Frame(self.past)
        self.imageLabelPast.pack(pady=white*2)
        for n in range(6):
            if len(GlobalWindow.myBookList[0]) > n:
                image = GlobalWindow.myBookList[0][n].getImage(150)
                Label(self.imageLabelPast, image=image).grid(row=(n//3), column=n)
            else:
                break

        print()



        self.present = Label(self.myBooklistFrame, relief='solid',
                             borderwidth=3, width=55, height=30, bg='#d8d9bf')
        self.present.pack(side="left", padx=white, pady=2 * white)
        self.present.propagate(0)
        self.presentText = Label(self.present, text='현재에\n읽고 있는 책',
                                 font=self.fontstyleBig, bg='#d8d9bf')
        self.presentText.pack(pady=white*2)

        self.future = Label(self.myBooklistFrame, relief='solid',
                            borderwidth=3, width=55, height=30, bg='#d9bfc3')
        self.future.pack(side="left", padx=white, pady=2 * white)
        self.future.propagate(0)
        self.futureText = Label(self.future, text='미래에\n읽고 싶은 책',
                                font=self.fontstyleBig, bg='#d9bfc3')
        self.futureText.pack(pady=white*2)

    def exit(self):
        for frame in self.bookListFrames:
            frame.destroy()
        self.searchFrame.destroy()

    def pause(self):
        for frame in self.bookListFrames:
            frame.pack_forget()
        self.searchFrame.pack_forget()

    def resume(self):
        for frame in self.bookListFrames:
            frame.pack()
        self.searchFrame.pack()

    def bookClickUp(self, event):
        print("위쪽 책 선택")
        GlobalWindow.book = self.bookList[0]
        framework.push_state(BookInformationFramework)

    def bookClickDown(self, event):
        print("아래쪽 책 선택")
        GlobalWindow.book = self.bookList[1]
        framework.push_state(BookInformationFramework)

    def getBookDataFromTITLE(self):
        print('버튼 눌림')
        self.myBooklistFrame.pack_forget()
        title = (self.searchEntry.get())
        bookDatas = internetbook.getBookDataFromTitle(title)
        bookClickFunc = [self.bookClickUp, self.bookClickDown]
        self.bookList = []
        self.bookListFrames = []
        for idx, bookData in enumerate(bookDatas):
            B = BookClass.Book(bookData)
            self.bookList.append(B)
            self.bookListFrame = Frame(GlobalWindow.window, relief="raised", borderwidth=3)
            self.bookListFrames.append(self.bookListFrame)
            self.bookListFrame.pack()
            self.clickLabels = []
            self.imageLabel = Label(self.bookListFrame, image=B.getImage(300))
            self.imageLabel.grid(row=0, column=0, rowspan=3)
            self.clickLabels.append(self.imageLabel)
            title = B.getTitle()[:20] + ' ... '
            self.titleLabel = Label(self.bookListFrame, text=title, font=self.fontstyleBig, background='#E4F3F6')
            self.titleLabel.grid(row=0, column=1, columnspan=3, sticky=W)
            self.clickLabels.append(self.titleLabel)
            author = B.getAuthor()[:5] + ' ... '
            self.authorLabel = Label(self.bookListFrame, text='작가: ' + author, anchor=S, font=self.fontstyleMedium)
            self.authorLabel.grid(row=1, column=1, sticky=W)
            self.clickLabels.append(self.authorLabel)
            publisher = B.getPublisher()[:5] + ' ... '
            self.publisherLabel = Label(self.bookListFrame, text='출판사: ' + publisher,
                                        foreground='gray', anchor=S, font=self.fontstyleMedium)
            self.publisherLabel.grid(row=1, column=2, sticky=W)
            self.clickLabels.append(self.publisherLabel)
            self.discountLabel = Label(self.bookListFrame, text='가격: ' + B.getDiscount(),
                                       foreground='#1c2e75', anchor=S, font=self.fontstyleMedium)
            self.discountLabel.grid(row=1, column=3, sticky=W)
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
        self.fontstyleBig = font.Font(GlobalWindow.window, size=30, weight='bold', family='맑은 고딕')
        self.fontstyleMedium = font.Font(GlobalWindow.window, size=20, weight='bold', family='맑은 고딕')
        self.fontstyleSmall = font.Font(GlobalWindow.window, size=10, weight='bold', family='맑은 고딕')
