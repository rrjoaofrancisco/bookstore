from datetime import datetime
from flask import request
from restplus import api
from werkzeug.exceptions import BadRequest
from flask_restplus import Resource, fields
from services.lending import LendingService
from serializers.lending import lendings_schema, lending_schema

ns_client = api.namespace('Clients & Lendings', description='Clients management and book lendings', path='/clients')

#Model required by flask_restplus for expect
lending = ns_client.model('Lending', {
    'book_id': fields.Integer,
    'devolution_date': fields.String(default='31/12/2021')
})

def _valid_date(d, dt_format='%d/%m/%Y'):
    try:
        return datetime.strptime(d, dt_format)
    except ValueError:
        raise BadRequest(
            'Formato invalido. Deve ser {}'.format(dt_format))


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

    @ns_client.expect(lending)
    def put(self, id):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        devolution_date = _valid_date(json_data['devolution_date'])

        # item_data = lending_schema.load(json_data)
        
        new_loading = self.service.insert(client_id=id, 
                                          book_id=json_data['book_id'], 
                                          devolution_date=devolution_date)

        return lending_schema.dump(new_loading), 201

        # Validate and deserialize input
        # try:
        #     data = quote_schema.load(json_data)
        # except ValidationError as err:
        #     return err.messages, 422
        # lending = self.service.insert(client_id=client_id)

    def get(self, id):
        lendings = self.service.get_by_client(id)
        return lendings_schema.dump(lendings)
