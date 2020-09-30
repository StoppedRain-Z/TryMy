<template>
  <div>
    <el-container>
      <el-aside style="width:20%">
        <el-menu :default-openeds="['1','2','3']" router>
          <el-submenu index="1">
            <template slot="title"><i class="el-icon-message"></i>志愿填报</template>
            <el-menu-item index="choose_teacher">志愿填报</el-menu-item>
            <el-menu-item index="choose_queue_S">已选志愿</el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>毕设进度</template>
            <el-menu-item index="S_unfinished">未提交</el-menu-item>
            <el-menu-item index="S_half">已提交未批改</el-menu-item>
            <el-menu-item index="S_finished">已批改</el-menu-item>
          </el-submenu>
          <el-submenu index="3">
            <template slot="title"><i class="el-icon-menu"></i>我的</template>
            <el-menu-item index="student_message">我的信息</el-menu-item>
            <el-menu-item index="changePWD_S">修改密码</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

