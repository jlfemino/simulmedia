import logging
import os
import random
from datetime import datetime, timedelta
from typing import Callable, List, Optional

import requests

from simulmedia.dao.ad_dao import AdDao
from simulmedia.dao.user_ad_view_dao import UserAdViewDao
from simulmedia.services.config import config_parser
from simulmedia.types.ad import Ad
from simulmedia.types.ad_chooser import AdChooser
from simulmedia.types.country import Country
from simulmedia.types.exceptions import AdSourceServiceException, DBIntegrityException, ConfigException
from simulmedia.types.language import Language
from simulmedia.types.user import User
from simulmedia.types.user_ad_view import UserAdView

_logger = logging.getLogger(__name__)

# TODO: Create listener service to which Ads can be pushed (and/or polled from).


class AdsFetcher:
    __instance = None
    __ad_dao: AdDao = None
    __user_ad_view_dao: UserAdViewDao = None
    __ad_chooser_function: Callable = None

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

            # Select AdChooser function
            try:
                ad_chooser_str: str = config_parser[os.environ.get('APP_ENV', None)]['AD_CHOOSER']
                ad_chooser: Optional[AdChooser] = AdChooser.lookup(ad_chooser_str)
                if not ad_chooser:
                    _logger.warning(f'AD_CHOOSER not properly specified in config! value={ad_chooser_str}')

                # Determine which function will determine the ad
                AdsFetcher.__ad_chooser_function = AdsFetcher.determine_ad__once_per_24_hours
                if ad_chooser == AdChooser.ONCE_PER_24_HOURS:
                    pass
                else:
                    _logger.error(f'Unsupported AdChooser = {ad_chooser.value}. '
                                  f'Using {AdsFetcher.__ad_chooser_function}')
            except Exception as e:
                _logger.exception(f'Exception determining AdChooser.', exc_info=e)

    @staticmethod
    def get_ad(user: User,
               country: Country,
               language: Language,
               hour: int = None) -> Optional[Ad]:
        if hour is None:
            hour = datetime.utcnow().hour

        return AdsFetcher.__ad_chooser_function(user, country, language, hour)

    @staticmethod
    def determine_ad__once_per_24_hours(
            user: User,
            country: Country,
            language: Language,
            hour: int) -> Optional[Ad]:
        if hour is None:
            hour = datetime.utcnow().hour

        # Get all Ads for this country/language/hour
        ads: List[Ad] = AdsFetcher.__ad_dao.get_current_ads(country=country, language=language, hour=hour)

        # Get all Ads viewed by this user in the past 24 hours
        user_ad_views: List[UserAdView] = AdsFetcher.__user_ad_view_dao.get_all_by_user_id(
            user_id=user.user_id, since=datetime.utcnow() - timedelta(hours=24))
        viewed_ad_ids: List[str] = [user_ad_view.ad_id for user_ad_view in user_ad_views]

        # Determine which Ad (if any) to show the user
        if len(ads) == 0:
            return None

        # Return first current ad not viewed in past 24 hours
        for ad in ads:
            if ad.id not in viewed_ad_ids:
                return ad

    @staticmethod
    def fetch_ads(url: str):
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
