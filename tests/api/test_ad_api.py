import pytest

from simulmedia.api.ad_api import get_ad_url
from tests.base_test import BaseTest

# TODO: Refactor unit tests to initialize DB in test.
# TODO: Use a library method to compare URLs for equivalency (not str == str).
user_id: str = 'e38c6813-5228-4f59-a250-c5948a054502'


@pytest.mark.usefixtures('init_db', 'init_app_context')
class TestAdApiUnit(BaseTest):
    # ================================================================================
    # get_ad_url_short
    # ================================================================================
    def test__get_ad_url_short__unit_test__user_not_found(self):
        response = get_ad_url(
            user_id='bogus_user_id',
            country='US',
            language='en')
        assert response.status_code == 400

    # ================================================================================
    # get_ad_url
    # ================================================================================
    def test__get_ad_url__unit_test__user_not_found(self):
        response = get_ad_url(
            user_id='bogus_user_id',
            country='US',
            language='en',
            hour=1)
        assert response.status_code == 400


@pytest.mark.usefixtures('init_db')
class TestAdApiFunctional(BaseTest):
    # ================================================================================
    # get_ad_url_short
    # ================================================================================
    def test__get_ad_url_short__user_not_found(self, test_client):
        response = test_client.get(f'http://localhost:5000/ad/xxx/RO/ro')
        assert response.status_code == 400
        assert 'User not found' in str(response.data)

    def test__get_ad_url_short__country_not_found(self, test_client):
        response = test_client.get(f'http://localhost:5000/ad/{user_id}/xxx/ro')
        assert response.status_code == 400
        assert 'Country not found' in str(response.data)

    def test__get_ad_url_short__language_not_found(self, test_client):
        response = test_client.get(f'http://localhost:5000/ad/{user_id}/RO/xxx')
        assert response.status_code == 400
        assert 'Language not found' in str(response.data)

    def test__get_ad_url_short__happy_path(self, test_client):
        response = test_client.get(f'http://localhost:5000/ad/{user_id}/RO/ro')
        assert response.status_code == 200
        assert response.data == b'http://www.111111.ro/'

    # ================================================================================
    # get_ad_url
    # ================================================================================
    def test__get_ad_url__user_not_found(self, test_client):
        response = test_client.get(f'http://localhost:5000/ad/xxx/RO/ro/0')
        assert response.status_code == 400
        assert 'User not found' in str(response.data)

    def test__get_ad_url__country_not_found(self, test_client):
        response = test_client.get(f'http://localhost:5000/ad/{user_id}/xxx/ro/0')
        assert response.status_code == 400
        assert 'Country not found' in str(response.data)

    def test__get_ad_url__language_not_found(self, test_client):
        response = test_client.get(f'http://localhost:5000/ad/{user_id}/RO/xxx/0')
        assert response.status_code == 400
        assert 'Language not found' in str(response.data)

    def test__get_ad_url__happy_path(self, test_client):
        response = test_client.get(f'http://localhost:5000/ad/{user_id}/RO/ro/0')
        assert response.status_code == 200
        assert response.data == b'http://www.111111.ro/'
