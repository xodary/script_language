import tkinter.messagebox

import GlobalWindow
from tkinter import font
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import spam
import framework

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
        self.AllPage = Frame(GlobalWindow.window)
        self.AllPage.pack()
        self.BookInfoFrame = Frame(self.AllPage)
        self.BookInfoFrame.grid(row=0, column=0)
        self.imageLabel = Label(self.BookInfoFrame, image=self.myBook.getImage(500))
        self.imageLabel.grid(row=0, column=0, rowspan=6)
        title = self.myBook.getTitle()
        if title:
            if spam.strlen(title) > 20:
                title = title[:20]
            self.titleLabel = Label(self.BookInfoFrame, text=title,
                                    font=self.fontstyleBig, background='#E4F3F6')
            self.titleLabel.grid(row=0, column=1, sticky=W)
        author = self.myBook.getAuthor()
        if author:
            if spam.strlen(author) > 10:
                author = author[:10]
            self.authorLabel = Label(self.BookInfoFrame, text='작가: ' + author,
                                    anchor=S, font=self.fontstyleMedium)
            self.authorLabel.grid(row=1, column=1, sticky=W)
        publish = self.myBook.getPublisher()
        if publish:
            if spam.strlen(publish) > 10:
                publish = publish[:10]
            self.publisherLabel = Label(self.BookInfoFrame, text='출판사: ' + publish,
                                        foreground='gray', anchor=S, font=self.fontstyleMedium)
            self.publisherLabel.grid(row=2, column=1, sticky=W)
        discount = self.myBook.getDiscount()
        if discount:
            self.discountLabel = Label(self.BookInfoFrame, text='가격: ' + discount,
                                       foreground='#1c2e75', anchor=S, font=self.fontstyleMedium)
            self.discountLabel.grid(row=3, column=1, sticky=W)
        description = self.myBook.getDescription()
        if description:
            self.descriptionFrame = Frame(self.BookInfoFrame)
            self.descriptionFrame.grid(row=4, column=1, sticky=W)
            self.scrollbar = Scrollbar(self.descriptionFrame)
            self.descripterLabel = ScrolledText(self.descriptionFrame, yscrollcommand=self.scrollbar,
                                            font=self.fontstyleSmall, width=50, height=10)
            self.descripterLabel.insert('end', description)
            self.descripterLabel.pack(side='left')

        # 나의 책 리스트로 넣는다.
        self.checkboxFrame = Frame(self.AllPage)
        self.checkboxFrame.grid(row=1, column=0, sticky=W)
        self.checkboxList = []
        self.checkboxList.append(Button(self.checkboxFrame, text='과거에 읽은 책', font=self.fontstyleMedium,
                                        command=self.CheckPast, bg='white'))
        self.checkboxList[-1].grid(sticky=W, pady=5)
        self.checkboxList.append(Button(self.checkboxFrame, text='지금 읽고 있는 책', font=self.fontstyleMedium,
                                        command=self.CheckPresent, bg='white'))
        self.checkboxList[-1].grid(sticky=W, pady=5)
        self.checkboxList.append(Button(self.checkboxFrame, text='나중에 읽고 싶은 책', font=self.fontstyleMedium,
                                        command=self.CheckFuture, bg='white'))
        self.checkboxList[-1].grid(sticky=W, pady=5)
        for idx, l in enumerate(GlobalWindow.myBookList):
            for e in l:
                if self.myBook.getTitle() == e.getTitle():
                    self.myBook = e
                    self.checkboxList[idx]['bg'] = '#bad5ff'

        self.myMemoFrame = Frame(self.AllPage)
        self.myMemoFrame.grid(row=0, column=1, rowspan=2)
        self.myMemoTextFrame = Frame(self.myMemoFrame)
        self.myMemoTextFrame.pack(padx=20, pady=20)
        self.TextScrollbar = Scrollbar(self.myMemoTextFrame)
        self.myMemoText = ScrolledText(self.myMemoTextFrame, yscrollcommand=self.TextScrollbar.set,
                                       height=20, width=30, font=self.fontstyleMedium)
        self.myMemoText.insert('1.0',self.myBook.getMemo(),END)
        self.myMemoText.pack()
        self.saveButton = Button(self.myMemoFrame, font=self.fontstyleMedium,
                                 text='메모 저장', command=self.pressSave)
        self.saveButton.pack(padx=20, pady=20)

        self.exitButton = Button(self.AllPage, command=self.pressExitButton,
                                 text='뒤로가기', font=self.fontstyleMedium)
        self.exitButton.grid(row=0, column=2, sticky=NW, pady=20)

    def pause(self):
        pass
    def resume(self):
        pass

    def exit(self):
        self.AllPage.destroy()

    def pressSave(self):
        for l in GlobalWindow.myBookList:
            for b in l:
                if self.myBook == b:
                    b.setMemo(self.myMemoText.get('1.0', END))
                    print(b.getMemo())
                    return
        tkinter.messagebox.showinfo(title='책을 추가하세요.',
                                    message='메모를 남기기전에,\n'
                                            '먼저 나의 리스트에\n'
                                            '책을 추가해야 합니다.')

    def pressExitButton(self):
        framework.pop_state()

    def Check(self, n):
        if not self.myBook in GlobalWindow.myBookList[n]:
            self.checkboxList[n]['bg'] = '#bad5ff'
            GlobalWindow.myBookList[n].append(self.myBook)
        else:
            self.checkboxList[n]['bg'] = 'white'
            GlobalWindow.myBookList[n].remove(self.myBook)

    def Uncheck(self, n):
        if self.myBook in GlobalWindow.myBookList[n]:
            self.checkboxList[n]['bg'] = 'white'
            GlobalWindow.myBookList[n].remove(self.myBook)

    def CheckPast(self):
        self.Check(0)
        self.Uncheck(1)
        self.Uncheck(2)

    def CheckPresent(self):
        self.Check(1)
        self.Uncheck(0)
        self.Uncheck(2)

    def CheckFuture(self):
        self.Check(2)
        self.Uncheck(0)
        self.Uncheck(1)

    def __init__(self):
        self.fontstyleBig = font.Font(GlobalWindow.window, size=20, weight='bold', family='맑은 고딕')
        self.fontstyleMedium = font.Font(GlobalWindow.window, size=15, weight='bold', family='맑은 고딕')
        self.fontstyleSmall = font.Font(GlobalWindow.window, size=10, weight='bold', family='맑은 고딕')
        self.myBook = GlobalWindow.book
