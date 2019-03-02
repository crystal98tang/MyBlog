from django.db import models

from django.contrib.auth.models import User # 使用的SQLite自动生成的“用户”表
#### Power by Tang
# 调用方法：
#           a = models.User.objects.get(#匹配条件#)
#           b = models.User.objects.all()
#           a.item = #修改参数#
#           for i in b:
#               #修改或获取
#               i.message = 修改或获取
# username（用户名）、Password（密码)


class Article(models.Model):
    title = models.CharField(max_length=32, default='')
    author = models.CharField(max_length=32, default='')
    content = models.TextField(null=True)
    last_edit = models.CharField(max_length=32, default='')
    art_good = models.IntegerField(default=0)
    com_sum = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article_part_of = models.CharField(max_length=32, default='')
    comment_user = models.CharField(max_length=32, default='')
    content = models.TextField(max_length=500, null=False)
    creation_time = models.CharField(max_length=32, default='')
    state = models.CharField(max_length=8, default='0')

    def __str__(self):
        return self.comment_user