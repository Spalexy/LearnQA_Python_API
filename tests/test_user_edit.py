from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        new_name = 'Changed Name'

        response3 = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            'Wrong name of the user after edit'
        )

    def test_edit_user_without_authorisation(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        creation_response = self.create_new_user(register_data)

        # EDIT
        user_id = self.get_json_value(creation_response, 'id')
        data = {'firstName': 'Changed Name'}

        edit_response = MyRequests.put(
            f'/user/{user_id}',
            data=data
        )

        Assertions.assert_code_status(edit_response, 400)
        Assertions.assert_response_content(edit_response, 'Auth token not supplied')

    def test_edit_other_user(self):
        # FIRST USER REGISTER
        first_user_register_data = self.prepare_registration_data()
        self.create_new_user(first_user_register_data)

        email = first_user_register_data['email']
        password = first_user_register_data['password']

        # SECOND USER REGISTER
        second_user_register_data = self.prepare_registration_data()
        second_user_creation_response = self.create_new_user(second_user_register_data)

        second_user_id = self.get_json_value(second_user_creation_response, 'id')
        second_user_username = second_user_register_data['username']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        login_response = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(login_response, 'auth_sid')
        token = self.get_header(login_response, 'x-csrf-token')

        # EDIT
        new_user_name = 'Changed User Name'

        user_edit_response = MyRequests.put(
            f'/user/{second_user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'username': new_user_name}
        )

        Assertions.assert_code_status(user_edit_response, 200)

        # GET
        get_user_response = MyRequests.get(
            f'/user/{second_user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.assert_json_value_by_name(
            get_user_response,
            'username',
            second_user_username,
            'User name has been changed'
        )

    def test_edit_user_with_incorrect_email(self):
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

        # EDIT
        user_id = self.get_json_value(login_response, 'user_id')
        new_email = email.replace('@', '')

        edit_response = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'email': new_email}
        )

        Assertions.assert_code_status(edit_response, 400)
        Assertions.assert_response_content(edit_response, 'Invalid email format')

    def test_edit_user_to_one_symbol_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        register_response = self.create_new_user(register_data)

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

        # EDIT
        user_id = self.get_json_value(register_response, 'id')
        new_first_name = 'f'

        response3 = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_first_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_response_content(response3, '{"error":"Too short value for field firstName"}')
