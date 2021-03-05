import json

import pytest

from simulmedia.types.ad import Ad
from simulmedia.types.exceptions import InvalidAdException


# TODO: JSON comparisons should be done by library... not str equality

class TestAd:
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

        for field in Ad.required_fields:
            config = default_config.copy()
            config.pop(field)

            with pytest.raises(InvalidAdException) as e:
                Ad(**config)
            assert f'{field} not specified' in str(e)

    def test__init__invalid_start_hour(self):
        config: dict = {
            "id": "111111",
            "video_url": "https://www.111111.com",
            "country": "US",
            "lang": "eng",
            "start_hour": -1,
            "end_hour": 23
        }

        with pytest.raises(InvalidAdException) as e:
            Ad(**config)
        assert 'Invalid start_hour' in str(e)

    def test__init__invalid_end_hour(self):
        config: dict = {
            "id": "111111",
            "video_url": "https://www.111111.com",
            "country": "US",
            "lang": "eng",
            "start_hour": 0,
            "end_hour": 25
        }

        with pytest.raises(InvalidAdException) as e:
            Ad(**config)
        assert 'Invalid end_hour' in str(e)

    def test__init__invalid_start_end_hour(self):
        config: dict = {
            "id": "111111",
            "video_url": "https://www.111111.com",
            "country": "US",
            "lang": "eng",
            "start_hour": 5,
            "end_hour": 4
        }

        with pytest.raises(InvalidAdException) as e:
            Ad(**config)
        assert 'start_hour must less than end_hour' in str(e)

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

        ad: Ad = Ad(**config)
        ad_json = ad.to_json()
        ad_config_dict: dict = json.loads(json.dumps(ad_json))
        for field in Ad.required_fields:
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

        ad_config = Ad(**config)
        assert json.dumps(ad_config.to_json(), indent=4) == ad_config.__repr__()
