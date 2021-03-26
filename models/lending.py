from database import db
from datetime import datetime

class Lending(db.Model):
    __tablename__ = 'lending_books'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    devolution_date = db.Column(db.DateTime, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
