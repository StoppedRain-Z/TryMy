<template>
  <div>
    <el-container>
      <el-aside style="width:20%">
        <el-menu :default-openeds="['1', '2','3']" router>
          <el-submenu index="1">
            <template slot="title"><i class="el-icon-message"></i>填报情况查看</template>
            <el-menu-item index="choose_student">未完成确认</el-menu-item>
            <el-menu-item index="choose_queue_T">已完成确认</el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>毕设进度查看</template>
            <el-menu-item index="T_unfinished">学生未提交</el-menu-item>
            <el-menu-item index="T_half">学生提交未批阅</el-menu-item>
            <el-menu-item index="T_finished">已完成批阅</el-menu-item>
          </el-submenu>
          <el-submenu index="3">
            <template slot="title"><i class="el-icon-menu"></i>我的</template>
            <el-menu-item index="teacher_message">我的信息</el-menu-item>
            <el-menu-item index="changePWD_T">修改密码</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

