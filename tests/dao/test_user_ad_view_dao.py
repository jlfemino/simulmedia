from datetime import datetime, timedelta
from typing import List

import pytest

from simulmedia.dao.user_ad_view_dao import UserAdViewDao
from simulmedia.types.user_ad_view import UserAdView
from tests.base_test import BaseTest

user_ad_view_dao = UserAdViewDao.get_instance()


@pytest.mark.usefixtures('init_db')
class TestUserAdViewDao(BaseTest):
    # ================================================================================
    # add() & get_all_by_user_id()
    # ================================================================================
    def test__get_all_by_user_id__happy_path(self):
        # ----------------------------------------
        # Setup
        # ----------------------------------------
        now_utc: datetime = datetime.utcnow()
        user_id: str = 'e38c6813-5228-4f59-a250-c5948a054502'

        user_ad_view_dao.create(user_id=user_id,
                                ad_id='111111',
                                created=now_utc - timedelta(minutes=178))
        user_ad_view_dao.create(user_id=user_id,
                                ad_id='222222',
                                created=now_utc - timedelta(minutes=118))
        user_ad_view_dao.create(user_id=user_id,
                                ad_id='333333',
                                created=now_utc - timedelta(minutes=58))

        # ----------------------------------------
        # Get ALL by this User
        # ----------------------------------------
        user_ad_views: List[UserAdView] = user_ad_view_dao.get_all_by_user_id(user_id=user_id)
        assert len(user_ad_views) == 3
        assert user_ad_views[0].ad_id == '111111'
        assert user_ad_views[1].ad_id == '222222'
        assert user_ad_views[2].ad_id == '333333'

        # ----------------------------------------
        # Get all from the past 3 hours
        # ----------------------------------------
        user_ad_views: List[UserAdView] = user_ad_view_dao.get_all_by_user_id(
            user_id=user_id, since=now_utc - timedelta(hours=3))
        assert len(user_ad_views) == 3
        assert user_ad_views[0].ad_id == '111111'
        assert user_ad_views[1].ad_id == '222222'
        assert user_ad_views[2].ad_id == '333333'

        # ----------------------------------------
        # Get all from the past 2 hours
        # ----------------------------------------
        user_ad_views = user_ad_view_dao.get_all_by_user_id(
            user_id=user_id, since=now_utc - timedelta(hours=2))
        assert len(user_ad_views) == 2
        assert user_ad_views[0].ad_id == '222222'
        assert user_ad_views[1].ad_id == '333333'

        # ----------------------------------------
        # Get all from the past 1 hour
        # ----------------------------------------
        user_ad_views = user_ad_view_dao.get_all_by_user_id(
            user_id=user_id, since=now_utc - timedelta(hours=1))
        assert len(user_ad_views) == 1
        assert user_ad_views[0].ad_id == '333333'
