import pytest
from models.lending import Lending
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
    Lending.query.filter_by(id=response.json['id']).delete()
    book.avaiable = True
    db.session.add(book)
    db.session.commit()
