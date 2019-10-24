from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True, verbose_name='用户名')
    nickname = models.CharField(max_length=30, verbose_name='昵称')
    password = models.CharField(max_length=32, verbose_name='密码')
    avatar = models.ImageField(upload_to='avatar/', verbose_name='头像')
    signature = models.CharField(max_length=90, verbose_name='个性签名')
    gender = models.CharField(max_length=1, verbose_name='性别')
    birthday = models.DateField(verbose_name='生日')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'user'

