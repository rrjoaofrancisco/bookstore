import pytest
from models.loan import Loan
from models.book import Book
from database import db


def test_should_get_books(client):

    response = client.get("/books")

    assert response.status_code == 200
    assert response.json == [{'avaiable': True, 'id': 1, 'title': 'Livro 1'}, {
        'avaiable': True, 'id': 2, 'title': 'Livro 2'}, {'avaiable': True, 'id': 3, 'title': 'Livro 3'}]


def test_should_reserve_book(client):
    response = client.post("/books/1/reserve",
                           headers={'accept': 'application/json'},
                           json={'client_id': 1,
                                 'reserve_date': '10/03/2021',
                                 'value': 10.0
                                 })

    assert response.status_code == 201
    assert response.json == {'book_id': 1, 'client_id': 1, 'created_at': '2021-03-10T00:00:00',
                             'devolution_date': '2021-03-13T00:00:00', 'id': response.json['id'], 'value': 10.0}
    book = Book.query.filter_by(id=response.json['book_id']).one()
    assert not book.avaiable
    Loan.query.filter_by(id=response.json['id']).delete()
    book.avaiable = True
    db.session.add(book)
    db.session.commit()


def test_should_not_reserve_book_no_input(client):
    response = client.post("/books/1/reserve",
                           headers={'accept': 'application/json'},
                           json={})

    assert response.status_code == 400
    assert response.json == {'message': 'No input data provided'}


def test_should_not_reserve_book_already_reserved(client):
    response = client.post("/books/2/reserve",
                           headers={'accept': 'application/json'},
                           json={'client_id': 1,
                                 'reserve_date': '10/03/2021',
                                 'value': 10.0
                                 })

    assert response.status_code == 400
    assert response.json == {'message': 'Book already reserved'}


def test_should_not_reserve_book_client_not_found(client):
    response = client.post("/books/1/reserve",
                           headers={'accept': 'application/json'},
                           json={'client_id': 4,
                                 'reserve_date': '10/03/2021',
                                 'value': 10.0
                                 })

    assert response.status_code == 404
    assert response.json == {'message': 'Book or Client not found'}


def test_should_not_reserve_book_book_not_found(client):
    response = client.post("/books/4/reserve",
                           headers={'accept': 'application/json'},
                           json={'client_id': 2,
                                 'reserve_date': '10/03/2021',
                                 'value': 10.0
                                 })

    assert response.status_code == 404
    assert response.json == {'message': 'Book or Client not found'}


def test_should_not_reserve_book_invalid_date(client):
    response = client.post("/books/1/reserve",
                           headers={'accept': 'application/json'},
                           json={'client_id': 2,
                                 'reserve_date': 'string',
                                 'value': 10.0
                                 })

    assert response.status_code == 400
    assert response.json == {'message': 'Invalid date format. Should be %d/%m/%Y'}
