from django.db import models


# Create your models here.

class News(models.Model):
    title = models.CharField(verbose_name="新闻标题", max_length=300)
    source = models.CharField(verbose_name="来源", max_length=30)
    release_time = models.DateField(verbose_name='发布时间')
    content = models.TextField(verbose_name='新闻内容')
    category = models.CharField(verbose_name='新闻类别', max_length=30)
    comment_number = models.IntegerField(verbose_name='评论数量', default=0)
    img = models.CharField(verbose_name='新闻图片',max_length=200,null=True)

    class Meta:
        db_table = 'news'
