from typing import Optional

import dateutil
from dateutil import tz
from datetime import datetime

from simulmedia.dao.base_dao import BaseDao
from simulmedia.services.database import DB_FILE_PATH
from simulmedia.types.exceptions import DBException, InvalidInputException
from simulmedia.types.user import User


class UserDao(BaseDao):
    __instance = None

    @staticmethod
    def get_instance():
        if UserDao.__instance is None:
            UserDao()
        return UserDao.__instance

    def __init__(self):
        if UserDao.__instance is not None:
            raise Exception('UserDao is a singleton!')
        else:
            super().__init__(db_file_path=DB_FILE_PATH)
            UserDao.__instance = self

    def get_by_id(self, user_id: str) -> Optional[User]:
        if not user_id:
            raise InvalidInputException(f'user_id not specified')

        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"SELECT user_id, created, updated, name FROM 'user' WHERE user_id = '{user_id}'")
            row = cursor.fetchone()
            if not row:
                return None

            created: datetime = dateutil.parser.parse(row[1]).replace(tzinfo=tz.UTC)
            updated: datetime = dateutil.parser.parse(row[2]).replace(tzinfo=tz.UTC)

            return User(
                user_id=row[0],
                created=created,
                updated=updated,
                name=row[3])
        except Exception as e:
            raise DBException(f'Error reading User from DB. user_id={user_id}') from e
        finally:
            if connection is not None:
                connection.close()
