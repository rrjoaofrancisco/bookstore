from database import db


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    lending_books = db.relationship('Loan', backref='client', lazy=True)
