from main import get_ad_url

from simulmedia.ad_config import AdConfig, AdConfigs


class TestApi:
    # ================================================================================
    # get_ad_url()
    # ================================================================================
    def test__get_ad_url__us_en__all_hours(self):
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

        assert get_ad_url(country='us', language='en', hour=0, ad_configs=ad_configs) is None
        assert get_ad_url(country='us', language='en', hour=1, ad_configs=ad_configs) == 'https://www.111111.com'
        assert get_ad_url(country='us', language='en', hour=2, ad_configs=ad_configs) == 'https://www.111111.com'
        assert get_ad_url(country='us', language='en', hour=3, ad_configs=ad_configs) == 'https://www.222222.com'
        assert get_ad_url(country='us', language='en', hour=4, ad_configs=ad_configs) == 'https://www.222222.com'
        assert get_ad_url(country='us', language='en', hour=5, ad_configs=ad_configs) == 'https://www.222222.com'
        assert get_ad_url(country='us', language='en', hour=6, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=7, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=8, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=9, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=10, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=11, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=12, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=13, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=14, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=15, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=16, ad_configs=ad_configs) == 'https://www.333333.com'
        assert get_ad_url(country='us', language='en', hour=17, ad_configs=ad_configs) == 'https://www.222222.com'
        assert get_ad_url(country='us', language='en', hour=18, ad_configs=ad_configs) == 'https://www.222222.com'
        assert get_ad_url(country='us', language='en', hour=19, ad_configs=ad_configs) == 'https://www.222222.com'
        assert get_ad_url(country='us', language='en', hour=20, ad_configs=ad_configs) == 'https://www.111111.com'
        assert get_ad_url(country='us', language='en', hour=21, ad_configs=ad_configs) == 'https://www.111111.com'
        assert get_ad_url(country='us', language='en', hour=22, ad_configs=ad_configs) == 'https://www.111111.com'
        assert get_ad_url(country='us', language='en', hour=23, ad_configs=ad_configs) is None
