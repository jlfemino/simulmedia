from datetime import datetime
from sqlite3 import IntegrityError
from typing import List

import dateutil

from simulmedia.dao.base_dao import BaseDao
from simulmedia.services.config import config_parser
from simulmedia.services.database import DB_FILE_PATH
from simulmedia.types.exceptions import DBException, DBIntegrityException, InvalidInputException
from simulmedia.types.user_ad_view import UserAdView

ISO_8601_FORMAT: str = config_parser['DEFAULT']['ISO_8601_FORMAT']


class UserAdViewDao(BaseDao):
    __instance = None

    @staticmethod
    def get_instance():
        if UserAdViewDao.__instance is None:
            UserAdViewDao()
        return UserAdViewDao.__instance

    def __init__(self):
        if UserAdViewDao.__instance is not None:
            raise Exception('UserAdViewDao is a singleton!')
        else:
            super().__init__(db_file_path=DB_FILE_PATH)
            UserAdViewDao.__instance = self

    def get_all_by_user_id(self,
                           user_id: str,
                           since: datetime = None) -> List[UserAdView]:
        if not user_id:
            raise InvalidInputException(f'user_id not specified')

        connection = None
        try:
            user_ad_views: List[UserAdView] = []

            sql: str = f"SELECT created, updated, user_id, ad_id FROM 'user_ad_view' WHERE user_id = '{user_id}' "
            if since:
                sql += f"AND created >= '{since.strftime(ISO_8601_FORMAT)}' "
            sql += "ORDER BY created ASC;"

            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                user_ad_view: UserAdView = UserAdView(
                    created=dateutil.parser.isoparse(row[0]),
                    updated=dateutil.parser.isoparse(row[1]),
                    user_id=row[2],
                    ad_id=row[3])
                user_ad_views.append(user_ad_view)

            return user_ad_views
        except Exception as e:
            raise DBException(
                f'Error reading UserAdViews from DB. '
                f'user_id={user_id}, since={since}') from e
        finally:
            if connection is not None:
                connection.close()

    def create(self,
               user_id: str,
               ad_id: str,
               created: datetime = None,
               updated: datetime = None):
        if not user_id:
            raise InvalidInputException(f'user_id not specified')

        if not ad_id:
            raise InvalidInputException(f'ad_id not specified')

        now_utc: datetime = datetime.utcnow()
        if not created:
            created = now_utc

        if not updated:
            updated = now_utc

        connection = None
        try:
            sql: str = f"""INSERT INTO 'user_ad_view' (user_id, ad_id, created, updated) 
                VALUES ('{user_id}', '{ad_id}', '{created.isoformat()}', '{updated.isoformat()}')"""

            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            connection.close()
        except IntegrityError as e:
            raise DBIntegrityException('SQL integrity violation. Probably UNIQUE constraint. Skipping.') from e
        except Exception as e:
            raise DBException(
                f'Error writing UserAdView to DB. '
                f'user_id={user_id}, ad_id={ad_id}') from e
        finally:
            if connection is not None:
                connection.close()
