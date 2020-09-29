<template>
  <div>
    <el-container>
      <el-aside width="200px">
        <el-menu :default-openeds="['1','2']" router>
          <el-submenu index="1">
            <template slot="title"><i class="el-icon-menu"></i>毕设进度</template>
            <el-menu-item index="create_progress">创建进度</el-menu-item>
            <el-menu-item index="check_progress">查看进度</el-menu-item>
            <el-menu-item index="teacher_to_student">导师与学生对应关系</el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title"><i class="el-icon-menu"></i>导师与学生对应关系</template>
            <el-menu-item index="create_progress">已对应</el-menu-item>
            <el-menu-item index="check_progress">未对应</el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view/>
      </el-main>
    </el-container>
  </div>
</template>

