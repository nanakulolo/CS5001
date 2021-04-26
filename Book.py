import numpy as np

# used to stored the data of each instance book in the books.csv file
class Book:
    def __init__(self, book_id=np.NaN, ISBN=np.NaN, title=np.NaN, author=np.NaN, publisher=np.NaN, language=np.NaN,
                 publication_date=np.NaN, status='available', holder=np.NaN, borrowed_date=np.NaN):
        self.book_id = book_id
        self.ISBN = ISBN
        self.title = title
        self.author = author
        self.publisher = publisher
        self.language = language
        self.publication_date = publication_date
        self.status = status
        self.holder = holder
        self.borrowed_date = borrowed_date




