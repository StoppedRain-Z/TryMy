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
            <el-form-item label="进度提交" v-show = "unchangeshow">
                {{detail_message.student_text}} 
            </el-form-item>
            <el-form-item label="上传文件">
              <div>{{detail_message.student_file}}</div>
              <el-button type="primary" @click="download_student_file" v-show="student_show">下载文件</el-button>
            </el-form-item>


            <el-form-item label="进度提交" v-show = "changeshow">
                <el-input v-model="detail_message.student_text" type="textarea"></el-input>
            </el-form-item>
            <el-form-item label="上传文件" v-show = "changeshow">
                <input style="width: 260px" type="file" @change="getFile($event)"></input>
            </el-form-item>

            <el-form-item label="教师反馈">{{detail_message.teacher_text}}</el-form-item>
        </el-form>
        <el-button  type="primary" @click="text_change" v-show="unchangeshow">修改</el-button>
        <el-button type="primary" @click="commit" v-show="changeshow">提交</el-button>
        <router-link :to="{path:'/S_half'}">
        <el-button  type="primary">返回</el-button>
        </router-link>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
    inject: ['reload'],
    data() {
        return {
            id:0,
            status:'',
            detail_message: {},
            resply: [],
            unchangeshow: true,
            changeshow: false,
            progress_show: true,
            progress_file: ''
        }
    },
    methods: {
        getData() {
            this.id = this.$route.query.id
            this.status = this.$route.query.status
            var array = {
                "id": this.id
            }
            console.log(array)
            this.$http
                .get('student_center/S_P_detail/', {params: array})
                .then(result => {
                    this.detail_message = result.body
                    console.log(result.body)
                    if(this.detail_message.msg !== 'ok'){
                        alert(this.detail_message.msg)
                    }
                })
        },
        text_change() {
            this.unchangeshow = false
            this.changeshow = true
        },
        commit() {
            var array = {
                "id": this.id,
                "student_text": this.detail_message.student_text
            }
            var formData = new window.FormData();
            formData.append('id',this.id)
            formData.append('student_text', this.detail_message.student_text)
            formData.append('file',this.detail_message.file)
            console.log(formData.get('file'))
            this.$http
                .post('student_center/S_P_detail/', formData, {
                    headers:{
                    'Content-Type': 'multipart/form-data'
                }
                })
                .then(result => {
                    if(result.body === 'ok'){
                        alert('提交成功')
                        this.reload
                    }else{
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
        formdata.append('student_id', this.detail_message.student_id)
        this.$http
            .post('student_file_download/', formdata, {headers: {
            'Content-Type': 'multipart/form-data'}})
            .then(result => {
            console.log(result.data)
            const blob = new Blob([result.body])
            if (window.navigator.msSaveOrOpenBlob) {
                navigator.msSaveBlob(blob, this.student_file)
            } else {
                let aTag = document.createElement('a')
                aTag.download = this.student_file
                aTag.href = URL.createObjectURL(blob)
                aTag.click()
                URL.revokeObjectURL(aTag.href)
            }
            })
        }
    },
    created() {
        this.getData()
    }
}
</script>