from django.conf.urls import url

from news import views

urlpatterns = [
    url(r'^/$', views.index),
    url(r'^/([a-z]*)$', views.news),
    url(r'^/([0-9]*)', views.article),
]
