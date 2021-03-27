from models.book import Book
from database import db


class BookService(object):

    def get_all(self):
        return Book.query.all()

    def get_by_id(self, id):
        return Book.query.filter_by(id=id).first()

    def insert(self, book):
        db.session.add(book)
        db.session.commit()
        return book
