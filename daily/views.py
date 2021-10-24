from django.shortcuts import HttpResponse, render

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the daily exercise index.")


def receive_data(request):
    import json
    post_data = request.body
    post_data = json.loads(post_data)
    print(post_data)

    return HttpResponse(json.dumps(post_data))


def show_html(request):
    return render(request, 'daily/index.html')


def post_test(request):
    print(request.POST)

    return HttpResponse('')
