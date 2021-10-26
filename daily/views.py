# -*- coding:utf-8 -*-

from django.utils import timezone
from django.shortcuts import HttpResponse, render
from .models import iCourse, Pushup

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the daily exercise index.")


def receive_data(request):
    import json
    post_data = request.body
    post_data = json.loads(post_data)

    today = timezone.now().strftime('%Y%m%d')
    course_data = post_data['result']
    pushup_data = post_data['pushup']
    data_str = ','.join(map(str, course_data))

    course_filter = iCourse.objects.filter(today=today)
    pushup_filter = Pushup.objects.filter(today=today)
    course_cnt = course_filter.count()
    pushup_cnt = pushup_filter.count()
    if course_cnt > 0:
        course_filter.update(**{'today': today, 'watched': data_str})
    else:
        i = iCourse(today=today, watched=data_str)
        i.save()

    if pushup_cnt > 0:
        pushup_filter.update(**{'today': today, 'finish_num': pushup_data})
    else:
        p = Pushup(today=today, finish_num=pushup_data)
        p.save()
    
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
