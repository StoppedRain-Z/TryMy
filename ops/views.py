from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.hashers import make_password
from .models import *
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse, FileResponse
import json
from datetime import datetime, tzinfo, timedelta, date
from django.utils import timezone
from urllib.parse import quote
import pytz
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
import operator
import os
import xlrd
from users.views import check_email, check_mobile
from django.utils.decorators import method_decorator
from django.utils.encoding import escape_uri_path
# Create your views here.


EMAIL_ADDRESS = 'zhangrt20@126.com'


def teacher_desc(name, title):
    start = '老师，您好'
    content = '您的学生' + name + '已完成毕设进度检查：' + title
    end = '请您及时上线查看批改'
    wish = '此邮件为系统自动邮件，请勿回复'
    return start + content + end + wish


def desc_detail(title, desc):
    hello = '同学，你好'
    head_desc = '你的辅导员发布了新的毕设进度检查。'
    new_title = '进度标题：' + title
    new_desc = '进度描述：' + desc
    end = '此邮件为系统自动邮件，请勿回复'
    return hello + head_desc + new_title + new_desc + end


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
    def __init__(self, offset=0):
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
        student = request.user.student
        grade = student.grade
        json_list = []
        for teacher in teacher_list:
            u_count = teacher.student_set.filter(student_type='U', grade=grade).count()
            f_count = teacher.student_set.filter(student_type='F', grade=grade).count()
            json_item = {"teacher_name": teacher.user.name,
                         "teacher_institute": teacher.institute,
                         "teacher_info": teacher.teacher_info,
                         "teacher_id": teacher.user.username,
                         "student_count": str(u_count) + '/' + str(teacher.max_student),
                         "foreign_count": str(f_count) + '/' + str(teacher.max_foreign),
                         "mobile": teacher.user.mobile,
                         "email": teacher.user.email}

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
        grade = student.grade
        count = 0
        max_count = 0
        if student_type == 'U':
            count = teacher.student_set.filter(student_type='U', grade=grade).count()
            max_count = teacher.max_student
        elif student_type == 'F':
            count = teacher.student_set.filter(student_type='F', grade=grade).count()
            max_count = teacher.max_foreign
        print(count)
        print(teacher.max_student)
        if count < max_count:
            choose_list = Choose.objects.filter(student=student, teacher=teacher, grade=student.grade).count()
            print(choose_list)
            if choose_list == 0:
                Choose.objects.create(student=student, teacher=teacher, teacher_choice=1, student_choice=2, grade=grade)
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
                        'mobile': user.mobile, 'student_type': student.student_type, 'teacher': '未选择',
                        'institute': '空', 'grade': student.grade}
            return JsonResponse(response)
        else:
            response = {'msg': 'ok', 'student_name': user.name, 'student_id': user.username, 'email': user.email,
                        'mobile': user.mobile, 'student_type': student.student_type, 'teacher': student.teacher.user.name,
                        'institute': student.teacher.institute, 'grade': student.grade}
            return JsonResponse(response)

    @staticmethod
    def post(request):
        user = request.user
        student = user.student
        data = request.POST
        email = data.get('email')
        mobile = data.get('mobile')
        grade = data.get('grade')
        if not check_email(email):
            return HttpResponse('邮箱格式错误')
        if not check_mobile(mobile):
            return HttpResponse('手机格式错误')
        try:
            user.email = email
            user.mobile = mobile
            user.save()
            student.grade = grade
            student.save()
            return HttpResponse('ok')
        except Exception as e:
            print(str(e))
            return HttpResponse(str(e))


'''
学生详细信息，根据学生id查找账户
供导师和辅导员查看
'''


@login_required
def student_detail(request):
    uid = request.POST.get('id')
    try:
        user = User.objects.get(username=id)
        student = user.student
        response = {'msg': 'ok', 'student_name': user.name, 'student_id': user.username, 'email': user.email,
                    'mobile': user.mobile, 'student_type': student.student_type, 'grade': student.grade}
        return JsonResponse(response)
    except Exception as e:
        print(str(e))
        return JsonResponse({'msg': str(e)})


'''
学生已填报的志愿的状态列表
未确认、同意、拒绝
'''


@login_required
def cancel_choose(request):
    student = request.user.student
    teacher_id = request.POST.get('teacher_id')
    try:
        teacher = User.objects.get(username=teacher_id).teacher
        choose = Choose.objects.get(student=student, teacher=teacher, grade=student.grade)
        if choose.teacher_choice == 1:  # 导师未确认
            choose.teacher_choice = 3
            choose.student_choice = 4
            choose.save()
            return HttpResponse('取消成功')
        elif choose.teacher_choice == 2:   # 导师已确认
            choose.teacher_choice = 3
            choose.student_choice = 4
            choose.save()
            student.teacher = None
            student.save()
            return HttpResponse('导师关系已取消')
        elif choose.teacher_choice == 3:
            return HttpResponse('无需取消')
    except Exception as e:
        return HttpResponse(str(e))


@login_required
def confirm_list_s(request):
    user = request.user
    student = Student.objects.get(user=user)
    choose_list = Choose.objects.filter(student=student, student_choice=2, grade=student.grade)
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
        json_list.sort(key=lambda k: k['teacher_choice'])
    choose_list = Choose.objects.filter(student=student, student_choice=4, grade=student.grade)
    for choose in choose_list:
        json_item = {"name": choose.teacher.user.name, "teacher_id": choose.teacher.user.username,
                     "teacher_choice": '已取消', "teacher_info": choose.teacher.teacher_info}
        json_list.append(json_item)
    return HttpResponse(json.dumps(json_list))


'''
学生未完成progress列表
'''


@login_required
def s_progress_list_unfinished(request):
    student = request.user.student
    if student is None:
        response = {'msg': 'user does not found'}
        return HttpResponse(json.dumps(response))
    res = []
    now = timezone.now()
    print(now)
    detail_list = ProgressDetail.objects.filter(start_time__lt=now, end_time__gt=now, grade=student.grade)
    for detail in detail_list:
        print(detail.title, detail.start_time, detail.end_time)
        progress = Progress.objects.filter(detail=detail, student=student, student_ok=False).count()
        if progress != 0:
            json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                         'end_time': detail.end_time, 'status': '未完成'}
            res.append(json_item)
    detail_list = ProgressDetail.objects.filter(end_time__lt=now, grade=student.grade)
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


@login_required
def s_half(request):
    student = request.user.student
    if student is None:
        response = {'msg': 'user does not found'}
        return HttpResponse(json.dumps(response))
    res = []
    now = timezone.now()
    print(now)
    detail_list = ProgressDetail.objects.filter(start_time__lt=now, grade=student.grade)
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


@login_required
def s_progress_list_finished(request):
    student = request.user.student
    if student is None:
        response = {'msg': 'user does not found'}
        return HttpResponse(json.dumps(response))
    detail_list = ProgressDetail.objects.filter(grade=student.grade)
    progress_list = []
    for detail in detail_list:
        try:
            progress = Progress.objects.get(detail=detail, student=student, student_ok=True, teacher_ok=True)
            progress_list.append(progress)
        except Exception as e:
            print(str(e))
            continue
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
            detail = ProgressDetail.objects.get(unique_id=uid, grade=student.grade)
            progress = Progress.objects.get(detail=detail, student=student)
            response = {'msg': 'ok', 'title': detail.title, 'desc': detail.desc, 'start_time': detail.start_time,
                        'end_time': detail.end_time, 'student_text': progress.student_text, 'progress_file': detail.file,
                        'student_id': student.user.username, 'student_file': progress.student_file}
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
            detail = ProgressDetail.objects.get(unique_id=uid, grade=student.grade)
            now = timezone.now()
            print(now)
            if detail.start_time < now < detail.end_time:
                progress = Progress.objects.get(detail=detail, student=student)
                if progress.teacher_ok:
                    return HttpResponse('老师已批改，不可再次提交')
                progress.student_text = student_text
                progress.student_ok = True
                if file is not None:
                    filename = file.name
                    s_dir = 'templates/student_file/' + str(detail.unique_id) + '_' + detail.title + '/' + student.user.username
                    mkdir(s_dir)
                    with open(s_dir + '/' + filename, 'wb') as f:
                        for chunk in file.chunks():
                            print(chunk)
                            f.write(chunk)
                    progress.student_file = filename
                progress.save()
                # 向老师发送邮件
                print('send_mail teacher start')
                send_mail("学生作业提交", teacher_desc(student.user.name, detail.title), EMAIL_ADDRESS, [progress.teacher.user.email], fail_silently=False)
                print('send_mail teacher end')
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
        choose_list = Choose.objects.filter(teacher=teacher, student_choice=2, teacher_choice=1).order_by('-grade')
        json_list = []
        for choose in choose_list:
            if choose.student.student_type == 'U':
                json_item = {"student_id": choose.student.user.username, "name": choose.student.user.name,
                             "type": '非留学生', "grade": choose.grade}
                json_list.append(json_item)
            elif choose.student.student_type == 'F':
                json_item = {"student_id": choose.student.user.username, "name": choose.student.user.name,
                             "type": '留学生', "grade": choose.grade}
                json_list.append(json_item)
        print(json_list)
        return HttpResponse(json.dumps(json_list))

    @staticmethod
    def post(request):
        data = request.POST
        print(data)
        grade = int(data.get('grade'))
        student_id = data.get('student_id')
        choice = data.get('choice')
        teacher = request.user.teacher
        student = User.objects.get(username=student_id).student
        print(student.grade, grade)
        if grade != student.grade:
            return HttpResponse('学生毕业年级有误')
        if student.teacher is None:    # 该学生未选择导师
            choose = Choose.objects.get(student=student, teacher=teacher, grade=student.grade)
            if student.student_type == 'U':
                count = teacher.student_set.filter(student_type='U', grade=student.grade).count()
                max_count = teacher.max_student
                if count >= max_count:
                    choose.teacher_choice = 3
                    choose.save()
                    return HttpResponse('U_max')
            elif student.student_type == 'F':
                count = teacher.student_set.filter(student_type='F', grade=student.grade).count()
                max_count = teacher.max_foreign
                if count >= max_count:
                    choose.teacher_choice = 3
                    choose.save()
                    return HttpResponse('F_max')
            choose.teacher_choice = choice
            choose.save()
            if choice == '2':
                student.teacher = teacher
                student.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('student has teacher')


class T_Detail(View):
    @staticmethod
    def get(request):
        user = request.user
        teacher = user.teacher
        if teacher is None:
            response = {'msg': 'user not exist'}
            return JsonResponse(response)
        response = {'msg': 'ok', 'teacher_name': user.name, 'teacher_id': user.username, 'email': user.email,
                    'mobile': user.mobile, 'institute': teacher.institute, 'teacher_info': teacher.teacher_info}
        return JsonResponse(response)

    @staticmethod
    def post(request):
        user = request.user
        teacher = user.teacher
        data = request.POST
        email = data.get('email')
        mobile = data.get('mobile')
        info = data.get('teacher_info')
        if not check_email(email):
            return HttpResponse('邮箱格式错误')
        if not check_mobile(mobile):
            return HttpResponse('手机格式错误')
        try:
            user.email = email
            user.mobile = mobile
            user.save()
            teacher.teacher_info = info
            teacher.save()
            return HttpResponse('ok')
        except Exception as e:
            print(str(e))
            return HttpResponse(str(e))



'''
导师查看已确认过的志愿列表
'''


@login_required
def confirm_list_t(request):
    teacher = request.user.teacher
    choose_list = Choose.objects.filter(teacher=teacher).exclude(teacher_choice=1).order_by('-grade')
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


@login_required
def t_progress_list_unfinished(request):
    teacher = request.user.teacher
    response = {}
    if teacher is None:
        response['msg'] = 'user does not found'
        return HttpResponse(response)
    # time_now = timezone.now()
    now = timezone.now()
    print(now)
    res = []
    detail_list = ProgressDetail.objects.filter(start_time__lt=now, end_time__gt=now)
    for detail in detail_list:
        progress_list = Progress.objects.filter(detail=detail, student_ok=False, teacher=teacher)
        for progress in progress_list:
            json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                         'end_time': detail.end_time, 'msg': '未完成', 'student_id': progress.student.user.username,
                         'student_name': progress.student.user.name, 'grade': detail.grade}
            res.append(json_item)
    detail_list = ProgressDetail.objects.filter(end_time__lt=now)
    for detail in detail_list:
        progress_list = Progress.objects.filter(detail=detail, student_ok=False, teacher=teacher)
        for progress in progress_list:
            json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                         'end_time': detail.end_time, 'msg': '超时未完成', 'student_id': progress.student.user.username,
                         'student_name': progress.student.user.name, 'grade': detail.grade}
            res.append(json_item)
    res.sort(key=lambda k: (-k['grade'], k['msg']))
    return HttpResponse(json.dumps(res, cls=ComplexEncoder))


'''
导师  学生已提交但未批改progress
'''


@login_required
def t_half(request):
    teacher = request.user.teacher
    response = {}
    if teacher is None:
        response['msg'] = 'user does not found'
        return HttpResponse(response)
    now = timezone.now()
    print(now)
    res = []
    progress_list = Progress.objects.filter(student_ok=True, teacher=teacher, teacher_ok=False)
    for progress in progress_list:
        detail = progress.detail
        json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                     'end_time': detail.end_time, 'msg': '未回复', 'student_id': progress.student.user.username,
                     'student_name': progress.student.user.name, 'grade': detail.grade}
        res.append(json_item)
    res.sort(key=lambda k: (-k['grade'], k['start_time']))
    return HttpResponse(json.dumps(res, cls=ComplexEncoder))


'''
导师已批改列表
'''


@login_required
def t_progress_list_finished(request):
    teacher = request.user.teacher
    response = {}
    if teacher is None:
        response['msg'] = 'user does not found'
        return HttpResponse(json.dumps(response))
    # time_now = timezone.now()
    now = timezone.now()
    print(now)
    progress_list = Progress.objects.filter(teacher=teacher, student_ok=True, teacher_ok=True)
    res = []
    for progress in progress_list:
        detail = progress.detail
        json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                     'end_time': detail.end_time, 'msg': '已完成', 'student_id': progress.student.user.username,
                     'student_name': progress.student.user.name, 'grade': detail.grade}
        res.append(json_item)
    res.sort(key=lambda k: (-k['grade'], k['start_time']))
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
            detail = ProgressDetail.objects.get(unique_id=uid, grade=student.grade)
            progress = Progress.objects.get(detail=detail, teacher=teacher, student=student)
            response = {'msg': 'ok', 'title': detail.title, 'desc': detail.desc, 'start_time': detail.start_time,
                        'end_time': detail.end_time, 'student_name': student.user.name, 'student_text': progress.student_text,
                        'teacher_text': progress.teacher_text, 'student_file': progress.student_file,
                        'progress_file': detail.file, 'status': progress.status}
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
        status = data.get('status')
        teacher = request.user.teacher
        try:
            student = User.objects.get(username=student_id).student
            detail = ProgressDetail.objects.get(unique_id=uid, grade=student.grade)
            progress = Progress.objects.get(detail=detail, teacher=teacher, student=student)
            progress.teacher_text = teacher_text
            progress.teacher_ok = True
            progress.status = status
            progress.save()
            return HttpResponse('ok')
        except Exception as e:
            return HttpResponse(str(e))





'''
辅导员界面
辅导员查看当前学生列表，并查看其导师
'''


@login_required
def student_list(request):
    assistant = request.user.assistant
    s_list = Student.objects.filter(grade=assistant.grade).exclude(teacher=None)
    response = []
    for student in s_list:
        json_item = {'student_name': student.user.name, 'teacher_name': student.teacher.user.name,
                     'institute': student.teacher.institute}
        response.append(json_item)
    response.sort(key=lambda k: (k['institute'], k['teacher_name']))
    return HttpResponse(json.dumps(response))


@login_required
def student_list_not_selected(request):
    assistant = request.user.assistant
    s_list = Student.objects.filter(grade=assistant.grade, teacher=None)
    response = []
    for student in s_list:
        json_item = {'student_name': student.user.name, 'teacher_name': '未选择'}
        response.append(json_item)
    return HttpResponse(json.dumps(response))


'''
辅导员创建progress
'''


@login_required
def create_progress(request):
    assistant = request.user.assistant
    data = request.POST
    title = data.get('title')
    desc = data.get('desc')
    s_time = data.get('start_time').split('-')
    e_time = data.get('end_time').split('-')
    file = request.FILES.get('file', None)
    print(title, desc, s_time, e_time)
    start_time = datetime(int(s_time[0]), int(s_time[1]), int(s_time[2]), int(s_time[3]), int(s_time[4]), int(s_time[5]))
    end_time = datetime(int(e_time[0]), int(e_time[1]), int(e_time[2]), int(e_time[3]), int(e_time[4]), int(e_time[5]))
    student_list = Student.objects.filter(grade=assistant.grade).exclude(teacher=None)
    length = ProgressDetail.objects.all().count() + 1
    email_list = []
    filename = ''
    try:
        if file is not None:
            filename = file.name
            s_dir = 'templates/progress_file/' + str(length) + '_' + title
            mkdir(s_dir)
            with open(s_dir + '/' + filename, 'wb') as f:
                for chunk in file.chunks():
                    print(chunk)
                    f.write(chunk)
        progress = ProgressDetail.objects.create(unique_id=length, title=title, desc=desc, grade=assistant.grade,
                                                 start_time=start_time, end_time=end_time, file=filename)

        for student in student_list:
            Progress.objects.create(detail=progress, student=student, teacher=student.teacher)
            email_list.append(student.user.email)
        print('send email start')
        send_mail(title, desc_detail(title, desc), EMAIL_ADDRESS, email_list, fail_silently=False)
        print('send email end')
        return HttpResponse('ok')
    except Exception as e:
        print(str(e))
        return HttpResponse(str(e))


'''
辅导员查看progress列表
'''


@login_required
def a_progress_list(request):
    assistant = request.user.assistant
    progress_list = ProgressDetail.objects.filter(grade=assistant.grade).order_by('-start_time')
    response = []
    for progress in progress_list:
        json_item = {'id': progress.unique_id, 'title': progress.title, 'start_time': progress.start_time,
                     'end_time': progress.end_time}
        response.append(json_item)
    return HttpResponse(json.dumps(response, cls=ComplexEncoder))


'''
辅导员查看当前progress下的student和teacher回复完成情况
'''


@login_required
def a_plist_student_list(request):
    assistant = request.user.assistant
    uid = request.GET.get('id')
    try:
        detail = ProgressDetail.objects.get(unique_id=int(uid), grade=assistant.grade)
        progress_list = detail.progress_set.all()
        finished = []
        half = []
        unfinished = []
        for progress in progress_list:
            if progress.student_ok:
                if progress.teacher_ok:
                    status = ''
                    if progress.status == 1:
                        status = '超进度完成'
                    elif progress.status == 2:
                        status = '按时完成'
                    elif progress.status == 3:
                        status = '未达到预期'
                    json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                                 'end_time': detail.end_time, 'student_name': progress.student.user.name,
                                 'student_id': progress.student.user.username, 'student_ok': '已完成',
                                 'teacher': progress.teacher.user.name, 'teacher_ok': status,
                                 'teacher_id': progress.teacher.user.username}
                    finished.append(json_item)
                else:
                    if progress.teacher is None:
                        json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                                     'end_time': detail.end_time, 'student_name': progress.student.user.name,
                                     'student_id': progress.student.user.username, 'student_ok': '已完成',
                                     'teacher': '未选择', 'teacher_ok': '空',
                                     'teacher_id': progress.teacher.user.username}
                        half.append(json_item)
                    else:
                        json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                                     'end_time': detail.end_time, 'student_name': progress.student.user.name,
                                     'student_id': progress.student.user.username, 'student_ok': '已完成',
                                     'teacher': progress.teacher.user.name, 'teacher_ok': '未批改',
                                     'teacher_id': progress.teacher.user.username}
                        half.append(json_item)
            else:
                if progress.teacher is None:
                    json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time':detail.start_time,
                                 'end_time': detail.end_time, 'student_name': progress.student.user.name,
                                 'student_id': progress.student.user.username, 'student_ok': '未完成',
                                 'teacher': '未选择', 'teacher_ok': '空',
                                 'teacher_id': progress.teacher.user.username}
                    unfinished.append(json_item)
                else:
                    json_item = {'id': detail.unique_id, 'title': detail.title, 'start_time': detail.start_time,
                                 'end_time': detail.end_time, 'student_name': progress.student.user.name,
                                 'student_id': progress.student.user.username, 'student_ok': '未完成',
                                 'teacher': progress.teacher.user.name,  'teacher_ok': '未批改',
                                 'teacher_id': progress.teacher.user.username}
                    unfinished.append(json_item)
        return HttpResponse(json.dumps(finished + half + unfinished, cls=ComplexEncoder))
    except Exception as e:
        return HttpResponse(str(e))


'''
辅导员查看当前progress下id为xxxxx的学生的进度详情
'''


@login_required
def progress_detail(request):
    uid = request.GET.get('id')
    student_id = request.GET.get('student_id')
    print(uid, student_id)
    student = User.objects.get(username=student_id).student
    print(student)
    try:
        progress = ProgressDetail.objects.get(unique_id=uid, grade=student.grade)
        detail = Progress.objects.get(detail=progress, student=student)
        status = ''
        if detail.status == 1:
            status = '超进度完成'
        elif detail.status == 2:
            status = '按时完成'
        elif detail.status == 3:
            status = '未达到预期'
        elif detail.status == 4:
            status = '未批改'
        if detail.teacher is None:
            response = {'msg': 'ok', 'title': progress.title, 'desc': progress.desc, 'progress_file': progress.file,
                        'student_name': student.user.name, 'student_text': detail.student_text, 'status': '',
                        'teacher_name': '未选择', 'teacher_text': '空', 'student_file': detail.student_file}
            print(response)
            return JsonResponse(response)
        else:
            response = {'msg': 'ok', 'title': progress.title, 'desc': progress.desc, 'progress_file': progress.file,
                        'student_name': student.user.name, 'student_text': detail.student_text,
                        'teacher_name': student.teacher.user.name, 'teacher_text': detail.teacher_text,
                        'student_file': detail.student_file, 'status': status}
            print(response)
            return JsonResponse(response)
    except Exception as e:
        response = {'msg': str(e)}
        print(response)
        return JsonResponse(response)


@login_required
def send_email_teacher(request):
    teacher_id = request.POST.get('teacher_id')
    student_name = request.POST.get('student_name')
    title = request.POST.get('title')
    try:
        teacher = User.objects.get(username=teacher_id).teacher
        send_mail('请及时批改毕设进度',teacher_desc(student_name, title), EMAIL_ADDRESS, [teacher.user.email], fail_silently=False)
        return HttpResponse('ok')
    except Exception as e:
        return HttpResponse(str(e))
    return 'ok'


def mkdir(path):
    path = path.strip()
    path = path.replace('\\', '/')
    path = path.rstrip('/')
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path.encode('utf-8').decode('utf-8'))
        print("创建成功"+path)


@login_required
def progress_file_download(request):

    uid = request.GET.get('id')
    print(uid)
    try:
        def file_iterator(path):
            size = 1024
            with open(path, "rb")as f:
                for data in iter(lambda: f.read(size), b''):
                    print(data)
                    yield data
        detail = ProgressDetail.objects.get(unique_id=uid)
        s_dir = 'templates/progress_file/' + str(detail.unique_id) + '_' + detail.title
        filename = os.path.join(s_dir, detail.file).replace('\\', '/')
        response = StreamingHttpResponse(file_iterator(filename))
        print(filename)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment;filename*=utf-8''{}".format(quote(detail.file))
        print(response)
        return response

    except Exception as e:
        return HttpResponse(str(e))


@login_required
def student_file_download(request):
    uid = request.GET.get('id')
    student_id = request.GET.get('student_id')
    print(uid, student_id)
    try:
        def file_iterator(path):
            size = 1024
            with open(path, "rb")as f:
                for data in iter(lambda: f.read(size), b''):
                    yield data
        detail = ProgressDetail.objects.get(unique_id=uid)
        student = User.objects.get(username=student_id).student
        progress = Progress.objects.get(detail=detail, student=student)
        s_dir = 'templates/student_file/' + str(detail.unique_id) + '_' + detail.title + '/' + student.user.username
        filename = os.path.join(s_dir, progress.student_file).replace('\\', '/')
        print(filename)
        response = StreamingHttpResponse(file_iterator(filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment;filename=" + progress.student_file
        return response
    except Exception as e:
        return HttpResponse(str(e))


@login_required
def create_many_student(request):
    assistant = request.user.assistant
    grade = assistant.grade
    print(grade)
    file = request.FILES.get('file', None)
    print(file)
    wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['file'].read())
    table = wb.sheets()[0]
    print(table)

    row = table.nrows
    res = []
    for i in range(1, row):
        col = table.row_values(i)
        print(col)
        try:
            id = str(int(col[0]))
            name = str(col[1])
            email = str(col[2])
            mobile = str(int(col[3]))
            type = col[4]
            if check_email(email) and check_mobile(mobile) and (type == 'U' or type == 'F'):
                user = User.objects.create_user(user_type='S',username=id, password=id,
                                           name=name,
                                           email=email,
                                           mobile=mobile)
                Student.objects.create(user=user, student_type=type, grade=grade)
                data = '留学生'
                if type == 'U':
                    data = '非留学生'
                res.append({'id': id, 'name': name, 'email': email, 'mobile': mobile, 'type': data})
        except Exception as e:
            return HttpResponse(json.dumps(res))
    return HttpResponse(json.dumps(res))


@login_required
def change_password(request):
    user = request.user
    old_pwd = request.POST.get('old_pwd')
    new_pwd = request.POST.get('new_pwd')
    if not all([old_pwd, new_pwd]):
        return HttpResponse('缺少参数')
    old_pwd = make_password(old_pwd)
    print(old_pwd)
    print(user.password)
    if old_pwd == user.password:
        user.password = new_pwd
        user.save()
        return HttpResponse('ok')
    else:
        return HttpResponse('密码错误')


@login_required
def create_many_teacher(request):
    file = request.FILES.get('file', None)
    print(file)
    wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['file'].read())
    table = wb.sheets()[0]
    print(table)

    row = table.nrows
    res = []
    for i in range(1, row):
        col = table.row_values(i)
        print(col)
        try:
            id = str(int(col[0]))
            name = str(col[1])
            email = str(col[2])
            mobile = str(int(col[3]))
            institute = str(col[4])
            info = str(col[5])
            if check_email(email) and check_mobile(mobile):
                user = User.objects.create_user(user_type='T', username=id, password=id, name=name, email=email,
                                                mobile=mobile)
                Teacher.objects.create(user=user, institute=institute, teacher_info=info)
                res.append({'id': id, 'name': name, 'email': email, 'mobile': mobile, 'institute': institute, 'info': info})
        except Exception as e:
            return HttpResponse(json.dumps(res))
    return HttpResponse(json.dumps(res))

















