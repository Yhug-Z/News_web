from django.conf.urls import url

from comment import views

urlpatterns = [
    url(r'^$', views.comment),
]