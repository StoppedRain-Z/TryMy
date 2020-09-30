from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', index),
    path('student_center/', student_center),
    path('teacher_center/', teacher_center),
    path('assistant_center/', assistant_center),
    path('student_center/choose_teacher/', login_required(S_Choice.as_view())),  # 学生填报志愿
    path('student_center/choose_queue/', confirm_list_s),    # 学生已选志愿列表
    path('student_center/S_finished/', s_progress_list_finished),  # 学生已批改列表
    path('student_center/S_half/', s_half),                         # 学生已完成未批改列表
    path('student_center/S_unfinished/', s_progress_list_unfinished),  # 学生未完成progress列表
    path('student_center/S_P_detail/', login_required(S_Progress_Detail.as_view())),  # 学生Progress详情，post可修改
    path('student_center/S_detail/', login_required(S_Detail.as_view())),   # 学生个人信息，学生个人查看修改
    path('teacher_center/T_message/',login_required(T_Detail.as_view())),
    path('teacher_center/choose_student/', login_required(T_Choice.as_view())),
    path('teacher_center/choose_queue/', confirm_list_t),
    path('teacher_center/T_finished/', t_progress_list_finished),
    path('teacher_center/T_half/', t_half),
    path('teacher_center/T_unfinished/', t_progress_list_unfinished),
    path('teacher_center/T_detail/', login_required(T_Progress_Detail.as_view())),
    path('assistant_center/teacher_to_student_selected/', student_list),
    path('assistant_center/teacher_to_student_unselected/', student_list_not_selected),
    path('assistant_center/create_progress/', create_progress),
    path('assistant_center/check_progress/', a_progress_list),
    path('assistant_center/progress_student/', a_plist_student_list),
    path('assistant_center/progress_student_detail/', progress_detail),
    path('student_detail/', student_detail),   # 学生个人信息，导师和辅导员查看
    path('student_file_download/', student_file_download),
    path('progress_file_download/', progress_file_download),
    path('send_mail_teacher/', send_email_teacher),
    path('assistant_center/create_many_student/', create_many_student),
    path('assistant_center/create_many_teacher/', create_many_teacher),
    path('change_password/', change_password),
    path('student_center/cancel_choose/', cancel_choose)
]