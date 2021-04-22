from fastapi.testclient import TestClient
import pytest
from task_1 import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}


@pytest.mark.parametrize("method", ["GET", "PUT", "OPTIONS", "DELETE", "POST", "error"])
def test_method_func(method):
    response = client.get(f"/{method}")
    lst = ["GET", "PUT", "OPTIONS", "DELETE"]
    if method.upper() in lst:
        assert response.status_code == 200
        assert response.json() == {"method": f"{method}".upper()}
    elif method.upper() == "POST":
        assert response.status_code == 201
        assert response.json() == {"method": f"{method}".upper()}

