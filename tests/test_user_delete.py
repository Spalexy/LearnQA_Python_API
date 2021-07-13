import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_try_to_delete_protected_user(self):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        login_response = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(login_response, 'auth_sid')
        token = self.get_header(login_response, 'x-csrf-token')
        user_id = self.get_json_value(login_response, 'user_id')

        # DELETE
        delete_response = MyRequests.delete(f'/user/{user_id}',
                                            headers={'x-csrf-token': token},
                                            cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(delete_response, 400)
        Assertions.assert_response_content(delete_response, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')

    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        self.create_new_user(register_data)

        email = register_data['email']
        password = register_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        login_response = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(login_response, 'auth_sid')
        token = self.get_header(login_response, 'x-csrf-token')
        user_id = self.get_json_value(login_response, 'user_id')

        # DELETE
        delete_response = MyRequests.delete(f'/user/{user_id}',
                                            headers={'x-csrf-token': token},
                                            cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(delete_response, 200)

        # CHECK
        get_user_response = MyRequests.get(f'/user/{user_id}')

        Assertions.assert_code_status(get_user_response, 404)
        Assertions.assert_response_content(get_user_response, 'User not found')

    def test_try_to_delete_other_user(self):
        # FIRST USER REGISTER
        first_user_register_data = self.prepare_registration_data()
        self.create_new_user(first_user_register_data)

        email = first_user_register_data['email']
        password = first_user_register_data['password']

        # SECOND USER REGISTER
        second_user_register_data = self.prepare_registration_data()
        second_user_creation_response = self.create_new_user(second_user_register_data)

        second_user_id = self.get_json_value(second_user_creation_response, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        login_response = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(login_response, 'auth_sid')
        token = self.get_header(login_response, 'x-csrf-token')

        # DELETE
        delete_response = MyRequests.delete(f'/user/{second_user_id}',
                                            headers={'x-csrf-token': token},
                                            cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(delete_response, 200)

        # CHECK
        get_user_response = MyRequests.get(f'/user/{second_user_id}')

        Assertions.assert_code_status(get_user_response, 200)
        Assertions.assert_response_content(get_user_response, '{"username":"learnqa"}')
