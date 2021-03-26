import os
from datetime import datetime, timedelta
from flask import request, abort
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
})

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
        book_id = json_data['book_id']
        already_on_loan = self.service.get_by_book(book_id)
        if already_on_loan:
            abort(400, 'Book already on loan')
        today = datetime.today()
        devolution_date = today + timedelta(int(loan_days))

        new_loading = self.service.insert(client_id=id, 
                                          book_id=book_id, 
                                          created_at=today,
                                          devolution_date=devolution_date)

        book = self.book_service.get_by_id(book_id)
        book.avaiable = False
        self.book_service.insert(book)

        return lending_schema.dump(new_loading), 201


    def _apply_fees(self, loan_json, today, dt_devolution):
        fine = 0.0
        fee = 0.0
        if today > dt_devolution:
            if today - dt_devolution <= timedelta(days=3):
                loan_json['fine'] = 3.0
                loan_json['fee'] = 0.2
            elif today - dt_devolution <= timedelta(days=5):
                loan_json['fine'] = 5.0
                loan_json['fee'] = 0.4
            else:
                loan_json['fine'] = 7.0
                loan_json['fee'] = 0.6
        loan_json['fine'] = fine
        loan_json['fee'] = fee


    def get(self, id):
        lendings = self.service.get_by_client(id)
        today = datetime.today()
        response = []
        for loan in lendings:
            loan_json = lending_schema.dump(loan)
            self._apply_fees(loan_json,today,loan.devolution_date)
            response.append(loan_json)
        return response
