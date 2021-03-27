import os
from datetime import datetime, timedelta
from flask import request, abort
from restplus import api
from flask_restplus import Resource, fields
from services.book import BookService
from services.lending import LendingService
from services.client import ClientService
from serializers.book import books_schema
from serializers.lending import lending_schema
from werkzeug.exceptions import BadRequest

reserve_days = os.environ.get('RESERVE_DAYS')

ns_book = api.namespace('Books & Reserves', description='Books management and reserves', path='/books')

lending = ns_book.model('Lending', {
    'client_id': fields.Integer,
    'reserve_date': fields.String,
    'value': fields.Float
})


def _valid_date(d, dt_format='%d/%m/%Y'):
    try:
        return datetime.strptime(d, dt_format)
    except ValueError:
        raise BadRequest(
            'Invalid date format. Should be {}'.format(dt_format))


@ns_book.route('/')
class Book(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(Book, self).__init__(api, args, kwargs)
        self.service = BookService()

    def get(self):
        books = self.service.get_all()
        return books_schema.dump(books)


@ns_book.route('/<id>/reserve')
class BookReserve(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(BookReserve, self).__init__(api, args, kwargs)
        self.service = LendingService()
        self.book_service = BookService()
        self.client_service = ClientService()

    @ns_book.expect(lending)
    def post(self, id):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        already_on_loan = self.service.get_by_book(id)
        if already_on_loan:
            abort(400, 'Book already reserved')
        book = self.book_service.get_by_id(id)
        client = self.client_service.get_by_id(json_data['client_id'])

        if book and client:
            reserve_date = _valid_date(json_data['reserve_date'])

            devolution_date = reserve_date + timedelta(int(reserve_days))

            new_loading = self.service.insert(client_id=client.id, 
                                            book_id=book.id, 
                                            created_at=reserve_date,
                                            devolution_date=devolution_date,
                                            value=json_data['value'])

            book.avaiable = False
            self.book_service.insert(book)

            return lending_schema.dump(new_loading), 201
        abort(404, 'Book or Client not found.')