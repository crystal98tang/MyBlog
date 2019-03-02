from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render_to_response
from . import models
import datetime
from django.contrib.auth.models import User

"""""""""""""""""""""""""""""""""""""""""""""""""""
# release：0.0.1
# 修改：1.tang - 所有注释 <2019-1-10 15:35>
#       2.tang - article_page中传递comment遇到问题
#
"""""""""""""""""""""""""""""""""""""""""""""""""""

"""""""""""""""""""""""""""""""""""""""""""""""""""
#login处理登陆账号密码
"""""""""""""""""""""""""""""""""""""""""""""""""""


def login(request):
    message = ""  # 标注提示信息为空
    if request.method == "POST":  # 登录信息验证
        user = request.POST['user']  # 得到登录页面的内容
        password = request.POST['password']  # 同上
        if user and password:  # 确保用户名和密码都不为空
            try:
                users = models.User.objects.get(username=user)  # 获取该对象的信息
                if check_password(password, users.password):
                    users.last_login = datetime.datetime.now()  # 记录登陆时间
                    request.session['username'] = user
                    users.save()
                    return HttpResponseRedirect('/blog/index')
                else:
                    message = "密码不正确！"
            except ObjectDoesNotExist:
                message = "用户名不存在！"
    return render(request, 'login.html', {"message": message})


###用于加密明文密码（备用，留作注册页面使用）
# users.password = make_password(password, None, 'pbkdf2_sha256')

"""""""""""""""""""""""""""""""""""""""""""""""""""
#注册 na
"""""""""""""""""""""""""""""""""""""""""""""""""""


def register(request):
    errors = []
    account = None
    password = None
    email = None
    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('用户名不能为空')
        else:
            account = request.POST.get('account')

        if not request.POST.get('password'):
            errors.append('密码不能为空')
        else:
            password = request.POST.get('password')
        if not request.POST.get('email'):
            errors.append('邮箱不能为空')
        else:
            email = request.POST.get('email')

        if account is not None and password is not None and email is not None:
            user = User.objects.create_user(account, email, password)
            user.save()
            return render(request, 'login.html')
    return render(request, 'signup.html', {'errors': errors})


"""""""""""""""""""""""""""""""""""""""""""""""""""
# 登陆成功，读取账号主页面信息
"""""""""""""""""""""""""""""""""""""""""""""""""""


def index(request):
    # Notice：增加session功能后此处查找表中本作者的文章！
    articles = models.Article.objects.filter(author=request.session['username'])  # 数据库读取本作者文章
    #
    print(request.session['username'])
    return render(request, 'index.html',
                  {'articles': articles, 'user': request.session['username'],
                   'article_sum':articles.__len__()})
    # 'visit_sum': view_add(request, request.session['username']
    # 老版本！
    # articles = models.Article.objects.filter(author = request.user) # 数据库读取本作者文章
    # return render(request, 'index.html', {'articles': articles})


"""""""""""""""""""""""""""""""""""""""""""""""""""
# 文章详细页 pk = primary key
"""""""""""""""""""""""""""""""""""""""""""""""""""


def article_page(request, article_id):
    try:
        article = models.Article.objects.get(pk=article_id)  # 根据文章号，检索制定文章
        comment = models.Comment.objects.filter(article_part_of=article.pk)
    except ObjectDoesNotExist:
        # 未找到 跳出404
        return render_to_response('404.html', status=404)
    key_edit_id = 0
    if article.author == request.session['username']:
        key_edit_id = 1
    return render(request, 'article_page.html', {'article': article, 'comments': comment, 'user': article.author,'token':key_edit_id})

    # 原来的代码
    # render(request, 'article_page.html', {'article': article},{'comment': comment})


"""""""""""""""""""""""""""""""""""""""""""""""""""
# 文章详细页 pk = primary key
"""""""""""""""""""""""""""""""""""""""""""""""""""


def article_edit_page(request, article_id):
    # -1代表是新增博客，否则是编辑博客，编辑博客时需要传递博客对象到页面并显示
    # user_temp = request.GET.get('user_temp')
    # print("user_temp:" + user_temp)
    if str(article_id) == '0':
        return render(request, 'article_edit_page.html', {'user': request.session['username']})
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'article_edit_page.html', {'article': article, 'user': request.session['username']})


"""""""""""""""""""""""""""""""""""""""""""""""""""
# 文章详细页操作 pk = primary key
"""""""""""""""""""""""""""""""""""""""""""""""""""


def article_edit_page_action(request):
    title = request.POST.get('title', '默认标题')  ##get是根据参数名称从form表单页获取内容
    content = request.POST.get('desc', '默认内容')
    author = request.POST.get('user_hidden', '默认内容')
    article_id = request.POST.get('article_id_hidden', 'ar')
    user = request.session['username']
    last_edit = datetime.datetime.now()
    ##保存数据

    ##如果是0，标记新增，使用create方法，否则使用save方法
    if str(article_id) == '0':
        models.Article.objects.create(title=title, author=author, content=content, last_edit=last_edit)

        ##数据保存完成，返回首页
        articles = models.Article.objects.filter(author=user)
        ##新增是返回首页
        return render(request, 'index.html', {'articles': articles, 'user': user})

    article = models.Article.objects.get(pk=article_id)
    article.title = title
    article.content = content
    article.author = author
    article.save()
    # 编辑是返回详情页
    return render(request, 'article_page.html', {'article': article, 'user': request.session['username']})


"""""""""""""""""""""""""""""""""""""""""""""""""""
# 删除本文
"""""""""""""""""""""""""""""""""""""""""""""""""""


def article_delete(request, article_id):
    article = models.Article.objects.filter(pk=article_id)
    article.delete()
    return HttpResponseRedirect('/blog/index')


"""""""""""""""""""""""""""""""""""""""""""""""""""
# 新建评论
"""""""""""""""""""""""""""""""""""""""""""""""""""


def comment_create(request):
    # user = request.POST.get('user_hidden', '游客')  ##get是根据参数名称从form表单页获取内容
    user = request.session['username']
    comment = request.POST.get('comment', '默认内容')
    article_id = request.POST.get('article_part_of_hidden', 'ar')
    create_time = datetime.datetime.now()
    ##保存数据
    ##如果是0，标记新增，使用create方法，否则使用save方法
    models.Comment.objects.create(comment_user=user, content=comment, creation_time=create_time,
                                  article_part_of=article_id)
    ##新增是返回首页
    temp = models.Article.objects.get(pk=article_id)
    temp.com_sum = temp.com_sum + 1
    temp.save()
    return article_page(request, article_id)


"""""""""""""""""""""""""""""""""""""""""""""""""""
# 删除评论
"""""""""""""""""""""""""""""""""""""""""""""""""""


def comment_delete(request, comment_id):
    comments = models.Comment.objects.filter(pk=comment_id)  # 获取评论
    article_id = -1  # 初始化文章id标记
    for comment in comments:
        article_id = comment.article_part_of
        comment.delete()
        temp = models.Article.objects.get(pk=article_id)
        temp.com_sum = temp.com_sum - 1
        temp.save()
    return article_page(request, article_id)


def find_page(request):
    return


def page_not_found(request):
    return render_to_response('404.html')


"""""""""""""""""""""""""""""""""""""""""""""""""""
# 增加访问
"""""""""""""""""""""""""""""""""""""""""""""""""""


# request.session['username']
def view_add(request,name):
    visit = models.User.objects.get(username=name)
    visit = visit.view + 1
    visit_show = visit
    visit.save()
    return visit_show


"""""""""""""""""""""""""""""""""""""""""""""""""""
# 增加文章
"""""""""""""""""""""""""""""""""""""""""""""""""""


def art_add():
    return


"""""""""""""""""""""""""""""""""""""""""""""""""""
# 减少文章
"""""""""""""""""""""""""""""""""""""""""""""""""""


def art_dec():
    return
