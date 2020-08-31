<template>
  <div>
    <el-container>
      <el-aside width="200px">
        <el-menu :default-openeds="['1', '2']" router>
          <el-submenu index="1">
            <template slot="title"><i class="el-icon-message"></i>志愿填报</template>
            <el-menu-item index="choose_student">志愿填报</el-menu-item>
            <el-menu-item index="choose_queue_T">已选志愿</el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>毕设进度</template>
            <el-menu-item index="T_unfinished">未完成</el-menu-item>
            <el-menu-item index="T_finished">已完成</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

