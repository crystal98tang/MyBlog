"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # 主页面
    url(r'^index/', views.index),
    # 查询指定页
    url(r'article/$', views.find_page, name='find_page'),
    # 详细页跳转 参数id
    url(r'article/(?P<article_id>[0-9]+)$', views.article_page, name='article_page'),
    # 删除文章
    url(r'^article/action1/(?P<article_id>[0-9]+)$', views.article_delete, name='article_delete'),
    # 编辑页面
    url(r'^article/edit/(?P<article_id>[0-9]+)$', views.article_edit_page, name='article_edit_page'),
    # (?P<article_id>[0-9]+)
    # 编辑或新建的执行提交按钮
    url(r'^article/edit/action$', views.article_edit_page_action, name='article_edit_page_action'),
    # 新建评论
    url(r'^article/action2$', views.comment_create, name='comment_create'),
    # 删除评论
    url(r'^article/action3/(?P<comment_id>[0-9]+)$', views.comment_delete, name='comment_delete'),
]
