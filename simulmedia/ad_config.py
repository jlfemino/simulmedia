import json
import logging
from datetime import datetime
from typing import List, Optional

import requests

from simulmedia.country import Country
from simulmedia.exceptions import AdSourceServiceException, InvalidAdConfigException
from simulmedia.language import Language

_logger = logging.getLogger(__name__)


class AdConfig:
    """
    This class formalizes the format of the data found in the demo URL:
    https://gist.githubusercontent.com/victorhurdugaci/22a682eb508e65d97bd5b9152f564ab3/raw/dbf27ef217dba9bbd753de26cdabf8a91bdf1550/sm_ads.json
    """
    fields: List[str] = ['id', 'video_url', 'country', 'lang', 'start_hour', 'end_hour']

    id: str = None
    video_url: str = None
    country: Country = None
    lang: Language = None
    start_hour: int = None
    end_hour: int = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']

        if 'video_url' in kwargs:
            self.video_url = kwargs['video_url']
            # TODO: URL validation

        if 'country' in kwargs:
            self.country = Country.get(kwargs['country'])

        if 'lang' in kwargs:
            self.lang = Language.get(kwargs['lang'])

        if 'start_hour' in kwargs:
            self.start_hour = int(kwargs['start_hour'])
            if self.start_hour < 0 or self.start_hour > 24:
                raise InvalidAdConfigException(f'Invalid start_hour. Must be [0-24). value={self.start_hour}')

        if 'end_hour' in kwargs:
            self.end_hour = int(kwargs['end_hour'])
            if self.end_hour < 0 or self.end_hour > 24:
                raise InvalidAdConfigException(f'Invalid end_hour. Must be [0-24). value={self.end_hour}')

        # Ensure that all required attributes are set
        for field in self.fields:
            if getattr(self, field) is None:
                raise InvalidAdConfigException(f'{field} not specified')

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "video_url": self.video_url,
            "country": str(self.country),
            "lang": str(self.lang),
            "start_hour": self.start_hour,
            "end_hour": self.end_hour
        })

    def __repr__(self):
        return self.to_json()


class AdConfigs:
    ad_configs: List[AdConfig]

    def __init__(self, ad_configs: List[AdConfig]):
        self.ad_configs = ad_configs

    def set_ads(self, ad_configs: List[AdConfig]):
        """
        For unit testing (or for dynamic ad updates?)
        """
        self.ad_configs = ad_configs

    def get_ad(self, country: Country, language: Language, hour: int = None) -> Optional[AdConfig]:
        if hour is None:
            hour = datetime.utcnow().hour

        ads: List[AdConfig] = []
        for ad_config in self.ad_configs:
            if ad_config.country.equals(country) \
                    and ad_config.lang.equals(language) \
                    and ad_config.start_hour <= hour < ad_config.end_hour:
                ads.append(ad_config)

        if len(ads) == 0:
            return None

        sorted(ads, key=lambda k: k.start_hour)
        return ads[-1]

    @classmethod
    def fetch_ad_configs(cls, url: str) -> 'AdConfigs':
        # TODO: Put config into a DB so querying can be easier/faster than brute force searches
        # TODO: Add retry logic
        response = requests.get(url)
        if 199 < response.status_code < 300:
            ads = response.json()['ads']

            # ad_configs: List[AdConfig] = [AdConfig(**ad) for ad in ads]
            configs: List[AdConfig] = []
            for ad in ads:
                try:
                    config = AdConfig(**ad)
                    configs.append(config)
                except Exception as e:
                    _logger.error(f'Error processing ad={ad}. Skipping.', exc_info=e)

            ad_configs = AdConfigs(ad_configs=configs)
            return ad_configs
        else:
            raise AdSourceServiceException(
                f'Error response from AdConfigs fetch: url={url}, '
                f'status_code={response.status_code}, text={response.text}')
