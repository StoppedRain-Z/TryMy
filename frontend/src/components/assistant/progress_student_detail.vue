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
            <el-form-item label="学生姓名">{{detail_message.student_name}}</el-form-item>
            <el-form-item label="学生反馈">{{detail_message.student_text}}</el-form-item>
            <el-form-item label="学生作业文件">
              <div>{{detail_message.student_file}}</div>
              <el-button  type="primary" @click="download_student_file" v-show="student_show">下载文件</el-button>
            </el-form-item>
            <el-form-item label="指导教师">{{detail_message.teacher_name}}</el-form-item>
            <el-form-item label="完成情况">{{detail_message.status}}</el-form-item>
            <el-form-item label="教师评价">{{detail_message.teacher_text}}</el-form-item>
        </el-form>
        <router-link :to="{path:'/progress_student', query:{id:this.id}}">
        <el-button  type="primary">返回</el-button>
        </router-link>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
    data() {
        return {
            id:0,
            student_id:'',
            progress_show: true,
            student_show: true,
            detail_message: {
                "msg":'ok',
                "title":'test1',
                "desc":'fsdfsrgsg',
                "student_name":'我是13',
                "student_text":'写完啦发送你的反馈哈uofosadfigroafhoaagidfgoSDHFOHAOIFHOERYFOADFLHIAT大圣轮回覅两个红歌会偶尔螯合钙foe和欧弟发红奥后负荷org哈佛涩会人托哈佛点过后和然后给和投入和青奥刚好我过后确认过人后各个',
                "teacher_name":'我是a',
                "teacher_text":'可'
            }
        }
    },
    methods: {
        getData() {
            this.id = this.$route.query.id
            this.student_id = this.$route.query.student_id
            var array = {
                "id": this.id,
                "student_id": this.student_id
            }
            console.log(array)
            this.$http
                .get('assistant_center/progress_student_detail/', {params: array})
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
                    if(this.detail_message.msg !== 'ok'){
                        alert(this.detail_message.msg)
                    }
                })
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
                navigator.msSaveBlob(blob, this.detail_message.progress_file)
                } else {
                let aTag = document.createElement('a')
                aTag.download = this.detail_message.progress_file
                console.log(this.detail_message.progress_file)
                aTag.href = URL.createObjectURL(blob)
                aTag.click()
                URL.revokeObjectURL(aTag.href)
                }
            })
        },
        download_student_file () {
            var array = {
                'id': this.id,
                'student_id': this.student_id
            }
            this.$axios({
                method: 'GET',
                url: 'student_file_download/',
                params: array,
                responseType: 'blob'
            }).then(res => {
                console.log(res)
                let blob = new Blob([res.data], {type: 'application/octet-stream'})
                if (window.navigator.msSaveOrOpenBlob) {
                navigator.msSaveBlob(blob, this.detail_message.student_file)
                } else {
                let aTag = document.createElement('a')
                aTag.download = this.detail_message.student_file
                console.log(this.detail_message.student_file)
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