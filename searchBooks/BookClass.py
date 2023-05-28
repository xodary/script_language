class Book:
    def __init__(self, bookData):
        self.image = bookData['image']
        self.title = bookData['title']
        self.author = bookData['author']
        self.discount = bookData['discount']
        self.publisher = bookData['publisher']
        self.description = bookData['description']

    def getImage(self):
        return self.image

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
