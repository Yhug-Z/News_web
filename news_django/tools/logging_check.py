from django.http import JsonResponse
import jwt

from user.models import User

TOKEN_KEY = 'abc123abc'


def logging_check(*methods):
    def _logging_check(func):
        def _wrapper(request, *args, **kwargs):
            if not methods:
                return func(request, *args, **kwargs)

            if request.method not in methods:
                return func(request, *args, **kwargs)

            token = request.META.get('HTTP_AUTHORIZATION')
            if not token:
                response = {'code': 10207, 'error': '请登录'}
                return JsonResponse(response)

            try:
                res = jwt.decode(token, TOKEN_KEY, algorithms='HS256')
            except Exception as e:
                print(e)
                response = {'code': 10208, 'error': '请登录.'}
                return JsonResponse(response)

            username = res['username']

            try:
                user = User.objects.get(username=username)
            except Exception as e:
                print(e)
                response = {'code': 10209, 'error': '请登录..'}
                return JsonResponse(response)

            request.user = user

            return func(request, *args, **kwargs)
        return _wrapper
    return _logging_check


def get_user(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        return None

    try:
        res = jwt.decode(token, TOKEN_KEY, algorithms='HS256')
    except Exception as e:
        print(e)
        return None

    username = res['username']

    try:
        user = User.objects.get(username=username)
    except Exception as e:
        print(e)
        return None

    return user
