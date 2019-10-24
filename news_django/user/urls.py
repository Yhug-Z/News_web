from django.conf.urls import url
from . import views


urlpatterns = [
    # http://127.0.0.1:8000/v1/users
    url(r'^$', views.users),
    # http://127.0.0.1:8000/v1/users/<username>
    url(r'^/(?P<username>\w+)$', views.users),
    # http://127.0.0.1:8000/v1/users/<username>/avatar
    url(r'^/(?P<username>\w+)/avatar$', views.users_avatar),
    # http://127.0.0.1:8000/v1/users/<username>/password
    url(r'^/(?P<username>\w+)/password$', views.users_password)
]
