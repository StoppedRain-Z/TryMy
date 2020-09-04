from django.shortcuts import render, redirect, reverse
from django.views import View
from .models import *
from django.http import JsonResponse,HttpResponse,HttpResponseBadRequest
import json
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
    def get(self):
        teacher_list = Teacher.objects.all()
        json_list = []
        for teacher in teacher_list:
            json_item = {"teacher_name": teacher.user.name,
                         "teacher_institute": teacher.institute,
                         "teacher_info": teacher.teacher_info}

            json_list.append(json_item)
        print(json_list)
        # return render("student_choose.html", json.dumps(json_list))
        return JsonResponse(json.dumps(json_list), safe=False)
    
    def post(self):
        data = self.request.POST
        teacher_list = data.get['teacher_list']
        user = self.request.user
        student = Student.objects.get(user=user)
        for teacher in teacher_list:
            t = Teacher.objects.get(cardID=teacher)
            Choose.objects.create(student=student,teacher=t,teacher_choice=1,student_choice=2)
        return HttpResponse('ok')


class T_Choice(View):
    @staticmethod
    def get(self):
        student_list = Student.objects.all()
        json_list = []
        for student in student_list:
            json_item = {"cardID": student.user.username, "name": student.user.name}

            json_list.append(json_item)
        print(json_list)
        # return render("student_choose.html", json.dumps(json_list))
        return JsonResponse(json.dumps(json_list), safe=False)

    def post(self):
        data = self.request.POST
        student_list = data.get['student_list']
        user = self.request.user
        teacher = Teacher.objects.get(user=user)
        for student in student_list:
            s = Student.objects.get(cardID=student)
            Choose.objects.create(student=s, teacher=teacher, teacher_choice=2, student_choice=1)
        return HttpResponse('ok')


def confirm_list_s(request, student_choice):
    user = request.user
    student = Student.objects.get(user=user)
    choose_list = Choose.objects.filter(student=student, student_choice=student_choice)
    json_list = []
    for choose in choose_list:
        json_item = {"name": choose.teacher.user.name, "teacher_info": choose.teacher.teacher_info}
        json_list.append(json_item)
    return HttpResponse(json.dumps(json_list))


def confirm_list_t(request, teacher_choice):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    choose_list = Choose.objects.filter(teacher=teacher, teacher_choice=teacher_choice)
    json_list = []
    for choose in choose_list:
        json_item = {"name": choose.student.user.name, "cardID": choose.student.user.username}
        json_list.append(json_item)
    return HttpResponse(json.dumps(json_list))


def op_t(request, teacher_choice):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    card_id = request.POST.get('cardID')
    usr = User.objects.get(cardID=card_id)
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
    card_id = request.POST.get('cardID')
    usr = User.objects.get(cardID=card_id)
    teacher = Teacher.objects.get(user=usr)
    choose = Choose.objects.get(teacher=teacher, student=student)
    choose.student_choice = student_choice
    choose.save()
    if choose.student_choice == 2 and choose.teacher_choice == 2:
        student.teacher = teacher
        student.save()
    return HttpResponse("ok")


def create_progress(request):
    data = request.POST
    title = data.get('title')
    desc = data.get('desc')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    student_list = Student.objects.all()
    response = {}
    email_list = []
    for student in student_list:
        try:
            progress = Progress.objects.create(student=student, title=title, desc=desc)
            email_list.append(student.user.email)
        except Exception as e:
            print(e)
            response['msg'] = e
            return JsonResponse(response)
    print('send email start')
    # send_mail(title, desc, 'zhangrt20@126.com', email_list, fail_silently=False)
    print('send email end')













