import sqlite3
from tempfile import TemporaryDirectory

import pytest

from simulmedia.database import apply_db_migrations
from simulmedia.exceptions import DBConfigException
from tests.base_test import BaseTest, DB_FILE_PATH


@pytest.mark.usefixtures('init_db')
class TestDatabase(BaseTest):

    # ================================================================================
    # apply_db_migrations()
    # ================================================================================
    def test__apply_db_migrations__migrations_dir_missing(self, init_db):
        with pytest.raises(DBConfigException) as e:
            apply_db_migrations(migrations_dir='/This/path/does/not/exist.db')
        assert 'DB Migrations dir does not exist' in str(e)

    def test__apply_db_migrations__migration_error(self, init_db):
        with TemporaryDirectory() as tempdir:
            # Create dummy migration file
            script_path: str = f'{tempdir}/0000_init.sql'
            script_file = open(file=script_path, mode='w+')
            script_file.write('CREATE this does not compute... error... error')
            script_file.close()

            with pytest.raises(DBConfigException) as e:
                apply_db_migrations(migrations_dir=tempdir)
            assert 'Error applying DB migrations' in str(e)

    def test__apply_db_migrations__happy_path(self, init_db):
        cursor = None

        try:
            connection = sqlite3.connect(DB_FILE_PATH)
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM 'user' ORDER BY name ASC;")
            rows = cursor.fetchall()
            assert len(rows) == 2
            assert rows[0][0] == 'Baruta'
            assert rows[1][0] == 'Nomi'
        except Exception as e:
            pytest.fail(f'Exception encountered: {str(e)}')
        finally:
            if cursor is not None:
                cursor.close()

