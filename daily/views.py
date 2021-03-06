# -*- coding:utf-8 -*-

import os
from django.utils import timezone
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from django.conf import settings
from .models import iCourse, Pushup

# Create your views here.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exercise.settings")

def index(request):
    return HttpResponse("Hello, world. You're at the daily exercise index.")


def receive_data(request):
    import json
    post_data = request.body
    post_data = json.loads(post_data)

    today = timezone.now().strftime('%Y%m%d')
    course_name = post_data['courseName']
    course_data = post_data['watched']
    pushup_data = post_data['pushup']
    data_str = ','.join(map(str, course_data))

    course_name2 = post_data['courseName2']
    course_data2 = post_data['watched2']
    data_str2 = ','.join(map(str, course_data2))

    update_course(course_name, today, data_str)
    update_course(course_name2, today, data_str2)

    pushup_filter = Pushup.objects.filter(today=today)
    pushup_cnt = pushup_filter.count()
    if pushup_cnt > 0:
        pushup_filter.update(**{'today': today, 'finish_num': pushup_data})
    else:
        p = Pushup(today=today, finish_num=pushup_data)
        p.save()
    
    return HttpResponse(json.dumps(post_data))


def update_course(cname, today, data_str):
    course_filter = iCourse.objects.filter(name=cname)
    pushup_filter = Pushup.objects.filter(today=today)
    course_cnt = course_filter.count()
    if course_cnt > 0:
        course_filter.update(**{'today': today, 'watched': data_str, 'name': cname})
    else:
        i = iCourse(today=today, watched=data_str, name=cname)
        i.save()  


def get_data(request):
    """从数据库中取数据返回"""

    import json
    post_data = request.body
    post_data = json.loads(post_data)

    cname1 = post_data['courseName']
    cname2 = post_data['courseName2']

    ret = dict()
    watched = iCourse.objects.all()
    course = map(get_watched_data, [cname1, cname2])
    pushup = Pushup.objects.all()
    pushup = pushup.order_by('today')

    ret['course'] = dict()
    for c in course:
        ret['course'][c.name] = {
                'today': c.today,
                'watched': c.watched,
        }
    ret['pushup'] = []
    limit = 30
    count = len(pushup)
    if count > limit:
        start_index = count - limit
    else:
        start_index = 0
    for p in pushup[start_index:]:
        ret['pushup'].append({'date': p.today, 'num': p.finish_num})
    return JsonResponse(ret)


def get_watched_data(cname):
    return iCourse.objects.filter(name=cname).order_by('-today')[0]


def post_test(request):
    print(request.POST)

    return HttpResponse('hello, world')


def merge_pdf(file_list, out_file):
    from PyPDF2 import PdfFileWriter, PdfFileReader
    pdf_writer = PdfFileWriter()
    for in_file in file_list:
        pdf_reader = PdfFileReader(open(in_file, 'rb'))
        num_pages = pdf_reader.getNumPages()
        for index in range(0, num_pages):
            page_obj = pdf_reader.getPage(index)
            pdf_writer.addPage(page_obj)
        pdf_writer.write(open(out_file, 'wb'))

    return out_file


def delete_dir(dir_path):
    """删除文件夹"""


def get_static_file(fname):
    import random
    import shutil
    import zipfile
    full_name = os.path.join(settings.BASE_DIR, 'static', 'upload', fname)
    if full_name.endswith('zip'):
        zf = zipfile.ZipFile(full_name, 'r')
        random_id = str(random.randint(10, 100))
        tmp_dir = os.path.join('/tmp', random_id)
        os.mkdir(tmp_dir)
        tmp_file_list = []
        for name in zf.namelist():
            if not name.endswith('.pdf'):
                continue
            zf.extract(name, tmp_dir)
            tmp_file_list.append(os.path.join(tmp_dir, name))
        else:
            result = merge_pdf(tmp_file_list, 
                               os.path.join(settings.BASE_DIR,
                                            'static', 
                                            'upload',
                                            'merged'+random_id+'.pdf'))
            shutil.rmtree(tmp_dir)
            return result
    else:
        return 'There is not a zip file you have uploaded!'


def upload(request):
    if request.method == 'POST':
        # 获取对象
        obj = request.FILES.get('fafafa')
        f = open(os.path.join(settings.BASE_DIR, 
                              'static', 'upload', obj.name), 
                'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()
        result = get_static_file(obj.name)
        resp = HttpResponse(open(result, 'rb'))
        resp['Content-Type'] = 'application/oct-stream'
        resp['Content-Disposition'] = 'attachment;filename='+result.split('/')[-1]
        return  resp
    return HttpResponse('failed')
