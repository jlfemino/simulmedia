import pytest
from main import app


class TestApi:
    # ================================================================================
    # Flask functional testing
    # ================================================================================
    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    def test__get_ad_url__(self):
        with app.test_client() as client:
            response = client.get('http://localhost:5000/ad/can/fre/2')
            assert response.status_code == 200
            assert response.data == b'https://www.youtube.com/watch?v=Jm932Sqwf5E'
