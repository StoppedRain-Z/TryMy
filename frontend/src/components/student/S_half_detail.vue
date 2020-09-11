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
            <el-form-item label="进度提交" v-show = "unchangeshow">
                {{detail_message.student_text}} 
            </el-form-item>
            <el-form-item label="进度提交" v-show = "changeshow">
                <el-input v-model="detail_message.student_text" type="textarea"></el-input>
            </el-form-item>
            <el-form-item>
            <el-button  type="primary" @click="text_change">修改</el-button>
            </el-form-item>
            <el-form-item label="教师反馈">{{detail_message.teacher_text}}</el-form-item>
        </el-form>
        <el-button type="primary" @click="commit">提交</el-button>
        <router-link :to="{path:'/S_half'}">
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
            status:'',
            detail_message: {},
            resply: [],
            unchangeshow: true,
            changeshow: false
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
                    if(this.detail_message.msg != 'ok'){
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
            this.$http
                .post('student_center/S_P_detail/', array)
                .then(result => {
                    if(result.body === 'ok'){
                        alert('提交成功')
                        this.$router.push({path:'/S_half'})
                    }else{
                        alert(result.body)
                    }
                })
        }
    },
    created() {
        this.getData()
    }
}
</script>