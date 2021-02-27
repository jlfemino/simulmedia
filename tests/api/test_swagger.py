import pytest

from main import app
from simulmedia.config import config_parser


class TestSwagger:
    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    def test__spec__happy_path(self):
        with app.test_client() as client:
            response = client.get('http://localhost:5000/spec')
            assert response.status_code == 200
            assert response.json is not None
            assert response.json['info']['title'] == config_parser['SWAGGER']['INFO_TITLE']
            assert response.json['info']['version'] == config_parser['SWAGGER']['INFO_VERSION']
            print(response.json)
