from requests import get
from json import loads
from time import sleep


api_url = 'https://playground.learnqa.ru/ajax/api/longtime_job'


def request(url, payload=None):
    if payload is None:
        payload = {}
    response = get(url, payload).text
    response_as_object = loads(response)
    return response_as_object


obj = request(api_url)
api_token, execution_time = obj['token'], obj['seconds']

request_payload = {'token': api_token}
obj = request(api_url, request_payload)
assert obj['status'] == 'Job is NOT ready'

sleep(execution_time + 1)
request_payload = {'token': api_token}
obj = request(api_url, request_payload)
print(obj)
assert obj['status'] == 'Job is ready'
assert obj['result']
