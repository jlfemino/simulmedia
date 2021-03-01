import logging
import random
from datetime import datetime, timedelta
from typing import List, Optional

import requests

from simulmedia.dao.ad_dao import AdDao
from simulmedia.dao.user_ad_view_dao import UserAdViewDao
from simulmedia.types.ad import Ad
from simulmedia.types.country import Country
from simulmedia.types.exceptions import AdSourceServiceException, DBIntegrityException
from simulmedia.types.language import Language
from simulmedia.types.user import User
from simulmedia.types.user_ad_view import UserAdView

_logger = logging.getLogger(__name__)


# TODO: Create listener service to which Ads can be pushed... and/or polling.


class AdsFetcher:
    __instance = None
    __ad_dao: AdDao = None
    __user_ad_view_dao: UserAdViewDao = None

    @staticmethod
    def get_instance():
        if AdsFetcher.__instance is None:
            AdsFetcher()
        return AdsFetcher.__instance

    def __init__(self):
        if AdsFetcher.__instance is not None:
            raise Exception('AdsFetcher is a singleton!')
        else:
            AdsFetcher.__ad_dao = AdDao.get_instance()
            AdsFetcher.__user_ad_view_dao = UserAdViewDao.get_instance()
            AdsFetcher.__instance = self

    @staticmethod
    def determine_ad_for_user(user: User,
                              country: Country,
                              language: Language,
                              hour: int = None) -> Optional[Ad]:
        if hour is None:
            hour = datetime.utcnow().hour

        # Get all Ads for this country/language/hour
        ads: List[Ad] = AdsFetcher.__ad_dao.get_current_ads(country=country, language=language, hour=hour)

        # Get all Ads viewed by this user in the past 24 hours
        user_ad_views: List[UserAdView] = AdsFetcher.__user_ad_view_dao.get_all_by_user_id(
            user_id=user.user_id, since=datetime.utcnow() - timedelta(hours=24))

        # Determine which Ad (if any) to show the user
        if len(ads) == 0:
            return None

        # TODO: Replace random Ad with a layered approach:
        #  - Show the first ad in the list that hasn't been seen
        #  - If all have been seen, figure something else out (e.g. No ad, or the ad least recently seen)
        random_index: int = random.randint(0, len(ads)-1)
        return ads[random_index]

    @staticmethod
    def fetch_ads(self, url: str):
        """
        Fetch Ads from the provided URL, and save them to the current DB.
        """
        response = requests.get(url)
        if 199 < response.status_code < 300:
            ads = response.json()['ads']
            num_ads_saved: int = 0
            for ad in ads:
                try:
                    AdsFetcher.__ad_dao.create(Ad(**ad))
                    num_ads_saved += 1
                except DBIntegrityException as e:
                    _logger.warning(f'Already seem to have ad={ad}. Skipping.', exc_info=e)
                except Exception as e:
                    _logger.error(f'Error processing ad={ad}. Skipping.', exc_info=e)

            _logger.info(f'Saved {num_ads_saved} from url={url}')
        else:
            raise AdSourceServiceException(
                f'Error response from Ads fetch: url={url}, '
                f'status_code={response.status_code}, text={response.text}')
