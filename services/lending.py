from database import db
from models.lending import Lending


class LendingService(object):

    def insert(self, **kwargs):
        new_lending = Lending(
            client_id=kwargs.get('client_id'),
            book_id=kwargs.get('book_id'),
            created_at=kwargs.get('created_at'),
            devolution_date=kwargs.get('devolution_date'),
            value=kwargs.get('value')
        )
        db.session.add(new_lending)
        db.session.commit()
        return new_lending

    def get_by_client(self, _client_id):
        return Lending.query.filter_by(client_id=_client_id)

    def get_by_book(self, _book_id):
        return Lending.query.filter_by(book_id=_book_id).first()
