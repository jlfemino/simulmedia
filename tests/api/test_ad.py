from typing import List

import pytest

from main import app
from simulmedia.ad_config import AdConfig
from simulmedia.api.ad import default_ad_configs


class TestApi:
    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    # ================================================================================
    # Ads API
    # ================================================================================
    def test__get_ad_url__not_found(self):
        # Save original configs
        original_configs: List[AdConfig] = default_ad_configs.ad_configs
        try:
            # Set test configs
            default_ad_configs.set_ads(ad_configs=[])

            with app.test_client() as client:
                response = client.get('http://localhost:5000/ad/us/en')
                assert response.status_code == 404
        finally:
            # Restore original configs
            default_ad_configs.set_ads(ad_configs=original_configs)

    def test__get_ad_url__invalid_country(self):
        with app.test_client() as client:
            response = client.get('http://localhost:5000/ad/xxx/en')
            assert response.status_code == 400

    def test__get_ad_url__happy_path(self):
        # Save original configs
        default_configs: List[AdConfig] = default_ad_configs.ad_configs
        try:
            # Set test configs
            ad_configs = [AdConfig(**{
                "id": "111111",
                "video_url": "https://www.111111.com",
                "country": "us",
                "lang": "en",
                "start_hour": 0,
                "end_hour": 23
            })]
            default_ad_configs.set_ads(ad_configs=ad_configs)

            with app.test_client() as client:
                response = client.get('http://localhost:5000/ad/us/en/2')
                assert response.status_code == 200
                assert response.data == b'https://www.111111.com'
        finally:
            # Restore original configs
            default_ad_configs.set_ads(ad_configs=default_configs)
