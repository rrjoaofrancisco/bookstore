import pytest
import io


def test_should_get_books(client):

    response = client.get("/books")

    # Validate the response
    assert response.status_code == 200
    assert response.json == [{'avaiable': True, 'id': 1, 'title': 'Livro 1'}, {
        'avaiable': True, 'id': 2, 'title': 'Livro 2'}, {'avaiable': True, 'id': 3, 'title': 'Livro 3'}]
