import pytest

from simulmedia.dao.user_dao import UserDao
from simulmedia.types.user import User
from tests.base_test import BaseTest


@pytest.mark.usefixtures('init_db')
class TestUserDao(BaseTest):
    def test__get_by_id__happy_path(self):
        user_dao: UserDao = UserDao.get_instance()

        user: User = user_dao.get_by_id('e38c6813-5228-4f59-a250-c5948a054502')
        assert user is not None
        assert user.name == 'Nomi'

        user = user_dao.get_by_id('1007b32d-e692-454f-b1cb-acf1e7e6e01a')
        assert user is not None
        assert user.name == 'Baruta'
