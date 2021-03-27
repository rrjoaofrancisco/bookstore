from datetime import datetime, timedelta
from flask import abort
from restplus import api
from flask_restplus import Resource
from services.loan import LoanService
from services.book import BookService
from services.client import ClientService
from serializers.loan import loan_schema


ns_client = api.namespace('Clients & Loans', description='Clients management and book loans', path='/clients')


@ns_client.route('/<id>/books')
class Loan(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(Loan, self).__init__(api, args, kwargs)
        self.service = LoanService()
        self.book_service = BookService()
        self.client_service = ClientService()

    def _get_today(self):
        return datetime.today()

    def _apply_fees(self, loan_json, dt_devolution, value):
        today = self._get_today()
        fine = 0.0
        fee = 0.0
        current_value = value
        if today > dt_devolution:
            date_diff = today - dt_devolution
            days = date_diff.days
            if date_diff < timedelta(days=4):
                fine = 3.0
                fee = 0.2
            elif date_diff < timedelta(days=6):
                fine = 5.0
                fee = 0.4
            else:
                fine = 7.0
                fee = 0.6
            fee_value = ((days * fee) * value) / 100
            fine_value = (fine * value) / 100
            current_value = value + fee_value + fine_value
        loan_json['fine'] = fine
        loan_json['fee'] = fee
        loan_json['current_value'] = current_value

    def get(self, id):
        client = self.client_service.get_by_id(id)
        if not client:
            abort(404, 'Client not found')
        loans = self.service.get_by_client(id)
        response = []
        for loan in loans:
            loan_json = loan_schema.dump(loan)
            self._apply_fees(loan_json, loan.devolution_date, loan.value)
            response.append(loan_json)
        return response
