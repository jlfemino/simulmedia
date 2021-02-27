import os
import logging
from pathlib import Path
from simulmedia.exceptions import DBConfigException
from yoyo import read_migrations, get_backend
from simulmedia.config import config_parser

_logger = logging.getLogger(__name__)
BASE_DIR: str = str(Path(__file__).parent.parent)
MIGRATIONS_DIR: str = f'{BASE_DIR}/db_migrations'
DB_CONNECTION_URL: str = f"sqlite:///{BASE_DIR}/{config_parser['DB']['SQLITE3_FILE']}"


def apply_db_migrations(db_connection_url: str = DB_CONNECTION_URL, migrations_dir: str = MIGRATIONS_DIR):
    if not migrations_dir or not os.path.exists(migrations_dir) or not os.path.isdir(migrations_dir):
        raise DBConfigException(f'DB Migrations dir does not exist (or is not a dir). path={migrations_dir}')

    try:
        _logger.info(f'DB Migrations: Reading dir={migrations_dir}...')
        migrations = read_migrations(migrations_dir)

        backend = get_backend(db_connection_url)
        with backend.lock():
            _logger.info('DB Migrations: Applying...')
            backend.apply_migrations(backend.to_apply(migrations))

        _logger.info('DB migrations: Done.')
    except Exception as e:
        raise DBConfigException('Error applying DB migrations.') from e
