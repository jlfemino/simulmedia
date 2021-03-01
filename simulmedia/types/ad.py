import json
import logging
from datetime import datetime
from typing import List

from simulmedia.types.country import Country
from simulmedia.types.exceptions import InvalidAdException
from simulmedia.types.language import Language

_logger = logging.getLogger(__name__)


class Ad:
    """
    This class formalizes the format of the data found in the demo URL:
    https://gist.githubusercontent.com/victorhurdugaci/22a682eb508e65d97bd5b9152f564ab3/raw/dbf27ef217dba9bbd753de26cdabf8a91bdf1550/sm_ads.json
    """
    fields: List[str] = ['created', 'updated', 'id', 'video_url', 'country', 'lang', 'start_hour', 'end_hour']
    required_fields: List[str] = ['id', 'video_url', 'country', 'lang', 'start_hour', 'end_hour']

    created: datetime = None
    updated: datetime = None
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

        if 'end_hour' in kwargs:
            self.end_hour = int(kwargs['end_hour'])

        # Ensure that all required attributes are set
        for field in self.required_fields:
            if getattr(self, field) is None:
                raise InvalidAdException(f'{field} not specified')

        # Perform attribute validation
        if self.start_hour < 0 or self.start_hour > 23:
            raise InvalidAdException(f'Invalid start_hour. Must be [0-24). value={self.start_hour}')

        if self.end_hour < 1 or self.end_hour > 24:
            raise InvalidAdException(f'Invalid end_hour. Must be [0-24). value={self.end_hour}')

        if self.start_hour >= self.end_hour:
            raise InvalidAdException('start_hour must less than end_hour. '
                                     'start_hour={self.start_hour}, end_hour={self.end_hour}')

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
