import os
from datetime import datetime, timedelta
from flask import request, abort
from restplus import api
from flask_restplus import Resource
from services.lending import LendingService
from services.book import BookService
from serializers.lending import lendings_schema, lending_schema

loan_days = os.environ.get('LOAN_DAYS')

ns_client = api.namespace('Clients & Lendings', description='Clients management and book lendings', path='/clients')


@ns_client.route('/<id>/books')
class Lending(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(Lending, self).__init__(api, args, kwargs)
        self.service = LendingService()
        self.book_service = BookService()

    def _apply_fees(self, loan_json, today, dt_devolution):
        fine = 0.0
        fee = 0.0
        if today > dt_devolution:
            if today - dt_devolution <= timedelta(days=3):
                fine = 3.0
                fee = 0.2
            elif today - dt_devolution <= timedelta(days=5):
                fine = 5.0
                fee = 0.4
            else:
                fine = 7.0
                fee = 0.6
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
