import os
import pytest
import app as global_app
from models.book import Book
from models.client import Client
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
        db.session.commit()
    return global_app.app


def pytest_sessionfinish(session, exitstatus):
    if os.path.exists(DB_TEST):
        os.remove(DB_TEST)
