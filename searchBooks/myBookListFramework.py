from tkinter import *
from tkinter import font
import spam
import GlobalWindow
import framework
import SearchFramework
import BookInformationFramework

GUI = None

def enter():
    global GUI
    GUI = myBookListGUI()
    GUI.enter()

def pause():
    GUI.pause()

def resume():
    GUI.resume()

def exit():
    GUI.exit()

class myBookListGUI:
    fontstyleBig = font.Font(GlobalWindow.window, size=30, weight='bold', family='맑은 고딕')
    fontstyleMedium = font.Font(GlobalWindow.window, size=20, weight='bold', family='맑은 고딕')
    fontstyleSmall = font.Font(GlobalWindow.window, size=10, weight='bold', family='맑은 고딕')

    def exit(self):
        self.ListFrame.destroy()
        self.ExitButton.destroy()
        self.leftButton.destroy()
        self.rightButton.destroy()

    def pause(self):
        self.ListFrame.pack_forget()
        self.ExitButton.place_forget()
        self.leftButton.place_forget()
        self.rightButton.place_forget()

    def resume(self):
        self.setInfo()
        self.ListFrame.pack(pady=30)
        self.ExitButton.place(x=1650, y=50)
        self.leftButton.place(x=800 - 70, y=950)
        self.rightButton.place(x=800 + 70, y=950)


    def pressedExitButton(self):
        framework.change_state(SearchFramework)

    def first(self, event):
        print('첫번째 선택')
        GlobalWindow.book = self.mybookList[self.index * 3 + 0]
        framework.push_state(BookInformationFramework)

    def second(self, event):
        print('두번째 선택')
        GlobalWindow.book = self.mybookList[self.index * 3 + 1]
        framework.push_state(BookInformationFramework)

    def third(self, event):
        print('세번째 선택')
        GlobalWindow.book = self.mybookList[self.index * 3 + 2]
        framework.push_state(BookInformationFramework)

    def setInfo(self):
        self.mybookList = GlobalWindow.myBookList[GlobalWindow.mark]
        self.mybookLen = len(self.mybookList)
        self.ListFrame = Frame(GlobalWindow.window)
        self.ListFrame.pack(pady=30)
        self.myBooksFrame = Frame(self.ListFrame)
        self.myBooksFrame.pack()
        bookClickFunc = [self.first, self.second, self.third]
        self.ExitButton = Button(GlobalWindow.window, command=self.pressedExitButton,
                                 text='뒤로 가기', font=self.fontstyleMedium)
        self.ExitButton.place(x=1650, y=50)
        self.leftButton = Button(GlobalWindow.window, text='뒤로',
                                 font=self.fontstyleMedium, command=self.pressLeftButton)
        self.leftButton.place(x=800 - 70, y=950)
        self.rightButton = Button(GlobalWindow.window, text='앞으로',
                                  font=self.fontstyleMedium, command=self.pressRightButton)
        self.rightButton.place(x=800 + 70, y=950)
        if self.mybookLen == 0:
            Label(self.ListFrame, text='아무것도 없습니다.\n먼저 책을 추가해보세요.',
                  font=self.fontstyleBig).pack()
            return
        self.bookList = []
        self.bookListFrames = []
        self.imageLabels = []
        self.images = []
        self.clickLabels3 = []
        for idx, B in enumerate(self.mybookList):
            self.bookList.append(B)
            self.bookListFrame = Frame(self.myBooksFrame, relief="raised", borderwidth=3)
            self.bookListFrames.append(self.bookListFrame)
            self.clickLabels = []
            self.images.append(B.getImage(300))
            self.imageLabel = Label(self.bookListFrame, image=self.images[-1])
            self.imageLabel.grid(row=0, column=0, rowspan=3)
            self.imageLabels.append(self.imageLabel)
            self.clickLabels.append(self.imageLabel)
            title = B.getTitle()
            if title:
                if spam.strlen(title) > 20:
                    title = title[:20] + ' ... '
                self.titleLabel = Label(self.bookListFrame, text=title, font=self.fontstyleBig, background='#E4F3F6')
                self.titleLabel.grid(row=0, column=1, columnspan=3, sticky=W)
                self.clickLabels.append(self.titleLabel)
            author = B.getAuthor()
            if author:
                if spam.strlen(author) > 5:
                    author = author[:5] + ' ... '
                self.authorLabel = Label(self.bookListFrame, text='작가: ' + author, anchor=S, font=self.fontstyleMedium)
                self.authorLabel.grid(row=1, column=1, sticky=W)
                self.clickLabels.append(self.authorLabel)
            publisher = B.getPublisher()
            if publisher:
                if spam.strlen(publisher) > 5:
                    publisher = publisher[:5] + ' ... '
                self.publisherLabel = Label(self.bookListFrame, text='출판사: ' + publisher,
                                        foreground='gray', anchor=S, font=self.fontstyleMedium)
                self.publisherLabel.grid(row=1, column=2, sticky=W)
                self.clickLabels.append(self.publisherLabel)
            discount = B.getDiscount()
            if discount:
                self.discountLabel = Label(self.bookListFrame, text='가격: ' + discount,
                                           foreground='#1c2e75', anchor=S, font=self.fontstyleMedium)
                self.discountLabel.grid(row=1, column=3, sticky=W)
                self.clickLabels.append(self.discountLabel)
            description = B.getDescription()
            if description:
                description = description.replace("\n", " / ")
                if spam.strlen(description) > 200:
                    description = description[:200] + ' ... '
                self.discripterLabel = Label(self.bookListFrame, text=description,
                                            justify=LEFT,
                                            anchor=S, font=self.fontstyleSmall, wraplength=700)
                self.discripterLabel.grid(row=2, column=1, columnspan=3, sticky=W)
                self.clickLabels.append(self.discripterLabel)
            self.clickLabels3.append(self.clickLabels)
            # self.bookListBox.insert(END, self.bookListFrame)

        for i in range(3):
            if self.index * 3 + i < self.mybookLen:
                self.bookListFrames[i].pack()
        for idx in range(3):
            if self.index * 3 + idx < len(self.clickLabels3):
                for click in self.clickLabels3[self.index * 3 + idx]:
                    click.bind("<Button-1>", bookClickFunc[idx])

    def __init__(self):
        pass

    def enter(self):
        self.index = 0
        self.setInfo()


    def pressLeftButton(self):
        if 0 <= self.index - 1:
            for i in range(3):
                if self.index * 3 + i < self.mybookLen:
                    self.bookListFrames[self.index * 3 + i].pack_forget()
                else:
                    break
            self.index -= 1
            self.show3books()
    def pressRightButton(self):
        if (self.index + 1) * 3 < self.mybookLen:
            for i in range(3):
                self.bookListFrames[self.index * 3 + i].pack_forget()
            self.index += 1
            self.show3books()




    def show3books(self):
        for i in range(3):
            if self.index * 3 + i < self.mybookLen:
                self.bookListFrames[self.index * 3 + i].pack()
            else:
                break
        bookClickFunc = [self.first, self.second, self.third]
        for idx in range(3):
            if self.index * 3 + idx < len(self.clickLabels3):
                for click in self.clickLabels3[self.index * 3 + idx]:
                    click.bind("<Button-1>", bookClickFunc[idx])

