from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


def test_method_func(method):
    response = client.get(f"/{method}")
    if method.upper() == "GET" or "DELETE" or "OPTION" or "PUT":
        assert response.status_code == 200
    elif method.upper() == "POST":
        assert response.status_code == 201
    else:
        assert response.status_code == 406
    assert response.text == {"method": f"{method}".upper()}