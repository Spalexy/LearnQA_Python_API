import requests

api_url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'


# 1
response = requests.get(api_url)
print(response.status_code, response.text)

# 2
payload = {'method': 'HEAD'}
response = requests.head(api_url, data=payload)
print(response.status_code, response.text)

# 3
payload = {'method': 'GET'}
response = requests.get(api_url, params=payload)
print(response.status_code, response.text)

# 4
methods = {'POST', 'GET', 'PUT', 'DELETE', 'HEAD', 'DELETE', 'PATCH', 'CONNECT', 'OPTIONS', 'TRACE'}


def make_request(meth_name, url, request_payload):
    if meth_name == 'GET':
        resp = requests.request(meth_name, url, params=request_payload)
    else:
        resp = requests.request(meth_name, url, data=request_payload)
    return resp


for meth in methods:
    for meth_label in methods:
        payload = {'method': meth_label}
        response = make_request(meth, api_url, payload)
        if meth != meth_label and response.status_code == 200 and response.text == '{"success":"!"}':
            print('Ooops! Wrong server response:', meth, meth_label, response.status_code, response.text)
