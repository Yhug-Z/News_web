import requests

import json


def test_post(url, headers=None, data=None):
    print('test_post begin, url:', url, 'data:', data)
    try:
        res = requests.post(url=url, data=data, headers=headers, timeout=3)
    except Exception as e:
        print(e)
        return
    print('test_post ok.', res.status_code, json.loads(res.text))


def test_get(url, headers=None, params=None):
    print('test_get begin, url:', url)
    try:
        res = requests.get(url=url, params=params, headers=headers, timeout=3)
    except Exception as e:
        print(e)
        return
    print('test_get ok.', res.status_code, json.loads(res.text))


if __name__ == '__main__':
    url = 'http://176.47.10.229:8000/v1/users/abc'
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFiYyIsImV4cCI6MTU3MTgzMDYyMS4yNjUzMDU4fQ.5j9NkhSgailga4BFyimvD64JVOxBKab4y19Pw2zpLZk'
    # token = 'eyJ1c2VybmFtZSI6ImFiYyIsImV4cCI6MTU3MTgyOTAxNy43MTU1NDY2fQ.G' \
    #         '-mIefmGvCZLKR8nm4hV7oMksg_6kKcrcK6sJm3hnQo'
    # data = {'username': 'abc',
    #         'password_1': '123456',
    #         'password_2': '123456',
    #         'gender': 'f',
    #         'birthday': '1999-12-10'}
    # data = json.dumps(data)
    # test_post(url=url, data=data)

    headers = {'Authorization': token}

    test_get(url=url, headers=headers)
