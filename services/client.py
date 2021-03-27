from models.client import Client


class ClientService(object):

    def get_by_id(self, _id):
        return Client.query.filter_by(id=_id).first()
