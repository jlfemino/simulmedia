import pytest

from simulmedia.types.ad import Ad
from tests.base_test import BaseTest
from simulmedia.dao.ad_dao import AdDao


@pytest.mark.usefixtures('init_db')
class TestAdDao(BaseTest):
    def test__get_by_id__happy_path(self):
        ad_config: dict = {
            "id": "123456",
            "video_url": "https://www.123456.com",
            "country": "US",
            "lang": "en",
            "start_hour": 0,
            "end_hour": 24
        }

        AdDao.get_instance().create(Ad(**ad_config))
        ad: Ad = AdDao.get_instance().get_by_id(ad_config['id'])
        assert ad is not None
        assert ad.id == ad_config['id']
        assert ad.video_url == ad_config['video_url']
        assert ad.country.alpha_2.upper() == ad_config['country'].upper()
        assert ad.lang.alpha_2.lower() == ad_config['lang'].lower()
        assert ad.start_hour == ad_config['start_hour']
        assert ad.end_hour == ad_config['end_hour']
