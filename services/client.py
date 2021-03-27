from models.client import Client
from database import db

class ClientService(object):

    def get_by_id(self, id):
        return Client.query.filter_by(id= id).first()
