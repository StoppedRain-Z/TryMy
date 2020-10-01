<template>
  <div>
    <el-container>
      <el-main>
        <el-form :model="formData" ref="form" :rules="rules" label-width="100px" class="demo-form">
          <el-form-item label="进度名称" prop="title">
            <el-input v-model="formData.title"></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="desc">
            <el-input type="textarea" v-model="formData.desc"></el-input>
          </el-form-item>
          <el-form-item label="相关说明">
            <input style="width: 260px" type="file" id="uploadfile" 
              ref= "pathClear" @change="getFile($event)"></input>
            <span>仅支持扩展名为.doc .docx .pdf的文件</span>
          </el-form-item>
          <el-form-item label="开始时间" required>
            <el-col :span="11">
              <el-form-item prop="start_time">
                <el-date-picker
                  type="datetime"
                  placeholder="选择日期"
                  v-model="formData.start_time"
                  style="width: 100%;">
                </el-date-picker>
              </el-form-item>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="11">
              <el-form-item prop="end_time">
                <el-date-picker
                  type="datetime"
                  placeholder="选择日期"
                  v-model="formData.end_time"
                  style="width: 100%;"
                  @change="timeChange">
                </el-date-picker>
              </el-form-item>
            </el-col>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submit('form')">创建进度，并发送邮件</el-button>
            <el-button @click="reset()">重置</el-button>
          </el-form-item>
        </el-form>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  inject: ['reload'],
  data () {
    return {
      formData: {
        'title' :'',
        'desc': '',
        'start_time' : '',
        'end_time': '',
        'file': ''
      },
      rules: {
        title: [{required: true, message: '请输入进度名称', trigger: 'blur'}],
        desc: [{required: true, message: '请输入具体描述', trigger: 'blur'}],
        start_time: [{type: 'date', required: true, message: '请选择日期', trigger: 'change'}],
        end_time: [{type: 'date', required: true, message: '请选择日期', trigger: 'change'}]
      }
    }
  },
  methods: {
    submit (myform) {
      console.log(this.formData.start_time)
      let str1 = this.dateToString(this.formData.start_time)
      console.log(str1)
      let str2 = this.dateToString(this.formData.end_time)
      var array = new window.FormData()
      array.append('title', this.formData.title)
      array.append('desc', this.formData.desc)
      array.append('start_time', str1)
      array.append('end_time', str2)
      if(this.formData.file !== undefined){
        array.append('file', this.formData.file)
      }
      console.log(array)
      this.$http
        .post('assistant_center/create_progress/', array, {
           headers:{
                    'Content-Type': 'multipart/form-data'
                }
        })
        .then(result => {
          console.log(result.body)
          if (result.body === 'ok') {
            alert("该任务发布成功")
            this.reset()
          } else {
            alert(result.body)
          }
        })
    },
    dateToString(date){
      var year = date.getFullYear();
      var month = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1
      var day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate()
      var hours = date.getHours() < 10 ? '0' + date.getHours() : date.getHours()
      var minutes = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()
      var seconds = date.getSeconds() < 10 ? '0'+date.getSeconds() : date.getSeconds()
      return year + '-' + month + '-'+day+"-"+hours+"-"+minutes+"-"+seconds
    },
    reset() {
      //this.formData = {}
      this.reload()
    },
    getFile(event) {
        var file = event.target.files[0]
        console.log(event.target.files)
        console.log(file.type)
        var index = file.name.lastIndexOf(".")
        var type = file.name.substr(index+1)
        if(type !== "doc" && type !== "docx" && type !== "pdf"){
          this.$refs.pathClear.value = ''
          //var obj = document.getElementById('uploadfile')
          //obj.select();
          //document.selection.clear();
          alert("不支持该文件类型")
          return 
        }
        this.formData.file = event.target.files[0]
        console.log(this.formData.file)
    },
    timeChange(time){
      console.log(time)
      if(time.length && time[0] && time[1]){
        if(parseTime(this.formData.end_time) === '00:00:00'){
          this.formData.end_time = new Date(parseTime(time[1], '{y}-{m}-{d}'+'23:59:59'))
        }
      }
    }
  },
  created() {
    console.log(this.formData.file)
  }
}
</script>
