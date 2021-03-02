import logging
from enum import Enum
from typing import Optional

_logger = logging.getLogger(__name__)


class AdChooser(Enum):
    ONCE_PER_24_HOURS = 'ONCE_PER_24_HOURS'
    ONCE_PER_CALENDAR_DAY_UTC = 'ONCE_PER_CALENDAR_DAY_UTC'
    ONCE_PER_CALENDAR_DAY_LOCAL = 'ONCE_PER_CALENDAR_DAY_LOCAL'
    LEAST_RECENTLY_VIEWED = 'LEAST_RECENTLY_VIEWED'

    def __str__(self):
        return str(self.value)

    @classmethod
    def lookup(cls, val: str) -> Optional['AdChooser']:
        """
        Converts str to Enum member. Returns None, if no suitable value found.
        """
        try:
            return AdChooser(val.upper())
        except Exception as e:
            _logger.warning(f'Invalid AdChooser value={val}', exc_info=e)
            return None
