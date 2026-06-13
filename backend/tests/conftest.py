import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.dependencies import get_db
from app.main import app

_TEST_DATABASE_URL = "sqlite:///./test.db"

_engine = create_engine(_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
_TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=_engine)
    yield
    Base.metadata.drop_all(bind=_engine)


def _override_get_db():
    db = _TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def auth_token(client: TestClient) -> str:
    resp = client.post(
        "/auth/token", data={"username": "admin", "password": "changeme"}
    )
    assert resp.status_code == 200
    return resp.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {auth_token}"}
