import VueRouter from 'vue-router'

import index from './components/Index'
import register from './components/register'
import login from './components/login'
import center from './components/center'
import student_center from './components/student/student_center'
import choose_teacher from './components/student/choose_teacher'
import choose_queue_S from './components/student/choose_queue'
import S_unfinished from './components/student/S_unfinished'
import S_finished from './components/student/S_finished'
import S_isfinished from './components/student/S_isfinished'
import teacher_center from './components/teacher/teacher_center'
import choose_student from './components/teacher/choose_student'
import choose_queue_T from './components/teacher/choose_queue'
import T_unfinished from './components/teacher/T_unfinished'
import T_finished from './components/teacher/T_finished'
import assistant_center from './components/assistant/assistant_center'
import create_progress from './components/assistant/create_progress'
import check_progress from './components/assistant/check_progress'
import teacher_to_student from './components/assistant/teacher_to_student'
import progress_student from './components/assistant/progress_student'
import progress_student_detail from './components/assistant/progress_student_detail'

var router = new VueRouter({
  routes: [
    {path: '/', component: index},
    {path: '/register', component: register},
    {path: '/login', component: login},
    {
      path: '/student_center',
      component: student_center,
      children: [
        {path: '', component: center},
        {path: '/choose_teacher', component: choose_teacher},
        {path: '/choose_queue_S', component: choose_queue_S},
        {path: '/S_unfinished', component: S_unfinished},
        {path: '/S_isfinished', component: S_isfinished},
        {path: '/S_finished', component: S_finished}
      ]
    },
    {
      path: '/teacher_center',
      component: teacher_center,
      children: [
        {path: '', component: center},
        {path: '/choose_student', component: choose_student},
        {path: '/choose_queue_T', component: choose_queue_T},
        {path: '/T_unfinished', component: T_unfinished},
        {path: '/T_finished', component: T_finished}
      ]
    },
    {
      path: '/assistant_center',
      component: assistant_center,
      children: [
        {path: '', component: center},
        {path: '/create_progress', component: create_progress},
        {path: '/check_progress', component: check_progress},
        {path: '/teacher_to_student', component: teacher_to_student},
        {path: '/progress_student', component: progress_student},
        {path: '/progress_student_detail', component: progress_student_detail}
      ]
    }
  ]
})
export default router
