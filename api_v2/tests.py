import json
import os
import pathlib

import pytest
import requests
from django.core.management import call_command
from django.test import Client

root = pathlib.Path(__file__).parent


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "db_init.yaml")


@pytest.mark.django_db
def test_get_books():
    c = Client()
    response = c.get("/api/2/books")
    response_data = response.json()
    expected_response_data = json.load(open(root / "fixtures/GET_books.json"))
    assert response.status_code == 200
    assert response_data == expected_response_data


@pytest.mark.django_db
def test_post_books():
    c = Client()
    data = {
        "title": "Kobzar",
        "author": "Shevchenko",
        "genre": "drama",
        "publication_date": "2020-01-01",
    }
    json_data = json.dumps(data)
    response = c.post("/api/2/books", data=json_data, content_type="application/json")
    response_data = response.json()
    expected_response_data = {
        "id": 3,
        "title": "Kobzar",
        "author": "Shevchenko",
        "genre": "drama",
        "publication_date": "2020-01-01",
    }
    assert response.status_code == 201
    assert response_data == expected_response_data


@pytest.mark.django_db
def test_post_books_no_title():
    c = Client()
    data = {"author": "Shevchenko", "genre": "drama", "publication_date": "2020-01-01"}
    json_data = json.dumps(data)
    response = c.post("/api/2/books", data=json_data, content_type="application/json")
    response_data = response.json()
    expected_response_data = {"title": ["This field is required."]}
    assert response.status_code == 400
    assert response_data == expected_response_data


@pytest.mark.django_db
def test_get_books_id():
    c = Client()
    response = c.get("/api/2/books/1")
    response_data = response.json()
    expected_response_data = json.load(open(root / "fixtures/GET_books_id.json"))
    assert response.status_code == 200
    assert response_data == expected_response_data


@pytest.mark.django_db
def test_get_books_no_id():
    c = Client()
    response = c.get("/api/2/books/100")
    response_data = response.json()
    expected_response_data = {"detail": "Not found."}
    assert response.status_code == 404
    assert response_data == expected_response_data


@pytest.mark.django_db
def test_delete_books_id():
    c = Client()
    response = c.delete("/api/2/books/1")
    response_data = response.json()
    expected_response_data = {"success": "The book has been deleted"}
    assert response.status_code == 200
    assert response_data == expected_response_data


@pytest.mark.django_db
def test_get_authors():
    c = Client()
    response = c.get("/api/2/authors")
    response_data = response.json()
    expected_response_data = json.load(open(root / "fixtures/GET_authors.json"))
    assert response.status_code == 200
    assert response_data == expected_response_data


@pytest.mark.django_db
def test_get_authors_id():
    c = Client()
    response = c.get("/api/2/authors/1")
    response_data = response.json()
    expected_response_data = json.load(open(root / "fixtures/GET_authors_id.json"))
    assert response.status_code == 200
    assert response_data == expected_response_data


@pytest.mark.django_db
def test_get_authors_no_id():
    c = Client()
    response = c.get("/api/2/authors/100")
    response_data = response.json()
    expected_response_data = {"detail": "Not found."}
    assert response.status_code == 404
    assert response_data == expected_response_data


@pytest.mark.django_db
def test_put_books_id():
    c = Client()
    data = {
        "genre": "drama",
    }
    json_data = json.dumps(data)
    response = c.put("/api/2/books/1", data=json_data, content_type="application/json")
    response_data = response.json()
    expected_response_data = {
        "id": 1,
        "title": "book_1",
        "author": "author_1",
        "genre": "drama",
        "publication_date": "2000-01-01",
    }
    assert response.status_code == 200
    assert response_data == expected_response_data


# e2e tests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000/api/2/")


def test_get_books_e2e():
    r = requests.get(BASE_URL + "books")
    assert r.status_code == 200


def test_post_books_e2e():
    data = {
        "title": "Kobzar",
        "author": "Shevchenko",
        "genre": "drama",
        "publication_date": "2020-01-01",
    }
    response = requests.post(BASE_URL + "books", json=data)
    assert response.status_code == 201


def test_get_book_id_e2e():
    response = requests.get(BASE_URL + "books/1")
    assert response.status_code == 200


def test_get_book_no_id_e2e():
    response = requests.get(BASE_URL + "books/10000")
    response_data = response.json()
    expected_response_data = {"detail": "Not found."}
    assert response.status_code == 404
    assert response_data == expected_response_data


def test_get_authors_no_id_e2e():
    response = requests.get(BASE_URL + "authors/10000")
    response_data = response.json()
    expected_response_data = {"detail": "Not found."}
    assert response.status_code == 404
    assert response_data == expected_response_data
