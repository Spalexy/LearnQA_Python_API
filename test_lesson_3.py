import pytest
import requests


test_data = [
    ({"user_agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 "
                    "(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
      "expected_platform": "Mobile",
      "expected_browser": "No",
      "expected_device": "Android"
      }),
    ({"user_agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
      "expected_platform": "Mobile",
      "expected_browser": "Chrome",
      "expected_device": "iOS"
      }),
    ({"user_agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
      "expected_platform": "Googlebot",
      "expected_browser": "Unknown",
      "expected_device": "Unknown"
      }),
    ({"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
      "expected_platform": "Web",
      "expected_browser": "Chrome",
      "expected_device": "No"
      }),
    ({"user_agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                    "Version/13.0.3 Mobile/15E148 Safari/604.1",
      "expected_platform": "Mobile",
      "expected_browser": "No",
      "expected_device": "iPhone"
      }),
]


@pytest.mark.skip
def test_short_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, 'Phrase is too long'


def test_request_for_cookies():
    response = requests.get('https://playground.learnqa.ru/api/homework_cookie')
    print(dict(response.cookies))
    assert 'HomeWork' in response.cookies, 'There is no HomeWork field in cookies'
    assert response.cookies.get('HomeWork') == 'hw_value', 'Wrong value of HomeWork field'


def test_request_for_headers():
    response = requests.get('https://playground.learnqa.ru/api/homework_header')
    print(dict(response.headers))
    assert 'x-secret-homework-header' in response.headers, 'There is no x-secret-homework-header field in headers'
    assert response.headers.get('x-secret-homework-header') == 'Some secret value', \
        'Wrong value of x-secret-homework-header field'


@pytest.mark.parametrize('data', test_data)
def test_user_agent(data):
    response = requests.get('https://playground.learnqa.ru/ajax/api/user_agent_check',
                            headers={"User-Agent": data['user_agent']})

    assert 'platform' and 'browser' and 'device' in response.json(), 'Not all parameters are present in the response'

    assert response.json()['platform'] == data['expected_platform'], 'Invalid platform value'
    assert response.json()['browser'] == data['expected_browser'], 'Invalid browser value'
    assert response.json()['device'] == data['expected_device'], 'Invalid device value'
