from restplus import api
from flask_restplus import Resource
from services.book import BookService
from serializers.book import books_schema

ns_default = api.default_namespace

ns_book = api.namespace('Books', description='Books Management', path='/books')

@ns_book.route('/')
class Book(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(Book, self).__init__(api, args, kwargs)
        self.service = BookService()

    def get(self):
        books = self.service.get_all()
        return books_schema.dump(books)