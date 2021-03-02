from sqlite3 import IntegrityError
from typing import List, Optional

import dateutil

from simulmedia.dao.base_dao import BaseDao
from simulmedia.services.config import config_parser
from simulmedia.services.database import DB_FILE_PATH
from simulmedia.types.ad import Ad
from simulmedia.types.country import Country
from simulmedia.types.exceptions import DBException, DBIntegrityException, InvalidInputException
from simulmedia.types.language import Language

ISO_8601_FORMAT: str = config_parser['DEFAULT']['ISO_8601_FORMAT']


class AdDao(BaseDao):
    __instance = None

    @staticmethod
    def get_instance():
        if AdDao.__instance is None:
            AdDao()
        return AdDao.__instance

    def __init__(self):
        if AdDao.__instance is not None:
            raise Exception('AdDao is a singleton!')
        else:
            super().__init__(db_file_path=DB_FILE_PATH)
            AdDao.__instance = self

    @staticmethod
    def _row_to_ad(row: dict) -> Ad:
        return Ad(**{
            'created': dateutil.parser.isoparse(row[0]),
            'updated': dateutil.parser.isoparse(row[1]),
            'id': row[2],
            'video_url': row[3],
            'country': row[4],
            'lang': row[5],
            'start_hour': row[6],
            'end_hour': row[7]
        })

    def get_all(self) -> List[Ad]:
        connection = None
        try:
            sql: str = f"SELECT created, updated, ad_id, video_url, country, lang, start_hour, end_hour FROM 'ad';"

            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [self._row_to_ad(row) for row in rows]
        except Exception as e:
            raise DBException(f'Error reading Ads from DB.') from e
        finally:
            if connection is not None:
                connection.close()

    def get_all_by_region(self, country: Country, language: Language) -> List[Ad]:
        connection = None
        try:
            sql: str = f"SELECT created, updated, ad_id, video_url, country, lang, start_hour, end_hour FROM 'ad' "\
                       f"WHERE country = '{country.alpha_2}' AND lang = '{language.alpha_2}';"

            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [self._row_to_ad(row) for row in rows]
        except Exception as e:
            raise DBException(f'Error reading Ads from DB.') from e
        finally:
            if connection is not None:
                connection.close()

    def get_by_id(self, ad_id: str) -> Optional[Ad]:
        if not ad_id:
            raise InvalidInputException(f'ad_id not specified')

        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"""SELECT created, updated, ad_id, video_url, country, lang, start_hour, end_hour
                FROM 'ad' WHERE ad_id = '{ad_id}';""")
            row = cursor.fetchone()
            if not row:
                return None

            return self._row_to_ad(row)
        except Exception as e:
            raise DBException(f'Error reading Ad from DB. ad_id={ad_id}') from e
        finally:
            if connection is not None:
                connection.close()

    def get_current_ads(self, country: Country, language: Language, hour: int) -> List[Ad]:
        """
        Gets all Ads for the specified Country & Language & hour, and return them in 'end_hour' order.
        """
        if not country:
            raise InvalidInputException(f'country not specified')

        if not language:
            raise InvalidInputException(f'language not specified')

        connection = None
        try:
            ads: List[Ad] = []

            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT created, updated, ad_id, video_url, country, lang, start_hour, end_hour FROM 'ad' "
                f"WHERE country = '{country.alpha_2}' AND lang = '{language.alpha_2}' "
                f"AND start_hour <= {hour} AND {hour} < end_hour ORDER BY start_hour ASC;")
            rows = cursor.fetchall()
            for row in rows:
                ads.append(self._row_to_ad(row))

            return ads
        except Exception as e:
            raise DBException(
                f'Error reading Ads from DB. '
                f'country={country.alpha_2}, language={language.alpha_2}') from e
        finally:
            if connection is not None:
                connection.close()

    def create(self, ad: Ad):
        if not ad:
            raise InvalidInputException(f'ad not specified')

        connection = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"""INSERT INTO 'ad' (ad_id, video_url, country, lang, start_hour, end_hour)
                VALUES ('{ad.id}', '{ad.video_url}', '{ad.country.alpha_2}', 
                        '{ad.lang.alpha_2}', {ad.start_hour}, {ad.end_hour})""")
            connection.commit()
            connection.close()
        except IntegrityError as e:
            raise DBIntegrityException('SQL integrity violation. Probably UNIQUE constraint. Skipping.') from e
        except Exception as e:
            raise DBException(
                f'Error writing Ad to DB. ad={ad.to_json()}') from e
        finally:
            if connection is not None:
                connection.close()
