from datetime import datetime
from typing import List
from uuid import uuid4
import dateutil.parser

from simulmedia.exceptions import InvalidUserException


class User:
    """
    A User. What more can I say?
    """
    fields: List[str] = ['user_id', 'created', 'updated', 'name']

    user_id: str = None
    created: datetime = None
    updated: datetime = None
    name: str = None

    def __init__(self, **kwargs):
        if 'user_id' in kwargs:
            self.user_id = kwargs['user_id']
        else:
            self.user_id = str(uuid4())

        if 'created' in kwargs:
            self.created = kwargs['created']

        if 'updated' in kwargs:
            self.updated = kwargs['updated']

        if 'name' in kwargs:
            self.name = kwargs['name']

        # Ensure that all required attributes are set
        for field in ['user_id', 'name']:
            if getattr(self, field) is None:
                raise InvalidUserException(f'{field} not specified')

    def __repr__(self):
        return f'<User {self.name}:{self.user_id}>'

    def to_json(self):
        # TODO: Ensure that all output datetime strings are Zulu
        return {
            'user_id': self.user_id,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat(),
            'name': self.name,
        }

    @classmethod
    def from_json(cls, json):
        # TODO: Ensure that all input datetimes are converted to UTC
        user = cls()
        user.user_id = json['user_id']
        user.created = dateutil.parser.isoparse(json['created'])
        user.updated = dateutil.parser.isoparse(json['updated'])
        user.name = json['name']

    def equals(self, other: 'User') -> bool:
        return self.user_id == other.user_id
