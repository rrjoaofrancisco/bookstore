from datetime import datetime
from database import db
from models.lending import Lending

class LendingService(object):

    def insert(self, **kwargs):
        new_lending = Lending(
            client_id = kwargs.get('client_id'),
            book_id = kwargs.get('book_id'),
            created_at = datetime.now(),
            devolution_date = kwargs.get('devolution_date')
        )
        db.session.add(new_lending)
        db.session.commit()
        return new_lending

    def get_by_client(self, client_id):
        return Lending.query.filter_by(client_id=client_id)
