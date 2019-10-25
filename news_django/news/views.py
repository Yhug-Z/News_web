from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from news.models import News


def index(request):
    pass


def news(request, category):
    if request.method == "GET":
        news_list = get_news(category)
        if not news_list:
            response = {'code': 10501, 'content': '服务器错误,抱歉'}
            return JsonResponse(response)
        content = []
        for i in news_list:
            content.append({
                'id': i.id,
                'title': i.title,
                'source': i.source,
                'release_time': i.release_time,
                'comment_number': i.comment_number,
                'img': i.img
            })
        response = {'code': 200, 'content': content}
        return JsonResponse(response)


def get_news(category):
    classes = ""
    if category == "politics":
        classes = "国内"
    elif category == "foreign":
        classes = "国际"
    elif category == "finance":
        classes = "财经"
    elif category == "tec":
        classes = "科技"
    elif category == "sport":
        classes = "体育"
    elif category == "ent":
        classes = "娱乐"
    elif category == "house":
        classes = "房产"
    elif category == "auto":
        classes = "汽车"
    elif category == "internet":
        classes = "互联网"

    news_list = News.objects.filter(category=classes)[:30]
    return news_list


def article(request, news_id):
    if request.method == "GET":
        news_ = News.objects.filter(id=news_id)
        if not news_:
            response = {'code': 10502, 'error': 'Sorry,该文章丢失'}
            return JsonResponse(response)
        news_ = news_[0]
        response = {
            'code': 200,
            'data': {'title': news_.title, 'content': news_.content, 'release_time': news_.release_time,
                     'source': news_.source}
        }
        return JsonResponse(response)
