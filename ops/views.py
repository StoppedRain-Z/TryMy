from django.shortcuts import render, redirect, reverse
from django.views import View
from .models import *
from django.http import HttpResponse
import json
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.core.mail import send_mail
# Create your views here.


def index(requests):
    return render(requests,'index.html')


def student_center(requests):
    return render(requests, 'student_center')


def teacher_center(requests):
    return render(requests, 'teacher_center')


def assistant_center(requests):
    return render(requests, 'assistant_center')


class S_Choice(View):

    @staticmethod
    def get(request):
        teacher_list = Teacher.objects.all()
        json_list = []
        for teacher in teacher_list:
            json_item = {"teacher_name": teacher.user.name,
                         "teacher_institute": teacher.institute,
                         "teacher_info": teacher.teacher_info,
                         "teacher_id": teacher.user.username}

            json_list.append(json_item)
        print(json_list)
        return HttpResponse(json.dumps(json_list))

    @staticmethod
    def post(request):
        data = request.POST
        teacher_id = data.get('teacher_id')
        user = request.user
        student = Student.objects.get(user=user)
        teacher = User.objects.get(username=teacher_id).teacher
        count = teacher.student_set.all().count()
        if count < teacher.max_student:
            Choose.objects.create(student=student, teacher=teacher, teacher_choice=1, student_choice=2)
            return HttpResponse('ok')
        else:
            return HttpResponse('max')


class T_Choice(View):
    @staticmethod
    def get(request):
        print("lalala")
        teacher = request.user.teacher
        choose_list = Choose.objects.filter(teacher=teacher, student_choice=2, teacher_choice=1)
        json_list = []
        for choose in choose_list:
            json_item = {"student_id": choose.student.user.username, "name": choose.student.user.name}
            json_list.append(json_item)
        print(json_list)
        return HttpResponse(json.dumps(json_list))

    @staticmethod
    def post(request):
        data = request.POST
        print(data)
        student_id = data.get('student_id')
        choice = data.get('choice')
        teacher = request.user.teacher
        count = teacher.student_set.all().count()
        student = User.objects.get(username=student_id).student
        choose = Choose.objects.get(student=student, teacher=teacher)
        if student.teacher is None:    # 该学生未选择导师
            if count < teacher.max_student:   # 该老师还有名额
                choose.teacher_choice = choice
                choose.save()
                if choice == 2:
                    student.teacher = teacher
                    student.save()
                return HttpResponse('ok')
            else:
                choose.teacher_choice = 3
                choose.save()
                return HttpResponse('max')
        else:
            return HttpResponse('student has teacher')


def confirm_list_s(request):
    user = request.user
    student = Student.objects.get(user=user)
    choose_list = Choose.objects.filter(student=student, student_choice=2)
    json_list = []
    for choose in choose_list:
        teacher_choice = choose.teacher_choice
        choice = ''
        if teacher_choice == 1:
            choice = '未确认'
        elif teacher_choice == 2:
            choice = '同意'
        elif teacher_choice == 3:
            choice = '拒绝'
        json_item = {"name": choose.teacher.user.name, "teacher_id": choose.teacher.user.username,
                     "teacher_choice": choice, "teacher_info": choose.teacher.teacher_info}
        json_list.append(json_item)
    return HttpResponse(json.dumps(json_list))


def confirm_list_t(request):
    teacher = request.user.teacher
    choose_list = Choose.objects.filter(teacher=teacher).exclude(teacher_choice=1)
    json_list = []
    for choose in choose_list:
        teacher_choice = choose.teacher_choice
        choice = ''
        if teacher_choice == 2:
            choice = '同意'
        elif teacher_choice == 3:
            choice = '拒绝'
        json_item = {"name": choose.student.user.name, "cardID": choose.student.user.username, "choice": choice}
        json_list.append(json_item)
    return HttpResponse(json.dumps(json_list))

'''
def op_t(request):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    card_id = request.POST.get['cardID']
    teacher_choice = request.POST.get['teacher_choice']
    usr = User.objects.get(username=card_id)
    student = Student.objects.get(user=usr)
    choose = Choose.objects.get(teacher=teacher, student=student)
    choose.teacher_choice = teacher_choice
    choose.save()
    if choose.teacher_choice == 2 and choose.student_choice == 2:
        student.teacher = teacher
        student.save()
    return HttpResponse("ok")


def op_s(request, student_choice):
    user = request.user
    student = Student.objects.get(user=user)
    card_id = request.POST.get['cardID']
    usr = User.objects.get(username=card_id)
    teacher = Teacher.objects.get(user=usr)
    choose = Choose.objects.get(teacher=teacher, student=student)
    choose.student_choice = student_choice
    choose.save()
    if choose.student_choice == 2 and choose.teacher_choice == 2:
        student.teacher = teacher
        student.save()
    return HttpResponse("ok")
'''


def create_progress(request):
    data = request.POST
    title = data.get['title']
    desc = data.get['desc']
    start_time = data.get['start_time']
    end_time = data.get['end_time']
    student_list = Student.objects.all()
    length = Progress.objects.all().count()
    response = {}
    email_list = []
    for student in student_list:
        try:
            teacher = student.teacher
            progress = Progress.objects.create(unique_id=length, student=student, teacher=teacher, title=title, desc=desc)
            email_list.append(student.user.email)
            length = length + 1
        except Exception as e:
            print(e)
            response['msg'] = str(e)
            return HttpResponse(response)
    print('send email start')
    # send_mail(title, desc, 'zhangrt20@126.com', email_list, fail_silently=False)
    print('send email end')


def s_progress_list_unfinished(request):
    user = request.user
    student = Student.objects.find(user=user)
    response = {}
    if student is None:
        response['msg'] = 'user does not found'
        return HttpResponse(response)
    # time_now = timezone.now()
    now = datetime.now()
    progress_list = Progress.objects.filter(student=student, student_ok=False, start_time__lt=now, end_time__gt=now)
    res = []
    for progress in progress_list:
        json_item = {'id': progress.unique_id, 'title': progress.title, 'start_time': progress.start_time, 'end_time': progress.end_time}
        res.append(json_item)
    return HttpResponse(json.dumps(res))


def s_progress_list_finished(request):
    user = request.user
    student = Student.objects.find(user=user)
    response = {}
    if student is None:
        response['msg'] = 'user does not found'
        return HttpResponse(response)
    # time_now = timezone.now()
    now = datetime.now()
    progress_list = Progress.objects.filter(student=student, student_ok=True, teacher_ok=False)
    res = []
    for progress in progress_list:
        json_item = {'id': progress.unique_id, 'title': progress.title,
                     'end_time': progress.end_time, 'status': '导师未回复'}
        res.append(json_item)
    progress_list = Progress.objects.filter(student=student, student_ok=True, teacher_ok=True)
    for progress in progress_list:
        json_item = {'id': progress.unique_id, 'title': progress.title,
                     'end_time': progress.end_time, 'status': '已完成'}
        res.append(json_item)
    now = datetime.now()
    progress_list = Progress.objects.filter(student=student, student_ok=False, end_time__lt=now)
    for progress in progress_list:
        json_item = {'id': progress.unique_id, 'title': progress.title,
                     'end_time': progress.end_time, 'status': '已失效'}
        res.append(json_item)
    return HttpResponse(json.dumps(res))


class S_Progress_Detail(View):
    @staticmethod
    def get(request):
        id = request.GET.get['id']
        user = request.user
        try:
            student = Student.objects.get(user=user)
            progress = Progress.objects.get(unique_id=id,student=student)
            response = {'title': progress.title, 'desc': progress.desc, 'start_time': progress.start_time,
                        'end_time': progress.end_time, 'student_text': progress.student_text,
                        'teacher_text': progress.teacher_text}
            return HttpResponse(json.dumps(response))
        except Exception as e:
            response = {'msg': str(e)}
            return HttpResponse(response)

    @staticmethod
    def post(request):
        data = request.POST
        student_text = data.get['student_text']
        id = data.get['id']
        user = request.user
        try:
            student = Student.objects.get(user=user)
            progress = Progress.objects.get(unique_id=id, student=student)
            progress.student_text = student_text
            progress.student_ok = True
            progress.save()
            response = {'msg': 'ok'}
            return HttpResponse(response)
        except Exception as e:
            response = {'msg': str(e)}
            return HttpResponse(response)


class T_Progress_Detail(View):
    @staticmethod
    def get(request):
        id = request.GET.get['id']
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
            progress = Progress.objects.get(unique_id=id, teacher=teacher)
            response = {'title': progress.title, 'desc': progress.desc, 'start_time': progress.start_time,
                        'end_time': progress.end_time, 'student_text': progress.student_text,
                        'teacher_text': progress.teacher_text}
            return HttpResponse(json.dumps(response))
        except Exception as e:
            response = {'msg': str(e)}
            return HttpResponse(response)

    @staticmethod
    def post(request):
        data = request.POST
        teacher_text = data.get['teacher_text']
        id = data.get['id']
        user = request.user
        try:
            teacher = Teacher.objects.get(user=user)
            progress = Progress.objects.get(unique_id=id, teacher=teacher)
            progress.teacher = teacher_text
            progress.teacher_ok = True
            progress.save()
            response = {'msg': 'ok'}
            return HttpResponse(response)
        except Exception as e:
            response = {'msg': str(e)}
            return HttpResponse(response)


def t_progress_list_unfinished(request):
    user = request.user
    teacher = Teacher.objects.find(user=user)
    response = {}
    if teacher is None:
        response['msg'] = 'user does not found'
        return HttpResponse(response)
    # time_now = timezone.now()
    now = datetime.now()
    progress_list = Progress.objects.filter(teacher=teacher, student_ok=True, teacher_ok=False,
                                            start_time__lt=now, end_time__gt=now)
    res = []
    for progress in progress_list:
        json_item = {'id': progress.unique_id, 'title': progress.title, 'start_time': progress.start_time,
                     'end_time': progress.end_time, 'msg': '未回执'}
        res.append(json_item)
    progress_list = Progress.objects.filter(teacher=teacher, student_ok=False, teacher_ok=False,
                                            start_time__lt=now, end_time__gt=now)
    for progress in progress_list:
        json_item = {'id': progress.unique_id, 'title': progress.title, 'start_time': progress.start_time,
                     'end_time': progress.end_time, 'msg': '学生未回复'}
        res.append(json_item)
    return HttpResponse(json.dumps(res))


def t_progress_list_finished(request):
    user = request.user
    teacher = Teacher.objects.find(user=user)
    response = {}
    if teacher is None:
        response['msg'] = 'user does not found'
        return HttpResponse(response)
    # time_now = timezone.now()
    now = datetime.now()
    progress_list = Progress.objects.filter(teacher=teacher, student_ok=True, teacher_ok=True)
    res = []
    for progress in progress_list:
        json_item = {'id': progress.unique_id, 'title': progress.title, 'start_time': progress.start_time,
                     'end_time': progress.end_time, 'msg': '已完成'}
        res.append(json_item)
    progress_list = Progress.objects.filter(Q(student_ok=False) | Q(teacher_ok=False),teacher=teacher,
                                            end_time__lt=now)
    for progress in progress_list:
        json_item = {'id': progress.unique_id, 'title': progress.title, 'start_time': progress.start_time,
                     'end_time': progress.end_time, 'msg': '已过期'}
        res.append(json_item)
    return HttpResponse(json.dumps(res))


def a_progress_list_finished(request):
    teacher_list = Teacher.objects.all()
    response = {}
    now = datetime.now()
    res = []
    for teacher in teacher_list:
        progress_list = Progress.objects.filter(teacher=teacher, student_ok=True, teacher_ok=True)
        for progress in progress_list:
            json_item = {'id': progress.unique_id, 'title': progress.title, 'start_time': progress.start_time,
                         'end_time': progress.end_time, 'msg': '已完成'}
            res.append(json_item)
        progress_list = Progress.objects.filter(Q(student_ok=False) | Q(teacher_ok=False), teacher=teacher,
                                                end_time__lt=now)
        for progress in progress_list:
            json_item = {'id': progress.unique_id, 'title': progress.title, 'start_time': progress.start_time,
                         'end_time': progress.end_time, 'msg': '已过期'}
            res.append(json_item)
    res.sort(key=lambda k: k['start_time'], reverse=True)
    print(res)
    return HttpResponse(json.dumps(res))


def a_progress_list_unfinished(request):
    teacher_list = Teacher.objects.all()
    now = datetime.now()
    res = []
    for teacher in teacher_list:
        progress_list = Progress.objects.filter(Q(teacher_ok=False) | Q(student_ok=False), teacher=teacher,
                                                start_time__lt=now, end_time__gt=now)
        for progress in progress_list:
            json_item = {'id': progress.unique_id, 'title': progress.title, 'start_time': progress.start_time,
                         'end_time': progress.end_time, 'msg': '未完成'}
            res.append(json_item)
    res.sort(key=lambda k: k['start_time'], reverse=True)
    print(res)
    return HttpResponse(json.dumps(res))


def progress_detail(request):
    id = request.GET.get['id']
    try:
        progress = Progress.objects.get(unique_id=id)
        response = {'msg': 'ok', 'title': progress.title, 'desc': progress.desc,
                    'student_name': progress.student.user.name, 'student_text': progress.student_text,
                    'teacher_name': progress.teacher.user.name, 'teacher_text': progress.teacher_text}
        return HttpResponse(response)
    except Exception as e:
        response = {'msg': str(e)}
        return HttpResponse(response)
















