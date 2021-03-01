from datetime import datetime
from typing import List

import dateutil.parser

from simulmedia.types.exceptions import InvalidUserException


class UserAdView:
    """
    An instance of when a User viewed an Ad
    """
    fields: List[str] = ['created', 'updated', 'user_id', 'ad_id']

    created: datetime = None
    updated: datetime = None
    user_id: str = None
    ad_id: str = None

    def __init__(self, **kwargs):
        if 'created' in kwargs:
            self.created = kwargs['created']

        if 'updated' in kwargs:
            self.updated = kwargs['updated']

        if 'user_id' in kwargs:
            self.user_id = kwargs['user_id']

        if 'ad_id' in kwargs:
            self.ad_id = kwargs['ad_id']

        # Ensure that all required attributes are set
        for field in ['user_id', 'ad_id']:
            if getattr(self, field) is None:
                raise InvalidUserException(f'{field} not specified')

    def __repr__(self):
        return f'<UserAdView {self.user_id}:{self.ad_id}>'

    def to_json(self):
        # TODO: Ensure that all output datetime strings are Zulu
        return {
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat(),
            'user_id': self.user_id,
            'ad_id': self.ad_id,
        }

    @classmethod
    def from_json(cls, json):
        # TODO: Ensure that all input datetimes are converted to UTC
        user = cls()
        user.created = dateutil.parser.isoparse(json['created'])
        user.updated = dateutil.parser.isoparse(json['updated'])
        user.user_id = json['user_id']
        user.ad_id = json['ad_id']

    def equals(self, other: 'UserAdView') -> bool:
        return self.user_id == other.user_id \
            and self.ad_id == other.ad_id \
            and self.created == other.created
