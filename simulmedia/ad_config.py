import json
import logging
from datetime import datetime
from typing import List, Optional

import requests

from simulmedia.country import Country
from simulmedia.exceptions import InvalidAdConfigException
from simulmedia.language import Language

_logger = logging.getLogger(__name__)


class AdConfig:
    id: str = None
    video_url: str = None
    country: Country = None
    language: Language = None
    start_hour: int = None
    end_hour: int = None

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self.id = kwargs['id']

        if 'video_url' in kwargs:
            self.video_url = kwargs['video_url']

        if 'country' in kwargs:
            self.country = Country.get(kwargs['country'])

        if 'lang' in kwargs:
            self.language = Language.get(kwargs['lang'])

        if 'start_hour' in kwargs:
            self.start_hour = int(kwargs['start_hour'])

        if 'end_hour' in kwargs:
            self.end_hour = int(kwargs['end_hour'])

        # Ensure that all required attributes are set
        for field in ['id', 'video_url', 'country', 'language', 'start_hour', 'end_hour']:
            if getattr(self, field) is None:
                raise InvalidAdConfigException(f'{field} not specified')

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "video_url": self.video_url,
            "country": str(self.country),
            "lang": str(self.language),
            "start_hour": self.start_hour,
            "end_hour": self.end_hour
        })

    def __repr__(self):
        return self.to_json()


class AdConfigs:
    ad_configs: List[AdConfig]

    def __init__(self, ad_configs: List[AdConfig]):
        self.ad_configs = ad_configs

    def get_ad(self, country: Country, language: Language, hour: int = None) -> Optional[AdConfig]:
        if hour is None:
            hour = datetime.utcnow().hour

        ads: List[AdConfig] = []
        for ad_config in self.ad_configs:
            if ad_config.country.equals(country) \
                    and ad_config.language.equals(language) \
                    and ad_config.start_hour <= hour < ad_config.end_hour:
                ads.append(ad_config)

        if len(ads) == 0:
            return None

        sorted(ads, key=lambda k: k.start_hour)
        return ads[-1]

    @classmethod
    def fetch_ad_configs(cls, url: str) -> 'AdConfigs':
        # TODO: Consider dumping config into a DB so querying can be easier/faster than brute force searches
        try:
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
                        _logger.error(f'Error processing ad={ad}', e)

                ad_configs = AdConfigs(ad_configs=configs)
                return ad_configs
            else:
                _logger.error(f'Error response from AdConfigs fetch: url={url}, '
                              f'status_code={response.status_code}, text={response.text}')
        except Exception as e:
            # Should think about adding some re-try logic
            _logger.error(f'Error fetching AdConfigs: url={url}:', e)
