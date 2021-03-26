from models.book import Book

class BookService(object):

    def get_all(self):
        return Book.query.all()
