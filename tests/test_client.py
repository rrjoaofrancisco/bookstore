import pytest
from apis.client import Lending
from datetime import datetime


def test_should_get_client_books_without_fees(client, mocker):

    with mocker.patch.object(Lending, '_get_today', return_value=datetime(2021, 3, 21)):
        response = client.get("/clients/1/books")

        assert response.status_code == 200
        assert response.json == [{'book_id': 3, 'client_id': 1, 'created_at': '2021-03-20T00:00:00',
                                  'current_value': 10.0, 'devolution_date': '2021-03-23T00:00:00',
                                  'fee': 0.0, 'fine': 0.0, 'id': 1, 'value': 10.0}]


def test_should_get_client_books_with_3_days_fee(client, mocker):

    with mocker.patch.object(Lending, '_get_today', return_value=datetime(2021, 3, 25)):
        response = client.get("/clients/1/books")

        assert response.status_code == 200
        assert response.json == [{'book_id': 3, 'client_id': 1, 'created_at': '2021-03-20T00:00:00',
                                  'current_value': 10.34, 'devolution_date': '2021-03-23T00:00:00',
                                  'fee': 0.2, 'fine': 3.0, 'id': 1, 'value': 10.0}]


def test_should_get_client_books_with_3_days_fee_2(client, mocker):

    with mocker.patch.object(Lending, '_get_today', return_value=datetime(2021, 3, 24)):
        response = client.get("/clients/1/books")

        assert response.status_code == 200
        assert response.json == [{'book_id': 3, 'client_id': 1, 'created_at': '2021-03-20T00:00:00',
                                  'current_value': 10.32, 'devolution_date': '2021-03-23T00:00:00',
                                  'fee': 0.2, 'fine': 3.0, 'id': 1, 'value': 10.0}]


def test_should_get_client_books_with_5_days_fee(client, mocker):

    with mocker.patch.object(Lending, '_get_today', return_value=datetime(2021, 3, 27)):
        response = client.get("/clients/1/books")

        assert response.status_code == 200
        assert response.json == [{'book_id': 3, 'client_id': 1, 'created_at': '2021-03-20T00:00:00',
                                  'current_value': 10.66, 'devolution_date': '2021-03-23T00:00:00',
                                  'fee': 0.4, 'fine': 5.0, 'id': 1, 'value': 10.0}]


def test_should_get_client_books_with_5_days_fee_2(client, mocker):

    with mocker.patch.object(Lending, '_get_today', return_value=datetime(2021, 3, 28)):
        response = client.get("/clients/1/books")

        assert response.status_code == 200
        assert response.json == [{'book_id': 3, 'client_id': 1, 'created_at': '2021-03-20T00:00:00',
                                  'current_value': 10.7, 'devolution_date': '2021-03-23T00:00:00',
                                  'fee': 0.4, 'fine': 5.0, 'id': 1, 'value': 10.0}]


def test_should_get_client_books_with_more_than_5_days_fee(client, mocker):

    with mocker.patch.object(Lending, '_get_today', return_value=datetime(2021, 3, 31)):
        response = client.get("/clients/1/books")

        assert response.status_code == 200
        assert response.json == [{'book_id': 3, 'client_id': 1, 'created_at': '2021-03-20T00:00:00',
                                  'current_value': 11.18, 'devolution_date': '2021-03-23T00:00:00',
                                  'fee': 0.6, 'fine': 7.0, 'id': 1, 'value': 10.0}]


def test_should_get_client_books_with_more_than_5_days_fee_2(client, mocker):

    with mocker.patch.object(Lending, '_get_today', return_value=datetime(2021, 3, 30)):
        response = client.get("/clients/1/books")

        assert response.status_code == 200
        assert response.json == [{'book_id': 3, 'client_id': 1, 'created_at': '2021-03-20T00:00:00',
                                  'current_value': 11.12, 'devolution_date': '2021-03-23T00:00:00',
                                  'fee': 0.6, 'fine': 7.0, 'id': 1, 'value': 10.0}]
