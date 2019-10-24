from django.conf.urls import url

from favorite import views

urlpatterns = [
    url(r'^/(?P<username>\w+)$', views.favorite),
    url(r'^/(?P<username>\w+)/(?P<title_id>\w+)$', views.favorite_news),
]
