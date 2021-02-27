import os
from pathlib import Path

import pytest

from simulmedia.config import config_parser
from simulmedia.database import apply_db_migrations

BASE_DIR: str = str(Path(__file__).parent.parent)
DB_FILE_PATH: str = f"{BASE_DIR}/{config_parser['DB']['SQLITE3_UNIT_TEST_FILE']}"
DB_CONNECTION_URL: str = f"sqlite:///{DB_FILE_PATH}"


# TODO: Add support for parallel unit tests

class BaseTest:
    @pytest.fixture
    def init_db(self):
        # Delete existing DB
        if os.path.exists(DB_FILE_PATH):
            os.remove(DB_FILE_PATH)

        # Initialize new DB
        apply_db_migrations(db_connection_url=DB_CONNECTION_URL)

        yield
