import os
from pathlib import Path

import pytest

from main import app
from simulmedia.services.config import config_parser
from simulmedia.services.database import apply_db_migrations


# TODO: Add support for parallel unit tests


class BaseTest:
    PROJECT_BASE_DIR: str = str(Path(__file__).parent.parent)
    DB_FILE_PATH: str = f"{PROJECT_BASE_DIR}/{config_parser['ENV_TEST']['SQLITE3_FILE']}"
    DB_CONNECTION_URL: str = f"sqlite:///{DB_FILE_PATH}"

    # ================================================================================
    # Pytest fixtures
    # ================================================================================
    @pytest.fixture
    def init_db(self):
        # Delete existing DB file
        if os.path.exists(self.DB_FILE_PATH):
            os.remove(self.DB_FILE_PATH)

        # Initialize fresh DB
        apply_db_migrations(db_connection_url=self.DB_CONNECTION_URL)
        yield

    @pytest.fixture
    def init_app_context(self):
        app_context = app.app_context()
        app_context.push()

        yield app_context

        app_context.pop()

    @pytest.fixture
    def test_client(self):
        test_client = app.test_client()

        yield test_client

    # ================================================================================
    # Utility methods
    # ================================================================================
    @staticmethod
    def list_api_endpoints(flask_app):
        for rule in flask_app.url_map.iter_rules():
            print(rule.rule)
