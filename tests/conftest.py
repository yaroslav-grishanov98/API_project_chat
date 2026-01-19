import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from api_service.main import create_application
from api_service.core.database import Base, get_db
from api_service.models import chat, message


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session:
        yield session

    session.close()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    fresh_app = create_application()

    def override_get_db():
        yield session

    fresh_app.dependency_overrides[get_db] = override_get_db

    with TestClient(fresh_app) as client:
        yield client

    fresh_app.dependency_overrides.clear()
