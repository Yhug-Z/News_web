import json

from django.http import JsonResponse

# Create your views here.
from favorite.models import Favorite
from news.models import News
from tools.logging_check import logging_check


def favorite_get(request, username):
    """
        获取收藏夹
    :param request:
    :param username:
    :return:
    """
    if username != request.user.username:
        result = {'code': 10405, 'error': 'username 错误'}
        return JsonResponse(result)
    favorite_list = Favorite.objects.filter(user=request.user)
    data = {
        'favorites': [],
        'count': 0
    }
    for fav in favorite_list:
        data['favorites'].append(
            {
                'title': fav.title,
                'favorite_id': fav.id
            }
        )
        data['count'] += 1
    result = {'code': 200, 'data': data}
    return JsonResponse(result)


def favorite_del(request, username):
    """
        删除收藏夹
    :param request:
    :param username:
    :return:
    """
    json_obj = _get_json(request)
    if not json_obj:
        result = {'code': 10406, 'error': 'json 数据不存在'}
        return JsonResponse(result)
    favorite_id = json_obj.get('favorite_id', None)
    if not favorite_id:
        result = {'code': 10407, 'error': 'favorite_id 数据不存在'}
        return JsonResponse(result)
    if username != request.user.username:
        result = {'code': 10408, 'error': 'user 错误'}
        return JsonResponse(result)
    favorite_list = Favorite.objects.filter(id=favorite_id, user=request.user)
    if not favorite_list:
        result = {'code': 10409, 'error': '收藏夹不存在'}
        return JsonResponse(result)
    try:
        favorite_list.delete()
    except Exception as e:
        print(e)
        result = {'code': 10410, 'error': '删除失败'}
        return JsonResponse(result)
    result = {'code': 200, 'data': {}}
    return JsonResponse(result)


@logging_check('POST', 'GET', 'DELETE')
def favorite(request, username):
    """
        收藏夹请求处理
    :param request:
    :param username:
    :return:
    """
    if request.method == "POST":
        return favorite_post(request, username)
    elif request.method == "GET":
        return favorite_get(request, username)
    elif request.method == "DELETE":
        return favorite_del(request, username)

    return JsonResponse({'code': 20000})


def favorite_post(request, username):
    """
        创建收藏夹
    :param request:
    :param username:
    :return:
    """
    json_obj = _get_json(request)
    if not json_obj:
        result = {'code': 10401, 'error': '请求为空'}
        return JsonResponse(result)
    title = json_obj.get('title', None)
    if not title:
        result = {'code': 10402, 'error': 'title不能为空'}
        return JsonResponse(result)
    if username != request.user.username:
        result = {'code': 10403, 'error': 'username 错误'}
        return JsonResponse(result)
    if Favorite.objects.filter(title=title, user=request.user):
        result = {'code': 10412, 'error': '收藏夹重名'}
        return JsonResponse(result)
    try:
        Favorite.objects.create(title=title, user=request.user)
    except Exception as e:
        print(e)
        result = {'code': 10404, 'error': '创建收藏夹 错误'}
        return JsonResponse(result)
    result = {'code': 200, 'data': {}}
    return JsonResponse(result)


def _get_json(request):
    """
        处理json
    :param request:
    :return:
    """
    json_str = request.body
    try:
        json_obj = json.loads(json_str)
    except Exception as e:
        print(e)
        return {}
    return json_obj


def favorite_news_post(request, title_id):
    """
        收藏新闻添加
    :param request:
    :param title_id:
    :return:
    """
    json_obj = _get_json(request)
    if not json_obj:
        result = {'code': 10413, 'error': 'json 错误'}
        return result
    news_id = json_obj.get('news_id', None)
    if not news_id:
        result = {'code': 10414, 'error': 'news_id 缺失'}
        return result
    news = News.objects.filter(id=news_id)
    if not news:
        result = {'code': 10415, 'error': 'news不存在'}
        return result
    news = news[0]
    favorite = Favorite.objects.filter(id=title_id, user=request.user)[0]
    if news in favorite.news.all():
        result = {'code': 10417, 'error': '添加新闻以添加'}
        return result
    try:
        favorite.news.add(news)
    except Exception as e:
        print(e)
        result = {'code': 10416, 'error': '添加新闻失败'}
        return result
    result = {'code': 200, 'data': {}}
    return result


def favorite_news_get(request, title_id):
    favorite = Favorite.objects.filter(id=title_id, user=request.user)[0]
    news_list = favorite.news.all()
    data = {
        'news': [],
        'count': 0
    }
    for news in news_list:
        data['news'].append({
            'title': news.title,
            'news_id': news.id
        })
        data['count'] += 1
    result = {'code': 200, 'data': data}
    return result


def favorite_news_delete(request, title_id):
    """
        删除收藏夹新闻
    :param request:
    :param title_id:
    :return:
    """
    json_obj = _get_json(request)
    if not json_obj:
        result = {'code': 10418, 'error': 'json 错误'}
        return result
    news_id = json_obj.get('news_id', None)
    if not news_id:
        result = {'code': 10419, 'error': 'news_id 缺失'}
        return result
    favorite = Favorite.objects.filter(id=title_id, user=request.user)[0]
    if not favorite.news.filter(id=news_id):
        result = {'code': 10420, 'error': '收藏夹中新闻不存在'}
        return result
    try:
        news=News.objects.get(id=news_id)
        favorite.news.remove(news)
    except Exception as e:
        print(e)
        result = {'code': 10421, 'error': '收藏夹中新闻删除失败'}
        return result
    result = {'code': 200, 'data': {}}
    return result


def _is_same_user_and_username(user, username):
    if user.username == username:
        return True
    else:
        return False


def _is_exist_favorite(request, title_id):
    try:
        Favorite.objects.get(id=title_id, user=request.user)
    except Exception as e:
        print(e)
        return False
    return True


@logging_check('POST', 'GET', 'DELETE')
def favorite_news(request, username, title_id):
    """
        处理收藏夹中新闻请求
    :param request:
    :param username:
    :param title_id:
    :return:
    """
    if not _is_same_user_and_username(request.user, username):
        result = {'code': 10411, 'error': '用户非法访问'}
        return JsonResponse(result)
    if not _is_exist_favorite(request, title_id):
        result = {'code': 10412, 'error': '用户收藏夹不存在'}
        return JsonResponse(result)
    if request.method == 'POST':
        return JsonResponse(favorite_news_post(request, title_id))
    elif request.method == 'GET':
        return JsonResponse(favorite_news_get(request, title_id))
    elif request.method == 'DELETE':
        return JsonResponse(favorite_news_delete(request, title_id))

    return JsonResponse({'code': 20000})
