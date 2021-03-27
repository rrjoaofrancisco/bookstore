import os
import pytest
import app as global_app
from models.book import Book
from models.client import Client
from models.loan import Loan
from datetime import datetime
from database import db


basedir = os.path.abspath(os.path.dirname(__file__))
DB_TEST = os.path.join(basedir, "test.db")


@pytest.fixture(scope='session')
def app():
    global_app.create_app(
        global_app.app, f'sqlite:///{DB_TEST}')
    with global_app.app.app_context():
        assert db.engine.name == 'sqlite', 'Database for tests must be SQLITE!'
        db.session.add(Book(title='Livro 1', avaiable=True))
        db.session.add(Book(title='Livro 2', avaiable=True))
        db.session.add(Book(title='Livro 3', avaiable=True))
        db.session.add(Client(name='Cliente 1'))
        db.session.add(Client(name='Cliente 2'))
        db.session.add(Client(name='Cliente 3'))
        db.session.add(Loan(client_id=1,
                            book_id=3,
                            created_at=datetime(2021, 3, 20),
                            devolution_date=datetime(2021, 3, 23),
                            value=10.0))
        db.session.add(Loan(client_id=3,
                            book_id=2,
                            created_at=datetime(2021, 3, 27),
                            devolution_date=datetime(2021, 3, 30),
                            value=18.0))

        db.session.commit()
    return global_app.app


def pytest_sessionfinish(session, exitstatus):
    if os.path.exists(DB_TEST):
        os.remove(DB_TEST)
