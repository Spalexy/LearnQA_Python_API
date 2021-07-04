import pytest
import requests


@pytest.mark.skip
def test_short_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, 'Phrase is too long'


def test_request_for_cookies():
    response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
    print(dict(response.cookies))
    assert 'HomeWork' in response.cookies, 'There is no HomeWork field in cookies'
    assert response.cookies.get('HomeWork') == 'hw_value', 'Wrong value of HomeWork field'
