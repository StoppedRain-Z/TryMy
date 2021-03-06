import VueRouter from 'vue-router'

import index from './components/Index'
import register from './components/register'
import login from './components/login'
import center from './components/center'
import changepwd from './components/changepwd'
import center_S from './components/student/center_S'
import center_A from './components/assistant/center_A'
import center_T from './components/teacher/center_T'
import student_center from './components/student/student_center'
import choose_teacher from './components/student/choose_teacher'
import choose_queue_S from './components/student/choose_queue'
import S_unfinished from './components/student/S_unfinished'
import S_finished from './components/student/S_finished'
import S_half from './components/student/S_half'
import student_message from './components/student/student_message'
import teacher_center from './components/teacher/teacher_center'
import choose_student from './components/teacher/choose_student'
import choose_queue_T from './components/teacher/choose_queue'
import T_unfinished from './components/teacher/T_unfinished'
import T_unfinished_detail from './components/teacher/T_unfinished_detail'
import T_finished from './components/teacher/T_finished'
import T_finished_detail from './components/teacher/T_finished_detail'
import teacher_message from './components/teacher/teacher_message'
import assistant_center from './components/assistant/assistant_center'
import create_progress from './components/assistant/create_progress'
import check_progress from './components/assistant/check_progress'
import teacher_to_student from './components/assistant/teacher_to_student'
import progress_student from './components/assistant/progress_student'
import progress_student_detail from './components/assistant/progress_student_detail'
import S_finish_detail from './components/student/S_finish_detail'
import S_unfinish_detail from './components/student/S_unfinish_detail'
import S_half_detail from './components/student/S_half_detail'
import T_half from './components/teacher/T_half'
import T_half_detail from './components/teacher/T_half_detail'
import T_S_selected from './components/assistant/T_S_selected'
import T_S_unselected from './components/assistant/T_S_unselected'
import add_student from './components/assistant/add_student'
import add_teacher from './components/assistant/add_teacher'

import store from './store'

var router = new VueRouter({
  routes: [
    {path: '/', component: index},
    {path: '/register', component: register},
    {path: '/login', component: login},
    {
      path: '/student_center',
      component: student_center,
      meta: {login: true},
      children: [
        {path: '', component: center_S, meta: {login: true}},
        {path: '/choose_teacher', component: choose_teacher, meta: {login: true}},
        {path: '/choose_queue_S', component: choose_queue_S, meta: {login: true}},
        {path: '/S_unfinished', component: S_unfinished, meta: {login: true}},
        {path: '/S_half', component: S_half, meta: {login: true}},
        {path: '/S_finished', component: S_finished, meta: {login: true}},
        {path: '/S_finish_detail', component: S_finish_detail, meta: {login: true}},
        {path: '/S_unfinish_detail', component: S_unfinish_detail, meta: {login: true}},
        {path: '/S_half_detail', component: S_half_detail, meta: {login: true}},
        {path: '/student_message', component: student_message, meta: {login: true}},
        {path: '/changePWD_S', component: changepwd, meta: {login: true}}
      ]
    },
    {
      path: '/teacher_center',
      component: teacher_center,
      meta: {login: true},
      children: [
        {path: '', component: center_T, meta: {login: true}},
        {path: '/choose_student', component: choose_student, meta: {login: true}},
        {path: '/choose_queue_T', component: choose_queue_T, meta: {login: true}},
        {path: '/T_unfinished', component: T_unfinished, meta: {login: true}},
        {path: '/T_finished', component: T_finished, meta: {login: true}},
        {path: '/T_half', component: T_half, meta: {login: true}},
        {path: '/T_half_detail', component: T_half_detail, meta: {login: true}},
        {path: '/T_finished_detail', component: T_finished_detail, meta: {login: true}},
        {path: '/T_unfinished_detail', component: T_unfinished_detail, meta: {login: true}},
        {path: '/teacher_message', component: teacher_message, meta: {login: true}},
        {path: '/changePWD_T', component: changepwd, meta: {login: true}}
      ]
    },
    {
      path: '/assistant_center',
      component: assistant_center,
      meta: {login: true},
      children: [
        {path: '', component: center_A, meta: {login: true}},
        {path: '/create_progress', component: create_progress, meta: {login: true}},
        {path: '/check_progress', component: check_progress, meta: {login: true}},
        {path: '/teacher_to_student', component: teacher_to_student, meta: {login: true}},
        {path: '/progress_student', component: progress_student, meta: {login: true}},
        {path: '/progress_student_detail', component: progress_student_detail, meta: {login: true}},
        {path: '/T_S_selected', component: T_S_selected, meta: {login: true}},
        {path: '/T_S_unselected', component: T_S_unselected, meta: {login: true}},
        {path: '/add_student', component: add_student, meta: {login: true}},
        {path: '/add_teacher', component: add_teacher, meta: {login: true}}
      ]
    }
  ]
})


export default router
