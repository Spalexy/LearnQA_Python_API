import requests

response = requests.get('https://playground.learnqa.ru/api/long_redirect', allow_redirects=True)

if response.history:
    print("Всего произошло {} редиректа".format(len(response.history)))
    print("Итоговый URL: {}".format(response.url))
else:
    print("Редиректов не было")
