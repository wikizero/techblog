# coding:utf-8
from django.shortcuts import render, HttpResponse, redirect, render_to_response
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from blog.models import *
from django.db.models import Q
import pdfkit
import random
import datetime
import json
import os
import time
import mimetypes


def index(request):
    notes = Notes.objects.filter(show=True).order_by('-id')
    data = {
        'notes': notes[:9]
    }
    return render(request, 'index.html', data)


def about_us(request):
    return render(request, 'about.html')


def full_page(request):
    return render(request, 'fullpage.html')


def notes_logout(request):
    logout(request)
    return redirect('/')


@login_required(login_url="/notes/login")
def notes(request):
    notes = Notes.objects.all()
    dct = {}
    for note in notes:
        if not dct.get(note.type, False):
            dct[note.type] = []
        lst = dct.get(note.type)
        lst.append(note)
    data = {
        'notes': dct
    }
    return render(request, 'notes.html', data)


@csrf_exempt
def notes_login(request):
    if request.method == "GET":
        return render(request, 'notes-login.html')
    elif request.method == "POST":
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if not username or not password:
            return HttpResponse('username or password can not be none')
        user = authenticate(username=username, password=password)
        if not user:
            return HttpResponse('error')
        login(request, user)
        return redirect('/notes')


def notes_share(request):
    if request.method == 'GET':
        type = request.GET.get('type', False)
        notes = Notes.objects.filter(show=True).order_by('-id')
        if type:
            all_note = Notes.objects.filter(show=True, type=type).order_by('-id')
        else:
            all_note = notes
        dct = {}
        for note in notes:
            if not dct.get(note.type, False):
                dct[note.type] = []
            lst = dct.get(note.type)
            lst.append(note)

        data = {
            'notes': all_note,
            'dct': dct
        }
    elif request.method == 'POST':
        print 'to do'
    return render(request, 'notes-share.html', data)


def notes_details(request):
    id = request.GET.get('id', False)
    if not id:
        return HttpResponse('data err')
    note = Notes.objects.get(id=id)
    data = {
        'note': note
    }
    return render(request, 'notes-details.html', data)


def file_download(request):
    response = HttpResponse(content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="java.png"'
    with open('static/blog/images/java.png') as fp:
        data = fp.read()
        response.write(data)

    return response


def sign_sys(request):
    task_list = Task.objects.filter(future=False)
    daily_list = History.objects.filter().order_by('-id')
    data = {
        'task_list': task_list,
        'daily_list': daily_list
    }

    if request.method == 'GET':
        return render(request, 'sign-in.html', data)
    elif request.method == 'POST':
        task_id = request.POST.getlist('checkbox', False)
        text = request.POST.get('textarea', '')

        if not task_id:
            return HttpResponse('天! 什么都没做，干嘛去了？')

        task_id = [int(float(x)) for x in task_id]
        ids = [t.id for t in task_list]
        not_task_id = []
        for i in ids:
            if i not in task_id:
                not_task_id.append(i)

        # status算法
        status = ''
        if len(task_id) >= len(not_task_id) + 1:
            status = 'high'
        elif len(task_id) + 1 <= len(not_task_id):
            status = 'low'
        else:
            status = 'middle'

        daily = History.objects.create(more=text, status=status)
        for i in task_id:
            task = Task.objects.get(id=i)
            Old.objects.create(
                daily=daily,
                task=task,
                done=True
            )
        for i in not_task_id:
            task = Task.objects.get(id=i)
            Old.objects.create(
                daily=daily,
                task=task,
                done=False
            )
        return redirect('/sign/in')


@csrf_exempt
def add_note(request):
    if request.method == 'POST':
        new_type = request.POST.get('new-type', False)
        if new_type:
            note = Notes.objects.create(type=new_type,
                                        title='wiki notes',
                                        content='<p><span style="color: rgb(32, 147, 97);">welcome to apply Wiki notes...</span><br></p>')
        else:
            type = request.POST.get('type', False)
            title = request.POST.get('value', False)
            if not type or not title:
                return HttpResponse('data error')
            note = Notes.objects.create(type=type, title=title)
        msg = {
            'msg': 'ok',
            'id': note.id
        }
        return HttpResponse(json.dumps(msg), content_type="application/json")


@csrf_exempt
def get_note(request):
    if request.method == 'POST':
        id = request.POST.get('id', False)
        if not id:
            return HttpResponse('data error')
        note = Notes.objects.get(id=id)
        result = {
            'note': {
                'content': note.content,
                'type': note.type,
                'title': note.title,
                'desc': note.desc,
                'show': note.show
            }
        }
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def del_note(request):
    if request.method == 'POST':
        id = request.POST.get('id', False)
        if not id:
            return HttpResponse('data error')
        note = Notes.objects.get(id=id)
        note.delete()
        result = {
            'msg': 'ok'
        }
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def save_note(request):
    if request.method == 'POST':
        new_name = request.POST.get('new-name', False)
        id = request.POST.get('id', False)
        content = request.POST.get('value', False)
        desc = request.POST.get('desc', 'No description for the note...')
        if not id:
            return HttpResponse('data error')
        note = Notes.objects.get(id=id)
        if new_name:
            note.title = new_name
        else:
            note.content = content
            note.desc = desc
        note.save()
        result = {
            'msg': 'ok'
        }
        return HttpResponse(json.dumps(result), content_type="application/json")

    elif request.method == 'GET':  # get request toggle show or hide
        id = request.GET.get('id', False)
        show = request.GET.get('bol', False)
        if not id or not show:
            return HttpResponse('data err')
        note = Notes.objects.get(id=id)
        if show == 'false':
            print '-' * 100
            note.show = False
        else:
            print '+' * 100
            note.show = True
        note.save()
        result = {
            'msg': 'ok'
        }
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def upload(request):
    if request.method == 'GET':
        root_dir = 'static/blog/files/'
        file_lst = []

        for parent_folder, folder_names, file_names in os.walk(root_dir):
            for filename in file_names:
                # print filename  # 文件名
                size = os.path.getsize(root_dir+filename)
                # file_size = round(size, 1)   # 文件大小
                create_sec = os.stat(root_dir+filename).st_ctime
                dates = datetime.datetime.fromtimestamp(create_sec)
                create_date = dates.strftime('%Y-%m-%d %H:%M:%S')  # 文件创建时间（也即是文件上传时间 ）
                file_lst.append([filename, size, create_date])   # filename.decode('gbk') 转中文显示
        data = {
            'file': file_lst[::-1],
            'imtype': ['png', 'PNG', 'jpg', 'JPG','gif', 'GIF', 'peg', 'PEG'],
            'mvtype': ['mp4', 'MP4']
        }
        return render(request, 'upload.html', data)

    elif request.method == 'POST':
        file_obj = request.FILES.getlist('files[]')
        file_list = []
        for f in file_obj:
            if len(f) / 1024 > 1000000000:   # 不大于10M
                result = {
                    'msg': 'err'
                }
                return HttpResponse(json.dumps(result), content_type="application/json")
        destination = 'static/blog/files/'
        if not os.path.exists(destination):
            os.makedirs(destination)
        with open(destination + f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        file_list.append(f.name)

        result = {
            'filename': ','.join(file_list),
            'msg': 'ok'
        }
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def download(request):
    name = request.GET.get('file', False)
    root_dir = 'static/blog/files/'

    # with open(root_dir+name) as f:
    #     res = f.read()
    # response = StreamingHttpResponse(res)
    # response['Content-Type'] = 'application/octet-stream'
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name)

    # response = HttpResponse(content_type=mimetypes.guess_type(root_dir+name))
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name)
    # with open(root_dir+name) as fp:
    #     data = fp.read()
    #     response.write(data)

    def readFile(fn, buf_size=262144):
        f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()

    file_name = root_dir+name
    response = HttpResponse(readFile(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name.encode('gbk'))

    return response


@csrf_exempt
def remove(request):
    name = request.GET.get('file', False)
    root_dir = 'static/blog/files/'
    os.remove(root_dir+name)
    return redirect('/upload')
