# -*- coding:utf-8 -*-

from django.utils import timezone
from django.shortcuts import HttpResponse, render
from .models import iCourse

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the daily exercise index.")


def receive_data(request):
    import json
    post_data = request.body
    post_data = json.loads(post_data)
    print(post_data)

    today = timezone.now().strftime('%Y%m%d')
    course_data = post_data['result']
    data_str = ','.join(map(str, course_data))

    filter_result = iCourse.objects.filter(today=today)
    n = filter_result.count()
    if n > 0:
        filter_result.update(**{'today': today, 'watched': data_str})
    else:
        i = iCourse(today=today, watched=data_str)
        i.save()
    
    return HttpResponse(json.dumps(post_data))


def get_data(request):
    """从数据库中取数据返回"""
    watched = iCourse.objects.all()
    watched = watched.order_by('-today')[0]
    return HttpResponse(watched)


def show_html(request):
    return render(request, 'daily/index.html')


def post_test(request):
    print(request.POST)

    return HttpResponse('hello, world')
