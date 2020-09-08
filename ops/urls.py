from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('student_center/', student_center),
    path('teacher_center/', teacher_center),
    path('assistant_center/', assistant_center),
    path('student_center/choose_teacher/', S_Choice.as_view()),
    path('student_center/choose_queue', confirm_list_s)
]