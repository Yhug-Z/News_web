"""

"""
import json

import requests

data={'content':'aaa','parent_id':9}
# data = {'comment_id': 1}

data = json.dumps(data)

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFiYyIsImV4cCI6MTU3MTgzMDYyMS4yNjUzMDU4fQ.5j9NkhSgailga4BFyimvD64JVOxBKab4y19Pw2zpLZk'

header = {
    'Authorization': token
}

html=requests.post(url='http://176.47.10.229:8000/v1/comment?news_id=1',headers=header,data=data)
# html = requests.delete(url='http://176.47.10.229:8000/v1/comment?news_id=1', headers=header, data=data)
print(html.json())
