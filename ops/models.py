from django.db import models
from users.models import *
# Create your models here.


class Choose(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    CHOICES = (
        (1, 'unconfirmed'),  # 未确认
        (2, 'confirmed'),    # 已确认
        (3, 'confused'),     # 拒绝
    )
    teacher_choice = models.PositiveSmallIntegerField(verbose_name="教师选择", choices=CHOICES, default=1)
    student_choice = models.PositiveSmallIntegerField(verbose_name="学生选择", choices=CHOICES, default=1)


class Progress(models.Model):
    title = models.CharField(max_length=256, default='')
    desc = models.TextField(default='')
    start_time = models.DateField()
    end_time = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_text = models.TextField(default='')
    teacher_text = models.TextField(default='')
