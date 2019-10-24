from django.db import models

# Create your models here.
from news.models import News
from user.models import User


class Favorite(models.Model):
    title=models.CharField('收藏夹名',max_length=300)
    user=models.ForeignKey(User)
    news=models.ManyToManyField(News)

    class Meta:
        db_table='favorite'
