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

            <el-form-item label="进度提交">
                <el-input v-model="detail_message.student_text" type="textarea"></el-input>
            </el-form-item>

            <el-form-item label="上传文件">
                <input style="width: 260px" type="file" 
                  ref= "pathClear" @change="getFile($event)"></input>
            </el-form-item>

        </el-form>
        <el-button type="primary" @click="commit" v-show="isshow">提交</el-button>
        <router-link :to="{path:'/S_unfinished'}">
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
      id:0,
      status:'',
      progress_show: true,
      progress_file: '',
      detail_message: {},
      resply: [],
      isshow: true
    }
  },
  methods: {
    getData () {
      this.id = this.$route.query.id
      this.status = this.$route.query.status
      if (this.status === '已失效') {
        this.isshow = false
      }
      var array = {
        'id': this.id
      }
      console.log(array)
      this.$http
        .get('student_center/S_P_detail/', {params: array})
        .then(result => {
          this.detail_message = result.body
          console.log(result.body)
          if (this.detail_message.progress_file === '') {
            this.detail_message.progress_file = '无相关文件'
            this.progress_show = false
          }
          this.progress_file = this.detail_message.progress_file
          if (this.detail_message.msg !== 'ok') {
            alert(this.detail_message.msg)
          }
        })
    },
    commit () {
      var formData = new window.FormData();
      formData.append('id',this.id)
      formData.append('student_text', this.detail_message.student_text)
      formData.append('file',this.detail_message.file)
      console.log(formData.get('file'))
      this.$http
        .post('student_center/S_P_detail/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(result => {
          if (result.body === 'ok') {
            alert('提交成功')
            this.$router.push({path: '/S_unfinished'})
          } else {
            alert(result.body)
          }
        })
    },
    getFile (event) {
      var file = event.target.files[0]
      var index = file.name.lastIndexOf(".")
      var type = file.name.substr(index+1)
      if(type !== "doc" && type !== "docx" && type !== "pdf"){
          this.$refs.pathClear.value = ''
          alert("不支持该文件类型")
          return 
      }
      this.detail_message.file = event.target.files[0]
    },
    download_progress_file () {
      var array = {
        'id': this.id
      }
      this.$axios({
        method: 'GET',
        url: 'progress_file_download/',
        params: array,
        responseType: 'blob'
      }).then(res => {
        console.log(res)
        let blob = new Blob([res.data], {type: 'application/octet-stream'})
        console.log('//////////////////')
        if (window.navigator.msSaveOrOpenBlob) {
          navigator.msSaveBlob(blob, this.progress_file)
        } else {
          let aTag = document.createElement('a')
          aTag.download = this.student_file
          console.log(this.student_file)
          console.log(this.detail_message.progress_file)
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
