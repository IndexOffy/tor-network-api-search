from fastapi.testclient import TestClient
from tests.database import app

client = TestClient(app)


def test_read_main():
    pass
