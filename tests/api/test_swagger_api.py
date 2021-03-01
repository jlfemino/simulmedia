import pytest

from simulmedia.services.config import config_parser
from tests.base_test import BaseTest


@pytest.mark.usefixtures('init_app_context')
class TestSwaggerApi(BaseTest):
    def test__spec__happy_path(self, test_client):
        response = test_client.get('http://localhost:5000/spec')
        assert response.status_code == 200
        assert response.json is not None
        assert response.json['info']['title'] == config_parser['ENV_TEST']['SWAGGER_INFO_TITLE']
        assert response.json['info']['version'] == config_parser['ENV_TEST']['SWAGGER_INFO_VERSION']
        print(response.json)
