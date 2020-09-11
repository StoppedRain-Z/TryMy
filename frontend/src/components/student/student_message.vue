<template>
  <div>
    <el-container>
      <el-main>
        <el-form :model="detail_message" ref="form" :rules="rules" label-width="100px" class="demo-form"
            cell-style="font-weight: 700;">
            <el-form-item label="姓名">{{detail_message.student_name}}</el-form-item>
            <el-form-item label="学号">{{detail_message.student_id}}</el-form-item>
            <el-form-item label="邮箱">{{detail_message.email}}</el-form-item>
            <el-form-item label="联系电话">{{detail_message.mobile}}</el-form-item>
            <el-form-item label="身份">{{detail_message.student_type}}</el-form-item>
            <el-form-item label="指导教师">{{detail_message.teacher}}</el-form-item>
        </el-form>
        <el-form>
            <el-button @click="logout" type="primary">登出</el-button>
        </el-form>
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
                .get('student_center/S_detail/', {params: array})
                .then(result => {
                    this.detail_message = result.body
                    console.log(result.body)
                    if(this.detail_message.msg !== 'ok'){
                        alert(this.detail_message.msg)
                    }
                    if(this.detail_message.student_type === 'U'){
                        this.detail_message.student_type = '非留学生'
                    }else{
                        this.detail_message.student_type = '留学生'
                    }
                })
        },
        logout() {
            console.log('1')
            this.$http
                .get('logout/')
                .then(result => {
                    console.log('2')
                    this.$router.push({path:'/login'})
                })
        }
    },
    created() {
        this.getData()
    }
}
</script>