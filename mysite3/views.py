from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from read_stastic.utils import get_seven_days_read_data, get_today_hot_data
from read_stastic.utils import get_yesterday_hot_data

from blogss.models import Blog
from django.db.models import Sum, Q
from django.utils import timezone
import datetime
from django.core.cache import cache


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
        .filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[0:5]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    #yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 60 * 60)
    blog_on_top = Blog.objects.filter(top=True)
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = today_hot_data

    #context['yesterday_hot_data'] = yesterday_hot_data
    context['hot_blogs_for_7_days'] = get_7_days_hot_blogs()
    context['blog_on_top'] = blog_on_top
    return render(request, 'home.html', context)


def search(request):
    search_word = request.GET.get('wd', '').strip(' ')
    condition = None
    for word in search_word.split(' '):
        if condition is None:
            condition = Q(title__icontains=word)
        else:
            condition = condition | Q(title__icontains=word)
    search_blogs = []
    if condition is not None:
        search_blogs = Blog.objects.filter(condition)
    paginator = Paginator(search_blogs, 20)
    page_num = request.GET.get('page', 1)  # 返回一个字典,默认值是1
    page_of_blogs = paginator.get_page(page_num)  # 返回对应页的博客
    context = {}
    context['search_word'] = search_word
    context['page_of_blogs'] = page_of_blogs
    context['search_blogs_count'] = search_blogs.count()
    return render(request, 'search.html', context)
