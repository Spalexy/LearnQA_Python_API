import pytest
import allure

from random import choice
from string import ascii_letters

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user_successfully(self):
        data = BaseCase.prepare_registration_data(self)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = BaseCase.prepare_registration_data(self, email)

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, f'Users with email \'{email}\' already exists')

    @allure.testcase(
        url='https://software-testing.ru/lms/mod/assign/view.php?id=207353',
        name='Создание пользователя с некорректным email'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_with_incorrect_email(self):
        data = BaseCase.prepare_registration_data(self, 'incorrectemail.com')
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, 'Invalid email format')

    @allure.testcase(
        url='https://software-testing.ru/lms/mod/assign/view.php?id=207353',
        name='Создание пользователя без указания одного из полей'
    )
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('param', ('password', 'username', 'firstName', 'lastName', 'email'))
    def test_create_user_without_one_parameter(self, param):
        data = BaseCase.prepare_registration_data(self)
        data.pop(param)
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, 'The following required params are missed: {}'.format(param))

    @allure.testcase(
        url='https://software-testing.ru/lms/mod/assign/view.php?id=207353',
        name='Создание пользователя с очень коротким именем в один символ'
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_one_symbol_name(self):
        data = BaseCase.prepare_registration_data(self)
        data.update({'firstName': 'l'})
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, 'The value of \'firstName\' field is too short')

    @allure.testcase(
        url='https://software-testing.ru/lms/mod/assign/view.php?id=207353',
        name='Создание пользователя с очень длинным именем'
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_very_long_name(self):
        data = BaseCase.prepare_registration_data(self)
        first_name = ''.join(choice(ascii_letters) for i in range(251))
        data.update({'firstName': first_name})
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_content(response, 'The value of \'firstName\' field is too long')

