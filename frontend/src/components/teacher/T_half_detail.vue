<template>
  <div>
    <el-container>
      <el-main>
        <el-form :model="detail_message" ref="form" :rules="rules" label-width="100px" class="demo-form"
            cell-style="font-weight: 700;">
            <el-form-item label="进度名称">{{detail_message.title}}</el-form-item>
            <el-form-item label="详细描述">{{detail_message.desc}}</el-form-item>
            <el-form-item label="开始时间">{{detail_message.start_time}}</el-form-item>
            <el-form-item label="结束时间">{{detail_message.end_time}}</el-form-item>
            <el-form-item label="学生姓名">{{detail_message.student_name}}</el-form-item>
            <el-form-item label="学生提交">{{detail_message.student_text}}</el-form-item>
            <el-form-item label="教师反馈提交">
                <el-input v-model="detail_message.teacher_text" type="textarea"></el-input>
            </el-form-item>

        </el-form>
        <el-button type="primary" @click="commit">提交</el-button>
        <router-link :to="{path:'/T_half'}">
        <el-button  type="primary">返回</el-button>
        </router-link>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      id: 0,
      student_id: '',
      detail_message: {},
      resply: [],
    }
  },
  methods: {
    getData () {
      this.id = this.$route.query.id
      this.student_id = this.$route.query.student_id
      var array = {
        'id': this.id,
        'student_id': this.student_id,
      }
      console.log(array)
      this.$http
        .get('teacher_center/T_detail/', {params: array})
        .then(result => {
          this.detail_message = result.body
          console.log(result.body)
          if (this.detail_message.msg !== 'ok') {
            alert(this.detail_message.msg)
          }
        })
    },
    commit () {
      var array = {
        'id': this.id,
        'teacher_text': this.detail_message.teacher_text,
        'student_id': this.student_id
      }
      this.$http
        .post('teacher_center/T_detail/', array)
        .then(result => {
          if (result.body === 'ok') {
            alert('提交成功')
            this.$router.push({path: '/T_half'})
          } else {
            alert(result.body)
          }
        })
    }
  },
  created () {
    this.getData()
  }
}
</script>
