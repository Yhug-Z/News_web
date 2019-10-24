"""

"""
import json

import requests

# data={'title':'aaa'}
data = {'news_id': 1}

data = json.dumps(data)

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFiYyIsImV4cCI6MTU3MTgzMDYyMS4yNjUzMDU4fQ.5j9NkhSgailga4BFyimvD64JVOxBKab4y19Pw2zpLZk'

header = {
    'Authorization': token
}

html=requests.post(url='http://176.47.10.229:8000/v1/favorite/abc/4',headers=header,data=data)
# print(html.json())
# html=requests.get(url='http://176.47.10.229:8000/v1/favorite/abc/3',headers=header)
# print(html.json())
# html = requests.delete(url='http://176.47.10.229:8000/v1/favorite/abc/3', headers=header, data=data)
# print(html.json())
# html=requests.get(url='http://176.47.10.229:8000/v1/favorite/abc/3',headers=header)
print(html.json())

