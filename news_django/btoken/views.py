from django.http import JsonResponse
from django.shortcuts import render
import json
import hashlib
import jwt
import time
from user.models import User
from tools.logging_check import TOKEN_KEY


def make_token(username, expire=86400):
    key = TOKEN_KEY
    now_t = time.time()
    payload = {'username': username, 'exp': now_t + expire}
    return jwt.encode(payload, key, algorithm='HS256')


def get_password(pwd):
    """
    获取加密后的密码
    :param pwd: 源密码
    :return: 加密密码
    """
    h = hashlib.md5()
    h.update(pwd.encode())
    return h.hexdigest()


# Create your views here.
def tokens(request):
    if request.method != 'POST':
        response = {'code': 10200, 'error': '请求并非POST'}
        return JsonResponse(response)

    # 获取数据
    json_str = request.body
    if not json_str:
        response = {'code': 10201, 'error': '请求为空'}
        return JsonResponse(response)

    try:
        json_obj = json.loads(json_str)
    except Exception as e:
        print(e)
        response = {'code': 10202, 'error': '请求格式有问题'}
        return JsonResponse(response)

    username = json_obj.get('username')
    password = json_obj.get('password')
    if not username:
        response = {'code': 10203, 'error': '请求中未提交用户名'}
        return JsonResponse(response)
    if not password:
        response = {'code': 10204, 'error': '请求中未提交密码'}
        return JsonResponse(response)

    # 查询数据
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        print(e)
        response = {'code': 10205, 'error': '用户名不存在'}
        return JsonResponse(response)

    if user.password != get_password(password):
        response = {'code': 10206, 'error': '密码错误'}
        return JsonResponse(response)

    # 创建token
    token = make_token(username)
    response = {'code': 200, 'username': username, 'data': {'token': token.decode()}}
    return JsonResponse(response)
