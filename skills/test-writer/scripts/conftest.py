import pytest
import os
import psycopg2
from unittest.mock import MagicMock
from common.config import config
from db import DB


@pytest.fixture(scope="session")
def pg_connection():
    conn = psycopg2.connect(os.getenv("TEST_DATABASE_URL"))
    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def rollback(pg_connection):
    yield
    pg_connection.rollback()


@pytest.fixture
def db(pg_connection):
    return DB(pg_connection)


@pytest.fixture
def mock_config():
    cfg = MagicMock(spec=config)
    cfg.model = "test-model"
    cfg.embedding_model = "nomic-embed-text"
    cfg.profile_model = "test-model"
    cfg.base_url = "http://localhost:11434"
    cfg.system_prompt = "You are a test agent. {user_profile}"
    return cfg
