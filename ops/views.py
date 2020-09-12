from django.shortcuts import render, redirect, reverse
from django.views import View
from .models import *
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
import json
from datetime import datetime, tzinfo, timedelta, date
from django.utils import timezone
import pytz
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import operator
import os
from django.utils.encoding import escape_uri_path
# Create your views here.


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class UTC(tzinfo):
    """UTC"""
    def __init__(self,offset = 0):
        self._offset = offset

    def utcoffset(self, dt):
        return timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return timedelta(hours=self._offset)


def index(requests):
    return render(requests, 'index.html')


@login_required
def student_center(requests):
    return render(requests, 'student_center')


@login_required
def teacher_center(requests):
    return render(requests, 'teacher_center')


@login_required
def assistant_center(requests):
    return render(requests, 'assistant_center')


'''
学生志愿填报，get导师列表，post填报志愿
'''


class S_Choice(View):

    @staticmethod
    def get(request):
        teacher_list = Teacher.objects.all()
        json_list = []
        for teacher in teacher_list:
            u_count = teacher.student_set.filter(student_type='U').count()
            f_count = teacher.student_set.filter(student_type='F').count()
            json_item = {"teacher_name": teacher.user.name,
                         "teacher_institute": teacher.institute,
                         "teacher_info": teacher.teacher_info,
                         "teacher_id": teacher.user.username,
                         "student_count": str(u_count) + '/' + str(teacher.max_student),
                         "foreign_count": str(f_count) + '/' + str(teacher.max_foreign)}

            json_list.append(json_item)
        print(json_list)
        return HttpResponse(json.dumps(json_list))

    @staticmethod
    def post(request):
        data = request.POST
        teacher_id = data.get('teacher_id')
        student = request.user.student
        teacher = User.objects.get(username=teacher_id).teacher
        student_type = student.student_type
        count = 0
        max_count = 0
        if student_type == 'U':
            count = teacher.student_set.filter(student_type='U').count()
            max_count = teacher.max_student
        elif student_type == 'F':
            count = teacher.student_set.filter(student_type='F').count()
            max_count = teacher.max_foreign
        print(count)
        print(teacher.max_student)
        if count < max_count:
            choose_list = Choose.objects.filter(student=student, teacher=teacher).count()
            print(choose_list)
            if choose_list == 0:
                Choose.objects.create(student=student, teacher=teacher, teacher_choice=1, student_choice=2)
                return HttpResponse('ok')
            else:
                return HttpResponse('exists')
        else:
            return HttpResponse('max')


'''
学生个人详细信息,post提供修改
供学生自己查看
'''


class S_Detail(View):
    @staticmethod
    def get(request):
        user = request.user
        student = user.student
        if student is None:
            response = {'msg': 'user not exist'}
            return JsonResponse(response)
        if student.teacher is None:
            response = {'msg': 'ok', 'student_name': user.name, 'student_id': user.username, 'email': user.email,
                        'mobile': user.mobile, 'student_type': student.student_type, 'teacher': '未选择', 'institute': '空'}
            return JsonResponse(response)
        else:
            response = {'msg': 'ok', 'student_name': user.name, 'student_id': user.username, 'email': user.email,
                        'mobile': user.mobile, 'student_type': student.student_type, 'teacher': student.teacher.user.name,
                        'institute': student.teacher.institute}
            return JsonResponse(response)

    @staticmethod
    def post(request):
        user = request.user
        data = request.POST
        email = data.get('email')
        mobile = data.get('mobile')
        try:
            user.email = email
            user.mobile = mobile
            user.save()
            return HttpResponse('ok')
        except Exception as e:
            print(str(e))
            return HttpResponse(str(e))


'''
学生详细信息，根据学生id查找账户
供导师和辅导员查看
'''


def student_detail(request):
    uid = request.POST.get('id')
    try:
        user = User.objects.get(username=id)
        student = user.student
        response = {'msg': 'ok', 'student_name': user.name, 'student_id': user.username, 'email': user.email,
                    'mobile': user.mobile, 'student_type': student.student_type}
        return JsonResponse(response)
    except Exception as e:
        print(str(e))
        return JsonResponse({'msg': str(e)})


'''
学生已填报的志愿的状态列表
未确认、同意、拒绝
'''


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


'''
学生未完成progress列表
'''


def s_progress_list_unfinished(request):
    student = request.user.student
    if student is None:
        response = {'msg': 'user does not found'}
        return HttpResponse(json.dumps(response))
    res = []
    now = datetime.now(tz=timezone.utc)
    print(now)
    detail_list = ProgressDetail.objects.filter(start_time__lt=now, end_time__gt=now)
    for detail in detail_list:
        print(detail.title, detail.start_time, detail.end_time)
        progress = Progress.objects.filter(detail=detail, student=student, student_ok=False).count()
        if progress != 0:
            json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                         'end_time': detail.end_time, 'status': '未完成'}
            res.append(json_item)
    detail_list = ProgressDetail.objects.filter(end_time__lt=now)
    for detail in detail_list:
        progress = Progress.objects.filter(detail=detail, student=student, student_ok=False).count()
        if progress != 0:
            json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                         'end_time': detail.end_time, 'status': '已失效'}
            res.append(json_item)
    return HttpResponse(json.dumps(res, cls=ComplexEncoder))


'''
学生已完成但导师未批改的progress列表
'''


def s_half(request):
    student = request.user.student
    if student is None:
        response = {'msg': 'user does not found'}
        return HttpResponse(json.dumps(response))
    res = []
    now = datetime.now(tz=timezone.utc)
    detail_list = ProgressDetail.objects.filter(start_time__lt=now)
    for detail in detail_list:
        progress = Progress.objects.filter(detail=detail, student=student, student_ok=True, teacher_ok=False).count()
        if progress != 0:
            json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                         'end_time': detail.end_time, 'status': '未批改'}
            res.append(json_item)
    return HttpResponse(json.dumps(res, cls=ComplexEncoder))


'''
学生已完成且导师已批改的progress列表
'''


def s_progress_list_finished(request):
    student = request.user.student
    if student is None:
        response = {'msg': 'user does not found'}
        return HttpResponse(json.dumps(response))
    progress_list = Progress.objects.filter(student=student, student_ok=True, teacher_ok=True)
    res = []
    for progress in progress_list:
        json_item = {'id': progress.detail.unique_id, 'title': progress.detail.title,
                     'start_time': progress.detail.start_time, 'end_time': progress.detail.end_time, 'status': '已批改'}
        res.append(json_item)
    return HttpResponse(json.dumps(res, cls=ComplexEncoder))


'''
学生progress详情，post提供修改
'''


class S_Progress_Detail(View):
    @staticmethod
    def get(request):
        uid = request.GET.get('id')
        student = request.user.student
        try:
            detail = ProgressDetail.objects.get(unique_id=uid)
            progress = Progress.objects.get(detail=detail, student=student)
            response = {'msg': 'ok', 'title': detail.title, 'desc': detail.desc, 'start_time': detail.start_time,
                        'end_time': detail.end_time, 'student_text': progress.student_text,
                        'teacher_text': progress.teacher_text, 'student_id':student.user.username,
                        'student_file': progress.file, 'progress_file': detail.file}
            return JsonResponse(response, encoder=ComplexEncoder)
        except Exception as e:
            response = {'msg': str(e)}
            return JsonResponse(response)

    @staticmethod
    def post(request):
        data = request.POST
        student_text = data.get('student_text')
        uid = data.get('id')
        print(request.FILES)
        file = request.FILES.get('file', None)
        print(file)
        student = request.user.student
        try:
            detail = ProgressDetail.objects.get(unique_id=uid)
            now = datetime.now(tz=timezone.utc)
            if detail.start_time < now < detail.end_time:
                progress = Progress.objects.get(detail=detail, student=student)
                if progress.teacher_ok:
                    return HttpResponse('老师已批改，不可再次提交')
                progress.student_text = student_text
                progress.student_ok = True
                filename = file.name
                s_dir = 'templates/student_file/' + str(detail.unique_id) + '_' + detail.title + '/' + student.user.username
                mkdir(s_dir)
                with open(s_dir + '/' + filename, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                progress.student_file = filename
                progress.save()
                return HttpResponse('ok')
            else:
                return HttpResponse('out of date')
        except Exception as e:
            return HttpResponse(str(e))


'''
导师界面
导师查看已填报志愿并进行确认操作
'''


class T_Choice(View):
    @staticmethod
    def get(request):
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
        print(count)
        print(teacher.max_student)
        student = User.objects.get(username=student_id).student
        if student.teacher is None:    # 该学生未选择导师
            choose = Choose.objects.get(student=student, teacher=teacher)
            if count < teacher.max_student:   # 该老师还有名额
                choose.teacher_choice = choice
                choose.save()
                if choice == '2':
                    student.teacher = teacher
                    student.save()
                return HttpResponse('ok')
            else:
                choose.teacher_choice = 3
                choose.save()
                return HttpResponse('max')
        else:
            return HttpResponse('student has teacher')


'''
导师查看已确认过的志愿列表
'''
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
导师   学生尚未提交progress列表
'''


def t_progress_list_unfinished(request):
    teacher = request.user.teacher
    response = {}
    if teacher is None:
        response['msg'] = 'user does not found'
        return HttpResponse(response)
    # time_now = timezone.now()
    now = datetime.now(tz=timezone.utc)
    res = []
    detail_list = ProgressDetail.objects.filter(start_time__lt=now, end_time__gt=now)
    for detail in detail_list:
        progress_list = Progress.objects.filter(detail=detail, student_ok=False, teacher=teacher)
        # length = progress_list.count()
        # if length != 0:
        for progress in progress_list:
            json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                         'end_time': detail.end_time, 'msg': '未完成', 'student_id': progress.student.user.username,
                         'student_name': progress.student.user.name}
            res.append(json_item)
    detail_list = ProgressDetail.objects.filter(end_time__lt=now)
    for detail in detail_list:
        progress_list = Progress.objects.filter(detail=detail, student_ok=False, teacher=teacher)
        for progress in progress_list:
            json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                         'end_time': detail.end_time, 'msg': '超时未完成', 'student_id': progress.student.user.username,
                         'student_name': progress.student.user.name}
            res.append(json_item)
    return HttpResponse(json.dumps(res, cls=ComplexEncoder))


'''
导师  学生已提交但未批改progress
'''


def t_half(request):
    teacher = request.user.teacher
    response = {}
    if teacher is None:
        response['msg'] = 'user does not found'
        return HttpResponse(response)
    now = datetime.now(tz=timezone.utc)
    res = []
    progress_list = Progress.objects.filter(student_ok=True, teacher=teacher, teacher_ok=False)
    for progress in progress_list:
        detail = progress.detail
        json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                     'end_time': detail.end_time, 'msg': '未回复', 'student_id': progress.student.user.username,
                     'student_name': progress.student.user.name}
        res.append(json_item)
    res.sort(key=lambda k: k['start_time'])
    return HttpResponse(json.dumps(res, cls=ComplexEncoder))


'''
导师已批改列表
'''


def t_progress_list_finished(request):
    teacher = request.user.teacher
    response = {}
    if teacher is None:
        response['msg'] = 'user does not found'
        return HttpResponse(json.dumps(response))
    # time_now = timezone.now()
    now = datetime.now(tz=timezone.utc)
    progress_list = Progress.objects.filter(teacher=teacher, student_ok=True, teacher_ok=True)
    res = []
    for progress in progress_list:
        detail = progress.detail
        json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                     'end_time': detail.end_time, 'msg': '已完成', 'student_id': progress.student.user.username,
                     'student_name': progress.student.user.name}
        res.append(json_item)
    res.sort(key=lambda k: k['start_time'])
    return HttpResponse(json.dumps(res, cls=ComplexEncoder))



'''
导师查看progress详情
'''
class T_Progress_Detail(View):
    @staticmethod
    def get(request):
        uid = request.GET.get('id')
        student_id = request.GET.get('student_id')
        teacher = request.user.teacher
        try:
            student = User.objects.get(username=student_id).student
            detail = ProgressDetail.objects.get(unique_id=uid)
            progress = Progress.objects.get(detail=detail, teacher=teacher, student=student)
            response = {'msg': 'ok', 'title': detail.title, 'desc': detail.desc, 'start_time': detail.start_time,
                        'end_time': detail.end_time, 'student_name': student.user.name, 'student_text': progress.student_text,
                        'teacher_text': progress.teacher_text, 'student_file': progress.file, 'progress_file': detail.file}
            return JsonResponse(response, encoder=ComplexEncoder)
        except Exception as e:
            response = {'msg': str(e)}
            return JsonResponse(response)

    @staticmethod
    def post(request):
        data = request.POST
        teacher_text = data.get('teacher_text')
        uid = data.get('id')
        student_id = data.get('student_id')
        teacher = request.user.teacher
        try:
            student = User.objects.get(username=student_id).student
            detail = ProgressDetail.objects.get(unique_id=uid)
            progress = Progress.objects.get(detail=detail, teacher=teacher, student=student)
            progress.teacher_text = teacher_text
            progress.teacher_ok = True
            progress.save()
            return HttpResponse('ok')
        except Exception as e:
            return HttpResponse(str(e))





'''
辅导员界面
辅导员查看当前学生列表，并查看其导师
'''


def student_list(request):
    s_list = Student.objects.all()
    response = []
    for student in s_list:
        json_item = {}
        if student.teacher is None:
            json_item = {'student_name': student.user.name, 'teacher_name': '未选择'}
        else:
            json_item = {'student_name': student.user.name, 'teacher_name': student.teacher.user.name}
        response.append(json_item)
    response.sort(key=lambda k: k['teacher_name'])
    return HttpResponse(json.dumps(response))


'''
辅导员创建progress
'''


def create_progress(request):
    data = request.POST
    title = data.get('title')
    desc = data.get('desc')
    s_time = data.get('start_time').split('-')
    e_time = data.get('end_time').split('-')
    file = request.FILES.get('file', None)
    print(title, desc, s_time, e_time)
    start_time = datetime(int(s_time[0]), int(s_time[1]), int(s_time[2]), int(s_time[3]), int(s_time[4]), int(s_time[5]), tzinfo=UTC(0))
    end_time = datetime(int(e_time[0]), int(e_time[1]), int(e_time[2]), int(e_time[3]), int(e_time[4]), int(e_time[5]), tzinfo=UTC(0))
    student_list = Student.objects.all()
    length = ProgressDetail.objects.all().count() + 1
    email_list = []
    filename = file.name
    try:
        s_dir = 'templates/progress_file/' + str(length) + '_' + title
        mkdir(s_dir)
        with open(s_dir + '/' + filename, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        progress = ProgressDetail.objects.create(unique_id=length, title=title, desc=desc,
                                                 start_time=start_time, end_time=end_time, file=filename)

        for student in student_list:
            Progress.objects.create(detail=progress, student=student, teacher=student.teacher)
            email_list.append(student.user.email)
        print('send email start')
        send_mail(title, desc, 'zhangrt20@126.com', email_list, fail_silently=False)
        print('send email end')
        return HttpResponse('ok')
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e))


'''
辅导员查看progress列表
'''


def a_progress_list(request):
    progress_list = ProgressDetail.objects.all().order_by('-start_time')
    response = []
    for progress in progress_list:
        json_item = {'id': progress.unique_id, 'title': progress.title, 'start_time': progress.start_time,
                     'end_time': progress.end_time}
        response.append(json_item)
    return HttpResponse(json.dumps(response, cls=ComplexEncoder))


'''
辅导员查看当前progress下的student和teacher回复完成情况
'''


def a_plist_student_list(request):
    uid = request.GET.get('id')
    print(request.GET)
    print(int(uid))
    detail = ProgressDetail.objects.get(unique_id=int(uid))
    progress_list = detail.progress_set.all()
    finished = []
    half = []
    unfinished = []
    for progress in progress_list:
        if progress.student_ok:
            if progress.teacher_ok:
                json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                             'end_time': detail.end_time, 'student_name': progress.student.user.name,
                             'student_id': progress.student.user.username, 'student_ok': '已完成',
                             'teacher': progress.teacher.user.name, 'teacher_ok': '已完成'}
                finished.append(json_item)
            else:
                if progress.teacher is None:
                    json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                                 'end_time': detail.end_time, 'student_name': progress.student.user.name,
                                 'student_id': progress.student.user.username, 'student_ok': '已完成',
                                 'teacher': '未选择', 'teacher_ok': '空'}
                    half.append(json_item)
                else:
                    json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                                 'end_time': detail.end_time, 'student_name': progress.student.user.name,
                                 'student_id': progress.student.user.username, 'student_ok': '已完成',
                                 'teacher': progress.teacher.user.name, 'teacher_ok': '未批改'}
                    half.append(json_item)
        else:
            if progress.teacher is None:
                json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time':detail.start_time,
                             'end_time': detail.end_time, 'student_name': progress.student.user.name,
                             'student_id': progress.student.user.username, 'student_ok': '未完成',
                             'teacher': '未选择', 'teacher_ok': '空'}
                unfinished.append(json_item)
            else:
                json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                             'end_time': detail.end_time, 'student_name': progress.student.user.name,
                             'student_id': progress.student.user.username, 'student_ok': '未完成',
                             'teacher': progress.teacher.user.name,  'teacher_ok': '未批改'}
                unfinished.append(json_item)
    return HttpResponse(json.dumps(finished + half + unfinished, cls=ComplexEncoder))


'''
辅导员查看当前progress下id为xxxxx的学生的进度详情
'''


def progress_detail(request):
    uid = request.GET.get('id')
    student_id = request.GET.get('student_id')
    print(uid, student_id)
    student = User.objects.get(username=student_id).student
    print(student)
    try:
        progress = ProgressDetail.objects.get(unique_id=uid)
        detail = Progress.objects.get(detail=progress, student=student)
        if detail.teacher is None:
            response = {'msg': 'ok', 'title': progress.title, 'desc': progress.desc, 'progress_file': progress.file,
                        'student_name': student.user.name, 'student_text': detail.student_text,
                        'teacher_name': '未选择', 'teacher_text': '空', 'student_file': detail.file}
            print(response)
            return JsonResponse(response)
        else:
            response = {'msg': 'ok', 'title': progress.title, 'desc': progress.desc, 'progress_file': progress.file,
                        'student_name': student.user.name, 'student_text': detail.student_text,
                        'teacher_name': student.teacher.user.name, 'teacher_text': detail.teacher_text,
                        'student_file': detail.file}
            print(response)
            return JsonResponse(response)
    except Exception as e:
        response = {'msg': str(e)}
        print(response)
        return JsonResponse(response)


def mkdir(path):
    path = path.strip()
    path = path.replace('\\','/')
    path = path.rstrip('/')
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path.encode('utf-8').decode('utf-8'))
        print("创建成功"+path)


'''
def s_file_upload(request):
    uid = request.POST.get('id')
    file = request.FILES.get('userFile', None)
    student = request.user.student
    try:
        detail = ProgressDetail.objects.get(unique_id=uid)
        progress = Progress.objects.get(detail=detail, student=student)
        filename = file.name
        s_dir = 'templates/student_file/' + detail.unique_id + '_' + detail.title + '/' + student.user.username
        mkdir(s_dir)
        with open(s_dir + '/' + filename, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        progress.student_file = filename
        progress.save()
        return HttpResponse('ok')
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e))


def a_file_upload(request):
    uid = request.POST.get('id')
    file = request.FILES.get('userFile', None)
    try:
        detail = ProgressDetail.objects.get(unique_id=uid)
        filename = file.name
        s_dir = 'templates/progress_file/' + detail.unique_id + '_' + detail.title
        mkdir(s_dir)
        with open(s_dir + '/' + filename, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)
        detail.file = filename
        detail.save()
        return HttpResponse('ok')
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e))
'''


def file_iterator(file_name, chunk_size=512):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def progress_file_download(request):
    uid = request.POST.get('id')
    try:
        detail = ProgressDetail.objects.get(unique_id=uid)
        s_dir = 'templates/progress_file/' + detail.unique_id + '_' + detail.title
        filename = os.path.join(s_dir, detail.file).replace('\\', '/')
        response = StreamingHttpResponse(file_iterator(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path(filename))
        return response
    except Exception as e:
        return HttpResponse(str(e))


def student_file_download(request):
    uid = request.POST.get('id')
    student_id = request.POST.get('student_id')
    try:
        detail = ProgressDetail.objects.get(unique_id=uid)
        student = User.objects.get(username=student_id).student
        progress = Progress.objects.get(detail=detail, student=student)
        s_dir = 'templates/student_file/' + detail.unique_id + '_' + detail.title + '/' + student.user.username
        filename = os.path.join(s_dir, progress.file).replace('\\', '/')
        response = StreamingHttpResponse(file_iterator(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(escape_uri_path(filename))
        return response
    except Exception as e:
        return HttpResponse(str(e))

















