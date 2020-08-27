from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):

    USER_TYPE_CHOICES = (
        ('S','student'),         #毕设学生
        ('T','teacher'),         #毕设导师
        ('A','assistant'),       #辅导员
        #(4,'supervisor'),      #管理员
    )


    user_type = models.CharField(max_length=1,verbose_name="用户类型",choices=USER_TYPE_CHOICES)
    username = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=128)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=11,unique=True)    

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    institute = models.CharField(max_length=128,default='')
    teacher_info = models.URLField(verbose_name="个人主页",max_length=128,default='')

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING,null=True,blank=True)
    grade = models.CharField(max_length=4)


class Assistant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    grade = models.CharField(max_length=4)