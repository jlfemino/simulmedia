import json

import pytest

from simulmedia.ad_config import AdConfig, AdConfigs
from simulmedia.country import Country
from simulmedia.exceptions import InvalidAdConfigException
from simulmedia.language import Language


class TestAdConfig:
    # ================================================================================
    # __init__()
    # ================================================================================
    def test__init__missing_fields(self):
        default_config: dict = {
            "id": "111111",
            "video_url": "https://www.111111.com",
            "country": "US",
            "lang": "eng",
            "start_hour": 1,
            "end_hour": 23
        }

        for field in AdConfig.fields:
            config = default_config.copy()
            config.pop(field)

            with pytest.raises(InvalidAdConfigException) as e:
                AdConfig(**config)
            assert f'{field} not specified' in str(e)

    # ================================================================================
    # to_json()
    # ================================================================================
    def test__to_json__happy_path(self):
        config: dict = {
            "id": "111111",
            "video_url": "https://www.111111.com",
            "country": "US",
            "lang": "en",
            "start_hour": 1,
            "end_hour": 23
        }

        ad_config_dict: dict = json.loads(AdConfig(**config).to_json())
        for field in AdConfig.fields:
            assert ad_config_dict[field] == config[field]

    # ================================================================================
    # __repr__()
    # ================================================================================
    def test__repr__happy_path(self):
        config: dict = {
            "id": "111111",
            "video_url": "https://www.111111.com",
            "country": "US",
            "lang": "en",
            "start_hour": 1,
            "end_hour": 23
        }

        ad_config = AdConfig(**config)
        assert ad_config.to_json() == ad_config.__repr__()


class TestAdConfigs:
    # ================================================================================
    # ad_get_ad()
    # ================================================================================
    def test__get_ad__not_found(self):
        ad_configs = AdConfigs([])

        us = Country.get('us')
        en = Language.get('en')

        assert ad_configs.get_ad(country=us, language=en, hour=0) is None

    def test__get_ad__us_en__hour_not_specified(self):
        ad_configs = AdConfigs([
            AdConfig(**{
                "id": "111111",
                "video_url": "https://www.111111.com",
                "country": "us",
                "lang": "eng",
                "start_hour": 0,
                "end_hour": 23
            })
        ])

        us = Country.get('us')
        en = Language.get('en')

        assert ad_configs.get_ad(country=us, language=en).id == '111111'

    def test__get_ad__us_en__all_hours(self):
        ad_configs = AdConfigs([
            # starts 1 hours after start of day, and stops 1 hour before end of day
            AdConfig(**{
                "id": "111111",
                "video_url": "https://www.111111.com",
                "country": "us",
                "lang": "eng",
                "start_hour": 1,
                "end_hour": 23
            }),
            # starts 3 hours after start of day, and stops 3 hours before end of day
            AdConfig(**{
                "id": "222222",
                "video_url": "https://www.222222.com",
                "country": "us",
                "lang": "eng",
                "start_hour": 3,
                "end_hour": 20
            }),
            # starts 6 hours after start of day, and stops 6 hours before end of day
            AdConfig(**{
                "id": "333333",
                "video_url": "https://www.333333.com",
                "country": "us",
                "lang": "eng",
                "start_hour": 6,
                "end_hour": 17
            })
        ])

        us = Country.get('us')
        en = Language.get('en')

        assert ad_configs.get_ad(country=us, language=en, hour=0) is None
        assert ad_configs.get_ad(country=us, language=en, hour=1).video_url == 'https://www.111111.com'
        assert ad_configs.get_ad(country=us, language=en, hour=2).video_url == 'https://www.111111.com'
        assert ad_configs.get_ad(country=us, language=en, hour=3).video_url == 'https://www.222222.com'
        assert ad_configs.get_ad(country=us, language=en, hour=4).video_url == 'https://www.222222.com'
        assert ad_configs.get_ad(country=us, language=en, hour=5).video_url == 'https://www.222222.com'
        assert ad_configs.get_ad(country=us, language=en, hour=6).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=7).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=8).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=9).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=10).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=11).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=12).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=13).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=14).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=15).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=16).video_url == 'https://www.333333.com'
        assert ad_configs.get_ad(country=us, language=en, hour=17).video_url == 'https://www.222222.com'
        assert ad_configs.get_ad(country=us, language=en, hour=18).video_url == 'https://www.222222.com'
        assert ad_configs.get_ad(country=us, language=en, hour=19).video_url == 'https://www.222222.com'
        assert ad_configs.get_ad(country=us, language=en, hour=20).video_url == 'https://www.111111.com'
        assert ad_configs.get_ad(country=us, language=en, hour=21).video_url == 'https://www.111111.com'
        assert ad_configs.get_ad(country=us, language=en, hour=22).video_url == 'https://www.111111.com'
        assert ad_configs.get_ad(country=us, language=en, hour=23) is None
