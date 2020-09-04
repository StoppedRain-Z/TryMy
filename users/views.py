from django.shortcuts import render
from django.shortcuts import redirect, reverse, HttpResponseRedirect
# Create your views here.
from django.contrib.auth import login, authenticate, logout
from .models import *
from django.views import View
from django.http import JsonResponse


class RegisterView(View):
    """
    用户注册接口
    """
    @staticmethod
    def get(request):
        print("visit register")
        return render(request, 'register')

    @staticmethod
    def post(request):
        print("post register")
        data = request.POST
        user_type = data.get('user_type')
        cardID = data.get('cardID')
        name = data.get('name')
        password = data.get('password')
        email = data.get('email')
        mobile = data.get('mobile')
        print(user_type, cardID, name, password, email, mobile)
        response = {}
        if not all([cardID, name, password, email, mobile]):
            response['msg'] = "缺少注册信息"
            return JsonResponse(response)
        try:
            user = User.objects.create_user(user_type=user_type, username=cardID, name=name, password=password, email=email, mobile=mobile)
            if user_type == 'S':
                print('create student')
                grade = data.get('grade')
                Student.objects.create(user=user, grade=grade)
            elif user_type == 'T':
                print('create teacher')
                teacher_info = data.get('teacher_info')
                institute = data.get('institute')
                Teacher.objects.create(user=user, teacher_info=teacher_info, institute=institute)
            elif user_type == 'A':
                print('create assistant')
                grade = data.get('grade')
                Assistant.objects.create(user=user, grade=grade)
            response['msg'] = 'ok'
            return JsonResponse(response)
        except Exception as e:
            print(e)
            response['msg'] = str(e)
            return JsonResponse(response)


class LoginView(View):
    @staticmethod
    def get(request):
        return render(request, 'login.html')

    @staticmethod
    def post(request):
        response = {}
        data = request.POST
        cardID = data.get('cardID')
        password = data.get('password')
        print(cardID, password)
        if not all([cardID, password]):
            response['msg'] = '缺少请求参数'
            return JsonResponse(response)

        user = authenticate(username=cardID, password=password)
        if user is None:
            response['msg'] = '用户名或密码错误'
            return JsonResponse(response)
        login(request, user)
        response['msg'] = 'ok'
        if user.user_type == 'S':
            response['user_type'] = 'S'
        elif user.user_type == 'T':
            response['user_type'] = 'T'
        elif user.user_type == 'A':
            response['user_type'] = 'A'
        return JsonResponse(response)


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))