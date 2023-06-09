import tkinter
from tkinter import *
from tkinter import font
import GlobalWindow
import BookInformationFramework
import framework
import internetbook
import BookClass
import myBookListFramework
import MapFramework
import spam

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
        self.searchFrame = tkinter.Frame(GlobalWindow.window)
        self.searchFrame.pack()
        self.searchLabel = Label(self.searchFrame, text="책 제목으로 검색", font=self.fontstyleBig)
        self.searchLabel.grid(row=0, column=1)
        self.searchEntry = Entry(self.searchFrame, font=self.fontstyleBig)
        self.searchEntry.grid(row=0, column=2)
        self.searchButton = Button(self.searchFrame, text="검색", font=self.fontstyleBig,
                                   command=self.getBookDataFromTITLE, borderwidth=5)
        self.searchButton.grid(row=0, column=3)
        self.drawMain()
    def drawMain(self):
        # l = internetbook.getBookDataFromTitle('a')
        # GlobalWindow.myBookList[0].append(BookClass.Book(l[0]))
        # l = internetbook.getBookDataFromTitle('a')
        # GlobalWindow.myBookList[0].append(BookClass.Book(l[1]))
        # l = internetbook.getBookDataFromTitle('d')
        # GlobalWindow.myBookList[0].append(BookClass.Book(l[0]))
        # l = internetbook.getBookDataFromTitle('d')
        # GlobalWindow.myBookList[0].append(BookClass.Book(l[1]))
        # l = internetbook.getBookDataFromTitle('w')
        # GlobalWindow.myBookList[0].append(BookClass.Book(l[0]))
        # l = internetbook.getBookDataFromTitle('w')
        # GlobalWindow.myBookList[0].append(BookClass.Book(l[1]))
        # l = internetbook.getBookDataFromTitle('r')
        # GlobalWindow.myBookList[0].append(BookClass.Book(l[0]))
        # l = internetbook.getBookDataFromTitle('r')
        # GlobalWindow.myBookList[0].append(BookClass.Book(l[1]))

        self.myBooklistFrame = tkinter.Frame(GlobalWindow.window)
        self.myBookList = []
        self.myBooklistFrame.pack()
        white = 20
        self.pastClickList = []
        self.past = Label(self.myBooklistFrame, highlightbackground='black', highlightthickness=5,
                          width=55, height=30, bg='#bfd9c6')
        self.pastClickList.append(self.past)
        self.past.pack(side="left", padx=white, pady=2 * white)
        self.past.propagate(False)
        self.childPast = Label(self.past, bg='#bfd9c6')
        self.pastClickList.append(self.childPast)
        self.childPast.pack()
        self.pastText = Label(self.childPast, text='과거에\n읽었던 책',
                              font=self.fontstyleBig, bg='#bfd9c6')
        self.pastClickList.append(self.pastText)
        self.pastText.pack(pady=white * 2)
        self.imageLabelPast = Frame(self.childPast, bg='#bfd9c6')
        self.pastClickList.append(self.imageLabelPast)
        self.imageLabelPast.pack(pady=white * 2)
        for n in range(6):
            if len(GlobalWindow.myBookList[0]) > n:
                image = GlobalWindow.myBookList[0][n].getImage(150)
                l = Label(self.imageLabelPast, image=image, bg='black')
                l.grid(row=(n // 3), column=(n % 3), padx=15, pady=20)
                self.pastClickList.append(l)
            else:
                break

        def reliefThickPast(event):
            self.childPast.pack_forget()
            self.past['highlightbackground'] = 'gray'
            self.childPast.pack()

        def reliefThinPast(event):
            self.childPast.pack_forget()
            self.past['highlightbackground'] = 'black'
            self.childPast.pack()

        def click1(event):
            GlobalWindow.mark = 0
            framework.change_state(myBookListFramework)

        self.past.bind("<Enter>", reliefThickPast)
        self.past.bind("<Leave>", reliefThinPast)
        for i in self.pastClickList:
            i.bind("<Button-1>", click1)

        self.presentClickList = []
        self.present = Label(self.myBooklistFrame, highlightbackground='black', highlightthickness=5,
                             width=55, height=30, bg='#d8d9bf')
        self.presentClickList.append(self.present)
        self.present.pack(side="left", padx=white, pady=2 * white)
        self.present.propagate(0)
        self.childPresent = Label(self.present, bg='#d8d9bf')
        self.presentClickList.append(self.childPresent)
        self.childPresent.pack()
        self.presentText = Label(self.childPresent, text='현재에\n읽고 있는 책',
                                 font=self.fontstyleBig, bg='#d8d9bf')
        self.presentClickList.append(self.presentText)
        self.presentText.pack(pady=white * 2)

        self.imageLabelPresent = Frame(self.childPresent, bg='#d8d9bf')
        self.presentClickList.append(self.imageLabelPresent)
        self.imageLabelPresent.pack(pady=white * 2)
        for n in range(6):
            if len(GlobalWindow.myBookList[1]) > n:
                image = GlobalWindow.myBookList[1][n].getImage(150)
                l = Label(self.imageLabelPresent, image=image, bg='black')
                l.grid(row=(n // 3), column=(n % 3), padx=15, pady=20)
                self.presentClickList.append(l)
            else:
                break

        def reliefThickPresent(event):
            self.childPresent.pack_forget()
            self.present['highlightbackground'] = 'gray'
            self.childPresent.pack()

        def reliefThinPresent(event):
            self.childPresent.pack_forget()
            self.present['highlightbackground'] = 'black'
            self.childPresent.pack()

        def click2(event):
            GlobalWindow.mark = 1
            framework.change_state(myBookListFramework)

        self.present.bind("<Enter>", reliefThickPresent)
        self.present.bind("<Leave>", reliefThinPresent)
        for i in self.presentClickList:
            i.bind("<Button-1>", click2)

        self.futureClickList = []
        self.future = Label(self.myBooklistFrame,highlightbackground='black', highlightthickness=5,
                            width=55, height=30, bg='#d9bfc3')
        self.futureClickList.append(self.future)
        self.future.pack(side="left", padx=white, pady=2 * white)
        self.future.propagate(0)
        self.childFuture = Label(self.future, bg='#d9bfc3')
        self.futureClickList.append(self.childFuture)
        self.childFuture.pack()
        self.futureText = Label(self.childFuture, text='미래에\n읽고 싶은 책',
                                font=self.fontstyleBig, bg='#d9bfc3')
        self.futureClickList.append(self.futureText)
        self.futureText.pack(pady=white * 2)
        self.imageLabelFuture = Frame(self.childFuture, bg='#d9bfc3')
        self.futureClickList.append(self.imageLabelFuture)
        self.imageLabelFuture.pack(pady=white * 2)
        for n in range(6):
            if len(GlobalWindow.myBookList[2]) > n:
                image = GlobalWindow.myBookList[2][n].getImage(150)
                l = Label(self.imageLabelFuture, image=image, bg='black')
                l.grid(row=(n // 3), column=(n % 3), padx=15, pady=20)
                self.futureClickList.append(l)
            else:
                break

        def reliefThickFuture(event):
            self.childFuture.pack_forget()
            self.future['highlightbackground'] = 'gray'
            self.childFuture.pack()

        def reliefThinFuture(event):
            self.childFuture.pack_forget()
            self.future['highlightbackground'] = 'black'
            self.childFuture.pack()

        def click3(event):
            GlobalWindow.mark = 2
            framework.change_state(myBookListFramework)

        self.future.bind("<Enter>", reliefThickFuture)
        self.future.bind("<Leave>", reliefThinFuture)
        for i in self.futureClickList:
            i.bind("<Button-1>", click3)

        self.goMapButton = Button(GlobalWindow.window, text='서점 위치 검색', font=self.fontstyleBig,
                                  command=self.pressMap, borderwidth=5)
        self.goMapButton.pack()

    def pressMap(self):
        framework.change_state(MapFramework)

    def exit(self):
        self.searchFrame.destroy()
        for frame in self.bookListFrames:
            frame.destroy()
        self.myBooklistFrame.destroy()
        self.goMapButton.destroy()

    def pause(self):
        self.searchFrame.pack_forget()
        for frame in self.bookListFrames:
            frame.pack_forget()
        self.goMapButton.pack_forget()

    def resume(self):
        self.searchFrame.pack()
        for frame in self.bookListFrames:
            frame.pack()
        for i, v in enumerate(self.images):
            self.imageLabels[i]['image'] = v

    def reset(self):
        for frame in self.bookListFrames:
            frame.destroy()
        self.againFrame.destroy()
        self.goMain.destroy()
        self.drawMain()


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
        title = self.searchEntry.get()
        print(title)
        self.goMain = Button(self.searchFrame, command=self.reset, text='메인으로',
                             font=self.fontstyleBig, borderwidth=5)
        self.goMain.grid(row=0, column=0)
        for bf in self.bookListFrames:
            bf.destroy()
        self.goMapButton.destroy()
        self.againFrame.destroy()
        self.againFrame = Frame(GlobalWindow.window)
        self.againFrame.pack()
        again = Label(self.againFrame, text='오류발생. 다시 시도해주세요.', font=self.fontstyleMedium)
        again.pack()
        if title == '':
            return
        bookDatas = internetbook.getBookDataFromTitle(title)
        bookClickFunc = [self.bookClickUp, self.bookClickDown]
        self.bookList = []
        self.bookListFrames = []
        self.imageLabels = []
        self.images = []
        if not bookDatas:
            i = Label(GlobalWindow.window, text='검색결과가 없습니다.', font=self.fontstyleMedium)
            self.bookListFrames.append(i)
            i.pack()
            self.againFrame.destroy()
            return
        for idx, bookData in enumerate(bookDatas):
            B = BookClass.Book(bookData)
            self.bookList.append(B)
            self.bookListFrame = Frame(GlobalWindow.window, relief="raised", borderwidth=3)
            self.bookListFrames.append(self.bookListFrame)
            self.bookListFrame.pack()
            self.clickLabels = []
            self.images.append(B.getImage(300))
            self.imageLabel = Label(self.bookListFrame, image=self.images[-1])
            self.imageLabel.grid(row=0, column=0, rowspan=3)
            self.imageLabels.append(self.imageLabel)
            self.clickLabels.append(self.imageLabel)
            title = B.getTitle()
            if title:
                if title and spam.strlen(title) > 20:
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
                self.discountLabel = Label(self.bookListFrame, text='가격: ' + B.getDiscount(),
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
            # self.bookListBox.insert(END, self.bookListFrame)
            for label in self.clickLabels:
                label.bind("<Button-1>", bookClickFunc[idx])
        self.searchEntry.delete(0, spam.strlen(self.searchEntry.get()))
        self.againFrame.destroy()

    def __init__(self):
        self.fontstyleBig = font.Font(GlobalWindow.window, size=30, weight='bold', family='맑은 고딕')
        self.fontstyleMedium = font.Font(GlobalWindow.window, size=20, weight='bold', family='맑은 고딕')
        self.fontstyleSmall = font.Font(GlobalWindow.window, size=10, weight='bold', family='맑은 고딕')
        self.bookListFrames = []
        self.againFrame = Frame(GlobalWindow.window)
