
from io import BytesIO
from PIL import Image, ImageTk
import urllib
import urllib.request

class Book:
    def __init__(self, bookData):
        self.image = bookData['image']
        self.title = bookData['title']
        self.author = bookData['author']
        self.discount = bookData['discount']
        self.publisher = bookData['publisher']
        self.description = bookData['description']

    def getImage(self, height):
        with urllib.request.urlopen(self.image) as u:  # image 출력
            raw_data = u.read()
        openImage = Image.open(BytesIO(raw_data))
        resizedImage = openImage.resize(
            (int(height * openImage.size[0] / openImage.size[1]), height))
        self.outImage = ImageTk.PhotoImage(resizedImage)
        return self.outImage

    def getTitle(self):
        return self.title

    def getAuthor(self):
        return self.author

    def getDiscount(self):
        return self.discount

    def getPublisher(self):
        return self.publisher

    def getDescription(self):
        return self.description
