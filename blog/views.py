# coding:utf-8
from django.shortcuts import render, HttpResponse, redirect
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from blog.models import *
import pdfkit
import random
import datetime
import json


def index(request):
    return render(request, 'index.html')


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

    notes = Notes.objects.filter(show=True).order_by('-id')
    dct = {}
    for note in notes:
        if not dct.get(note.type, False):
            dct[note.type] = []
        lst = dct.get(note.type)
        lst.append(note)

    data = {
        'notes': notes,
        'dct': dct
    }
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
        print data, '---' * 100

    return response


def export(request):
    # order_num_list = request.GET.get('id', '')
    options = {'margin-top': '0', 'margin-right': '0', 'margin-bottom': '0', 'margin-left': '0'}
    output = '/tmp/out.pdf-%d' % random.randint(1000, 9999)
    pdfkit.from_url('http://localhost:8022/index', output, options=options)
    response = HttpResponse(content_type='application/pdf')

    now = datetime.datetime.now()
    pdf_name = now.strftime('%Y%m%d%H%M%S')
    response['Content-Disposition'] = 'attachment; filename="' + pdf_name + '.pdf"'

    with file(output) as fp:
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
