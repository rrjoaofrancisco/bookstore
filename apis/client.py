import os
from datetime import datetime, timedelta
from flask import request
from restplus import api
from werkzeug.exceptions import BadRequest
from flask_restplus import Resource, fields
from services.lending import LendingService
from services.book import BookService
from serializers.lending import lendings_schema, lending_schema

loan_days = os.environ.get('LOAN_DAYS')

ns_client = api.namespace('Clients & Lendings', description='Clients management and book lendings', path='/clients')

lending = ns_client.model('Lending', {
    'book_id': fields.Integer,
    # 'devolution_date': fields.String(default='31/12/2021')
})

def _valid_date(d, dt_format='%d/%m/%Y'):
    try:
        return datetime.strptime(d, dt_format)
    except ValueError:
        raise BadRequest(
            'Invalid date format. Should be {}'.format(dt_format))


@ns_client.route('/')
class Client(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(Client, self).__init__(api, args, kwargs)
        self.service = LendingService()

    def get(self):
        books = self.service.get_all()
        return lendings_schema.dump(books)


@ns_client.route('/<id>/books')
class Lending(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(Lending, self).__init__(api, args, kwargs)
        self.service = LendingService()
        self.book_service = BookService()


    @ns_client.expect(lending)
    def post(self, id):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        today = datetime.today()
        devolution_date = today + timedelta(int(loan_days))
        # devolution_date = _valid_date(json_data['devolution_date'])

        new_loading = self.service.insert(client_id=id, 
                                          book_id=json_data['book_id'], 
                                          created_at=today,
                                          devolution_date=devolution_date)

        book = self.book_service.get_by_id(json_data['book_id'])
        book.avaiable = False
        self.book_service.insert(book)


        return lending_schema.dump(new_loading), 201


    def get(self, id):
        lendings = self.service.get_by_client(id)
        return lendings_schema.dump(lendings)
