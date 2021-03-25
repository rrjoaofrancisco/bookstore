from database import db


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    avaiable = db.Column(db.Boolean, nullable=False, default=True)
