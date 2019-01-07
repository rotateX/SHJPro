# coding=utf-8

from django.shortcuts import render, redirect, reverse, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from SHJ.models import Content, Tag, Category, Comment
from SHJ.forms import CommentForm
import markdown
from django.http import JsonResponse
from apscheduler.scheduler import Scheduler
from SHJPro import settings
import logging
from django.utils.timezone import now, timedelta
from SiteView.Viewchange import change_info

# Create your views here.

categories = Category.objects.all().order_by('created_time')
contents = Content.objects.all()
# category_list = []

# 统计每个分类下文章数量
# for i in range(1, 6):
#     category_list.append(contents.filter(category_id=i).count())

# 统计近7天评论数量
# today = now().date()
# for d in range(0, 7):
#     today = now().date()
#     for d in range(0, 7):
#         day = today - timedelta(days=d)
#         day_comment = Comment.objects.filter(
#             created_time__year=day.year,
#             created_time__month=day.month,
#             created_time__day=day.day,
#         ).count()
#         commentnum_list.insert(-d, day_comment)
#         day_list.insert(-d, str(day))


# 日志对象logger
logger = logging.getLogger('up_comment')


# base test
def base(request):

    return render(request, 'base.html', {
        'category': categories
    })


# 首页 index.html
def home(request):
    change_info(request) # 调用访问统计
    return render(request, 'index.html', {
        'category': categories
    })


# 按类别归档 category.html
def category(request, id):

    contents = Content.objects.filter(category_id=str(id))
    p_content = Paginator(contents, settings.PAGE_NUM)
    page = request.GET.get('page')
    try:
        content_list = p_content.page(page)
    except PageNotAnInteger:
        content_list = p_content.page(1)
    except EmptyPage:
        content_list = p_content.page(p_content.num_pages)
    return render(request, 'category.html', {
        'category': categories,
        'content': contents,
        'content_list': content_list,
        'p_content': p_content,
        'category_id': id,
    })


# 详情页面 post.html
def post(request, id):

    post_form = CommentForm()
    # comments = Comment.objects.filter(content_id=str(id), active=True)  # 用content_id获取评论, 并且active为True的评论
    comments = Comment.objects.filter(content_id=str(id)).order_by('-update_time')
    top10 = contents.order_by('-views')[:10]
    comment_num = Comment.objects.filter(content_id=str(id)).count()
    details = Content.objects.get(id=str(id))  # 用id获取Content实例
    tags = Content.objects.get(id=str(id)).tag.all()
    if len(tags) < 1:
        tags = ['暂无标签']
    details.up_view()  # 更新打开次数
    next_article = details.next_article()  # 调用方法，获取下一篇
    pre_article = details.pre_article()   # 调用方法，获取上一篇
    # markdown文章content字段
    details.content = markdown.markdown(
        details.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    return render(request, 'post-ajax.html', {
        'category': categories,
        'details': details,
        'next_article': next_article,
        'pre_article': pre_article,
        'comments': comments,
        'comment_num': comment_num,
        'top10': top10,
        'comment_form': post_form,
        'tags': tags,
    })


# 更新评论
def get_comments(request, id):

    res = {}  # 初始化res，用于返回数据
    if request.method == 'POST':
        post_form = CommentForm(request.POST)
        if post_form.is_valid():
            # 填写合法，创建评论实例，保存评论信息
            comment = Comment()
            comment.name = post_form.cleaned_data['name']
            comment.email = post_form.cleaned_data['email']
            comment.body = post_form.cleaned_data['body']
            comment.content_id = id
            comment.save()
            # 填写合法，返回数据，
            content = Content.objects.get(id=str(id))
            content.up_comment()  # 加了定时器 这边可以不用执行
            comment_num = Comment.objects.filter(content_id=str(id)).count()  # 查询当前文章评论数量
            res['status'] = 'SUCCESS'
            res['name'] = comment.name
            res['email'] = comment.email
            res['body'] = comment.body
            res['update_time'] = comment.update_time.strftime('%Y-%m-%d %H:%M:%S')
            res['comment_num'] = comment_num
        else:
            # 填写错误时，返回错误信息
            res['status'] = 'ERROR'
            res['message'] = list(post_form.errors.values())
        return JsonResponse(res)
    return HttpResponseRedirect(reverse('home'))


# ECharts
def date_echarts(request):

    return render(request, 'echarts.html')


# ECharts 异步请求
def get_data(request):
    category_list = []
    commentnum_list = []
    day_list = []
    today = now().date()
    for d in range(0, 7):
        day = today - timedelta(days=d)
        day_comment = Comment.objects.filter(
            created_time__year=day.year,
            created_time__month=day.month,
            created_time__day=day.day,
        ).count()
        commentnum_list.insert(-d, day_comment)
        day_list.insert(-d, str(day))
    for i in range(1, 6):
        category_list.append(contents.filter(category_id=i).count())
    if request.method == 'GET' and request.GET.get('data') == '1':
        data = {
            'categorydata': [
                {'value': category_list[0], 'name': categories[0].name},
                {'value': category_list[1], 'name': categories[1].name},
                {'value': category_list[2], 'name': categories[2].name},
                {'value': category_list[3], 'name': categories[3].name},
                {'value': category_list[4], 'name': categories[4].name},
            ],
            # 'categories': ["神话志","异兽录","怪谈论","奇人异事","金石志"],
            'commentnum_list': commentnum_list,
            'day_list': day_list,
        }
        print(category_list)
        return JsonResponse(data)
    return render(request, 'echarts.html')


# 评论翻页
def comment_page():
    pass


# 定义错误页面
def page_not_found(request):

    return render(request, '404.html')


# 定时任务
def tsk_up_comment():
    contents = Content.objects.all()
    # print('开始更新任务')
    # 遍历文章，计算每篇文章的评论数量，并更新
    logger.info('开始更新评论')  # 写入日志
    for i in contents:
        comments = Comment.objects.filter(content_id=i.id).count()
        Content.objects.filter(id=i.id).update(comment_num=comments)
    logger.info('更新评论结束')  # 写入日志


scheuler = Scheduler()


@scheuler.interval_schedule(seconds=settings.UP_COMMENT_NUM)
def tsk():

    # 执行更新任务 每30s
    # tsk_up_comment()
    pass


scheuler.start()
