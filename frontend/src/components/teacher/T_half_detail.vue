<template>
  <div>
    <el-container>
      <el-main>
        <el-form :model="detail_message" ref="form" :rules="rules" label-width="100px" class="demo-form"
            cell-style="font-weight: 700;">
            <el-form-item label="进度名称">{{detail_message.title}}</el-form-item>
            <el-form-item label="进度相关文件">
              <div>{{detail_message.progress_file}}</div>
              <el-button type="primary" @click="download_progress_file" v-show="progress_show">下载文件</el-button>
            </el-form-item>
            <el-form-item label="详细描述">{{detail_message.desc}}</el-form-item>
            <el-form-item label="开始时间">{{detail_message.start_time}}</el-form-item>
            <el-form-item label="结束时间">{{detail_message.end_time}}</el-form-item>
            <el-form-item label="学生姓名">{{detail_message.student_name}}</el-form-item>
            <el-form-item label="学生反馈">{{detail_message.student_text}}</el-form-item>
            <el-form-item label="学生作业文件">
              <div>{{detail_message.student_file}}</div>
              <el-button  type="primary" @click="download_student_file" v-show="student_show">下载文件</el-button>
            </el-form-item>
            <el-form-item label="教师反馈">
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
      progress_show: true,
      student_show: true,
      detail_message: {},
      progress_file: '',
      student_file: '',
      resply: []
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
          if (this.detail_message.progress_file === '') {
            this.detail_message.progress_file = '无相关文件'
            this.progress_show = false
          }
          if (this.detail_message.student_file === '') {
            this.detail_message.student_file = '无相关文件'
            this.student_show = false
          }
          this.progress_file = this.detail_message.progress_file
          this.student_file = this.detail_message.student_file
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
    },
    download_progress_file () {
      var formdata = new window.FormData()
      formdata.append('id', this.id)
      this.$http
        .post('progress_file_download/', formdata, {headers: {
          'Content-Type': 'multipart/form-data'}})
        .then(result => {
          console.log(result.data)
          const blob = new Blob([result.body])
          if (window.navigator.msSaveOrOpenBlob) {
            navigator.msSaveBlob(blob, this.progress_file)
          } else {
            let aTag = document.createElement('a')
            aTag.download = this.progress_file
            aTag.href = URL.createObjectURL(blob)
            aTag.click()
            URL.revokeObjectURL(aTag.href)
          }
        })
    },
    download_student_file () {
      var formdata = new window.FormData()
      formdata.append('id', this.id)
      formdata.append('student_id', this.student_id)
      console.log(formdata)
      this.$http
        .post('student_file_download/', formdata, {headers: {
          'Content-Type': 'multipart/form-data'}}, {responseType: 'blob'})
        .then(result => {
          console.log(result.data)
          const blob = new Blob([result.data])
          if (window.navigator.msSaveOrOpenBlob) {
            navigator.msSaveBlob(blob, this.student_file)
          } else {
            let aTag = document.createElement('a')
            aTag.download = this.student_file
            console.log(this.student_file)
            console.log(this.detail_message.student_file)
            aTag.href = URL.createObjectURL(blob)
            aTag.click()
            URL.revokeObjectURL(aTag.href)
          }
        })
    }
  },
  created () {
    this.getData()
  }
}
</script>
