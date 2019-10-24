from django.db import models

# Create your models here.
from news.models import News
from user.models import User


class Comment(models.Model):
    content=models.TextField(verbose_name='留言内容')
    created_time=models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    parent_id=models.IntegerField(verbose_name='留言ID',default=0)
    publisher=models.ForeignKey(User)
    news=models.ForeignKey(News)

    class Meta:
        db_table='comment'