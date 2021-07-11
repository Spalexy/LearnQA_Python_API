import requests
import pytest

from random import choice
from string import ascii_letters

from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = BaseCase.prepare_registration_data(self)

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = BaseCase.prepare_registration_data(self, email)

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f'Users with email \'{email}\' already exists')

    def test_create_user_with_incorrect_email(self):
        data = BaseCase.prepare_registration_data(self, 'incorrectemail.com')
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, 'Invalid email format')

    @pytest.mark.parametrize('param', ('password', 'username', 'firstName', 'lastName', 'email'))
    def test_create_user_without_one_parameter(self, param):
        data = BaseCase.prepare_registration_data(self)
        data.pop(param)
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, 'The following required params are missed: {}'.format(param))

    def test_create_user_with_one_symbol_name(self):
        data = BaseCase.prepare_registration_data(self)
        data.update({'firstName': 'l'})
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, 'The value of \'firstName\' field is too short')

    def test_create_user_with_very_long_name(self):
        data = BaseCase.prepare_registration_data(self)
        first_name = ''.join(choice(ascii_letters) for i in range(251))
        data.update({'firstName': first_name})
        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, 'The value of \'firstName\' field is too long')

