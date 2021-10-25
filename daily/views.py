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

    return HttpResponse(json.dumps(post_data))


def get_data(request):
    """从数据库中取数据返回"""
    watched = iCourse.objects.all()
    return HttpResponse(watched)


def show_html(request):
    return render(request, 'daily/index.html')


def post_test(request):
    print(request.POST)

    return HttpResponse('hello, world')
