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
            <el-form-item label="进度提交">{{detail_message.student_text}}</el-form-item>
            <el-form-item label="教师反馈">{{detail_message.teacher_text}}</el-form-item>
        </el-form>
        <router-link :to="{path:'/S_finished'}">
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
            detail_message: {}
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
        }
    },
    created() {
        this.getData()
    }
}
</script>