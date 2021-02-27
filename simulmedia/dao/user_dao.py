from typing import Optional

from simulmedia.dao.base_dao import BaseDao
from simulmedia.user import User
from simulmedia.exceptions import InvalidInputException, DBConfigException


class UserDao(BaseDao):
    def __init__(self, db_file_path: str):
        super().__init__(db_file_path=db_file_path)

    def get_by_id(self, user_id: str) -> Optional[User]:
        if not user_id:
            raise InvalidInputException(f'user_id not specified')

        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"SELECT user_id, created, updated, name FROM 'user' WHERE user_id = '{user_id}'")
            row = cursor.fetchone()
            if not row:
                return None

            return User(user_id=row[0], created=row[1], updated=row[2], name=row[3])
        except Exception as e:
            raise DBConfigException(f'Error reading from DB. user_id={user_id}') from e
