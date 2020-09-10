from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('student_center/', student_center),
    path('teacher_center/', teacher_center),
    path('assistant_center/', assistant_center),
    path('student_center/choose_teacher/', S_Choice.as_view()),
    path('student_center/choose_queue/', confirm_list_s),
    path('student_center/S_finished/', s_progress_list_finished),
    path('student_center/S_unfinished/', s_progress_list_unfinished),
    path('student_center/S_P_detail/', S_Progress_Detail.as_view()),
    path('student_center/S_detail/', S_Detail.as_view()),
    path('teacher_center/choose_student/', T_Choice.as_view()),
    path('teacher_center/choose_queue/', confirm_list_t),
    path('teacher_center/T_finished/', t_progress_list_finished),
    path('teacher_center/T_unfinished/', t_progress_list_unfinished),
    path('teacher_center/T_detail/', T_Progress_Detail.as_view()),
    path('assistant_center/teacher_to_student/', student_list),
    path('assistant_center/create_progress/', create_progress),
    path('assistant_center/check_progress/', a_progress_list),
    path('assistant_center/progress_student/', a_plist_student_list),
    path('assistant_center/progress_student_detail/', progress_detail),
    path('student_detail/', student_detail)
]