from django.db import models
from users.models import *
# Create your models here.


class Choose(models.Model):
    grade = models.IntegerField(default=2020)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    CHOICES = (
        (1, 'unconfirmed'),  # 未确认
        (2, 'confirmed'),    # 已确认
        (3, 'confused'),     # 拒绝
        (4, 'cancelled'),    # 取消
    )
    teacher_choice = models.PositiveSmallIntegerField(verbose_name="教师选择", choices=CHOICES, default=1)
    student_choice = models.PositiveSmallIntegerField(verbose_name="学生选择", choices=CHOICES, default=1)


class ProgressDetail(models.Model):
    unique_id = models.IntegerField(unique=True, default=1)
    title = models.CharField(max_length=256, default='')
    desc = models.TextField(default='')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    file = models.CharField(max_length=128, default='')
    grade = models.IntegerField(default=2020)


class Progress(models.Model):
    CHOICES = (
        (4, 'unchecked'),
        (1, 'overfinished'),
        (2, 'finished'),
        (3, 'unfinished'),
    )
    detail = models.ForeignKey(ProgressDetail, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    student_text = models.TextField(default='')
    teacher_text = models.TextField(default='')
    student_ok = models.BooleanField(default=False)
    teacher_ok = models.BooleanField(default=False)
    student_file = models.CharField(max_length=128, default='')
    status = models.PositiveSmallIntegerField(choices=CHOICES, default=4)


