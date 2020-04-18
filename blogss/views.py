from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.contenttypes.models import  ContentType

# Create your views here.
from blogss.models import Blog, BlogType
from django.conf import settings

from comments.models import Comment
from read_stastic.utils import read_statistic_one_read

from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from read_stastic.models import ReadNum


def get_blog_common(request, blog_all_list):
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_NUMBER)
    page_num = request.GET.get('page', 1)  # 返回一个字典,默认值是1
    print(page_num)
    page_of_blogs = paginator.get_page(page_num)  # 返回对应页的博客
    current_page_num = page_of_blogs.number  # 获取当前页
    print(current_page_num)
    # 列表生成器，生成指定范围的页号，往前两页，往后两页，不能超过范围
    page_range = [x for x in range(current_page_num - 2, current_page_num + 3) if
                  (x > 0 and x < paginator.num_pages + 1)]
    if page_range[0] - 1 >= 2:  # 中间用省略号表示
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    if page_range[0] != 1:  # 增加首页和尾页
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    print(blog_dates_dict)
    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = get_blog_common(request, blog_all_list)
    return render(request,'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key=read_statistic_one_read(request,blog)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    data={}

    response = render(request,'blog/blog_detail.html', context)
    response.set_cookie(read_cookie_key,'true')  # 关闭浏览器，cookie才无效
    return response


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_common(request, blog_all_list)
    context['blog_type']=blog_type
    return render(request,'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blog_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_common(request, blog_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request,'blog/blogs_with_date.html', context)
