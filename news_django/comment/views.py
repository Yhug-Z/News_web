import json

from django.db import transaction
from django.http import JsonResponse

# Create your views here.
from comment.models import Comment
from tools.logging_check import logging_check


def emit_comment(request):
    json_obj = _get_json(request)
    if not json_obj:
        result = {'code': 10300, 'error': 'Plase use json'}
        return result
    content = json_obj.get('content', None)
    if not content:
        result = {'code': 10301, 'error': 'Content empty'}
        return result
    parent_id = json_obj.get('parent_id', 0)
    news_id = _get_news_id(request)
    if not (Comment.objects.filter(id=parent_id,news_id=news_id) or parent_id==0):
        result={'code': 10311, 'error': 'Parent_id error'}
        return result
    try:
        Comment.objects.create(
            content=content,
            parent_id=parent_id,
            news_id=news_id,
            publisher=request.user
        )
    except Exception as e:
        print(e)
        result = {'code': 10310, 'error': 'Create failed'}
        return result
    result = {'code': 200, 'data': {}}
    return result


def _get_json(request):
    json_str = request.body
    try:
        json_obj = json.loads(json_str)
    except Exception as e:
        print(e)
        return {}
    return json_obj


def del_comment(request):
    json_obj = _get_json(request)
    comment_id = json_obj.get('comment_id', None)
    if not comment_id:
        result = {'code': 10302, 'error': 'Plase give comment_id'}
        return result
    comments = Comment.objects.filter(id=comment_id)
    if not comments:
        result = {'code': 10303, 'error': 'Comment_id  nonentity'}
        return result
    comment = comments[0]
    if comment.publisher != request.user:
        result = {'code': 10304, 'error': 'disobey del'}
        return result
    try:
        with transaction.atomic():
            Comment.objects.filter(parent_id=comment.id).delete()
            comment.delete()
            print('+++++++++++++')
    except Exception as e:
        print(e)
        result = {'code': 10305, 'error': 'Del failed'}
        return result
    result = {'code': 200, 'data': {}}
    return result


def _create_comment_dict(comments):
    """
        创建返回评论的字典结构
    :param comments: 评论列表
    :return:
    """
    comment_list = []
    parent_dict = {}
    count = 0
    for info in comments:
        if info.parent_id == 0:
            parent_dict[info.id] = {
                "id": info.id,
                "content": info.content,
                "publisher": info.publisher.nickname,
                "publisher_avatat": str(info.publisher.avatar),
                "reply": [],
                "created_time": info.created_time,
            }
            comment_list.append(parent_dict[info.id])
        else:
            info_dict = {
                "publisher": info.publisher.nickname,
                "publisher_avatar": str(info.publisher.avatar),
                "created_time": info.created_time,
                "content": info.content,
                "comment_id": info.id
            }
            parent_dict[info.parent_id]["reply"].append(info_dict)
        count += 1
    data = {
        "comment": comment_list,
        "comment_count": count
    }
    return {"code": 200, "data": data}


def get_comment(request):
    """
        获得评论
    :param request:
    :return:
    """
    print("------------------")
    news_id = _get_news_id(request)
    if news_id < 0:
        result = {'code': 10306, 'error': 'Get new_id failed'}
        return result
    comments = Comment.objects.filter(news_id=news_id)
    if not comments:
        result = {'code': 200, 'data': {'comment': [], 'comment_count': 0}}
        return result
    result = _create_comment_dict(comments)
    return result


def _get_news_id(request):
    """
        获得新闻ID
    :param request:
    :return:
    """
    try:
        news_id = int(request.GET.get('news_id', None))
    except Exception as e:
        print(e)
        return -1
    return news_id


@logging_check('POST', 'DELETE')
def comment(request):
    print(request.method)
    if request.method == 'POST':
        return JsonResponse(emit_comment(request))
    elif request.method == 'DELETE':
        return JsonResponse(del_comment(request))
    elif request.method == 'GET':
        return JsonResponse(get_comment(request))
    return JsonResponse({"code": 20000})
