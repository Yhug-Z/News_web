from django.http import JsonResponse
import json
from .models import User
from btoken.views import make_token, get_password
from tools.logging_check import logging_check


def register_user(request):
    response = {}
    json_str = request.body
    print('json-str:', json_str)
    # 数据可用性判断
    if not json_str:
        response['code'] = 10100
        response['error'] = '请求中无内容'
        return JsonResponse(response)
    try:
        json_obj = json.loads(json_str)
    except Exception as e:
        print(e)
        response['code'] = 10101
        response['error'] = '请求内容格式有问题'
        return JsonResponse(response)
    username = json_obj.get('username')
    gender = json_obj.get('gender')
    birthday = json_obj.get('birthday')
    password_1 = json_obj.get('password_1')
    password_2 = json_obj.get('password_2')
    if not username:
        response['code'] = 10102
        response['error'] = '请求中未提交用户名'
        return JsonResponse(response)
    if not gender:
        response['code'] = 10103
        response['error'] = '请求中未提交性别'
        return JsonResponse(response)
    if not birthday:
        response['code'] = 10104
        response['error'] = '请求中未提交生日'
        return JsonResponse(response)
    if not password_1 or not password_2:
        response['code'] = 10105
        response['error'] = '请求中未提交密码'
        return JsonResponse(response)
    if password_1 != password_2:
        response['code'] = 10106
        response['error'] = '两次提交的密码不一致'
        return JsonResponse(response)

    # 检查当前用户名是否可用
    users = User.objects.filter(username=username)
    if users:
        response['code'] = 10107
        response['error'] = '用户名已存在'
        return JsonResponse(response)

    # 创建用户
    try:
        user_obj = User()
        user_obj.username = username
        user_obj.nickname = username
        user_obj.password = get_password(password_1)
        user_obj.gender = gender
        user_obj.birthday = birthday
        user_obj.save()
    except Exception as e:
        print(e)
        response['code'] = 10108
        response['error'] = '用户名已存在.'
        return JsonResponse(response)

    # 计算token
    token = make_token(username)
    response['code'] = 200
    response['username'] = username
    response['data'] = {"token": token.decode()}
    return JsonResponse(response)


def get_user(request, username):
    if username is None:
        return JsonResponse({'code': 200001})

    user_objs = User.objects.filter(username=username)
    if len(user_objs) != 1:
        return JsonResponse({'code': 10109, 'error': '没有这个用户'})

    user = user_objs[0]

    data = {'username': user.username,
            'nickname': user.nickname,
            'gender': user.gender,
            'signature': user.signature,
            'birthday': user.birthday,
            'avatar': str(user.avatar),
            }
    return JsonResponse({'code': 200, 'data': data})


def update_user(request, username):
    json_str = request.body
    if not json_str:
        response = {'code': 10100, 'error': '请求中无内容'}
        return JsonResponse(response)
    try:
        json_obj = json.loads(json_str)
    except Exception as e:
        print(e)
        response = {'code': 10101, 'error': '请求内容格式有问题'}
        return JsonResponse(response)
    if username is None:
        response = {'code': 10108, 'error': '用户名不存在'}
        return JsonResponse(response)

    user_obj = request.user

    if username != user_obj.username:
        response = {'code': 10115, 'error': '登录信息有误, 请重新登录'}
        return JsonResponse(response)

    is_changed = False

    nickname = json_obj.get('nickname')
    signature = json_obj.get('signature')
    gender = json_obj.get('gender')
    birthday = json_obj.get('birthday')

    if nickname is not None and nickname != user_obj.nickname:
        is_changed = True
        user_obj.nickname = nickname

    if signature is not None and signature != user_obj.signature:
        is_changed = True
        user_obj.signature = signature

    if gender is not None and gender != user_obj.gender:
        is_changed = True
        user_obj.gender = gender

    if birthday is not None and birthday != user_obj.birthday:
        is_changed = True
        user_obj.birthday = birthday

    if is_changed:
        try:
            user_obj.save()
        except Exception as e:
            print(e)
            response = {'code': 10109, 'error': '修改用户信息失败'}
            return JsonResponse(response)

    response = {'code': 200, 'username': username}
    return JsonResponse(response)


# Create your views here.
@logging_check('PUT', 'GET')
def users(request, username=None):

    if request.method == 'GET':
        return get_user(request, username)
    elif request.method == 'POST':
        return register_user(request)
    elif request.method == 'PUT':
        return update_user(request, username)
    return JsonResponse({'code': 2000000})


@logging_check('POST')
def users_avatar(request, username):
    # 用户上传头像
    if request.method != 'POST':
        response = {'code': 10110, 'error': '请求并非POST'}
        return JsonResponse(response)

    user_obj = request.user

    if username != user_obj.username:
        response = {'code': 10115, 'error': '登录信息有误, 请重新登录'}
        return JsonResponse(response)

    user_avatar = request.FILES.get('avatar')
    if not user_avatar:
        response = {'code': 10112, 'error': '没有头像'}
        return JsonResponse(response)

    user_obj.avatar = user_avatar
    try:
        user_obj.save()
    except Exception as e:
        print(e)
        response = {'code': 10113, 'error': '头像修改失败'}
        return JsonResponse(response)

    response = {'code': 200, 'username': username}
    return JsonResponse(response)


@logging_check('PUT')
def users_password(request, username):
    if request.method != 'PUT':
        response = {'code': 10120, 'error': '请求并非PUT'}
        return JsonResponse(response)

    if request.user.username != username:
        response = {'code': 10121, 'error': '用户名不匹配'}
        return JsonResponse(response)

    json_str = request.body

    if not json_str:
        response = {'code': 10122, 'error': '请求中无内容'}
        return JsonResponse(response)
    try:
        json_obj = json.loads(json_str)
    except Exception as e:
        print(e)
        response = {'code': 10123, 'error': '请求内容格式有问题'}
        return JsonResponse(response)

    old_password = json_obj.get('old_password')
    password_1 = json_obj.get('password_1')
    password_2 = json_obj.get('password_2')

    if not old_password or not password_1 or password_2:
        response = {'code': 10124, 'error': '请填写密码'}
        return JsonResponse(response)

