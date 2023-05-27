from tkinter import*
from io import BytesIO
import urllib
import urllib.request
from PIL import Image,ImageTk
window=Tk()
window.geometry("1000x1000+500+200")

#openapi로 이미지 url을 가져옴.
url="https://shopping-phinf.pstatic.net/main_3429447/34294472620.20230524072206.jpg"
with urllib.request.urlopen(url) as u:
    raw_data=u.read()
im=Image.open(BytesIO(raw_data))
im.resize((100, 100))
image=ImageTk.PhotoImage(im)
Label(window, image=image, height=1000,width=1000).pack()
window.mainloop()
