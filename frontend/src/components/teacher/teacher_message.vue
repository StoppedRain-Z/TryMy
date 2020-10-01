<template>
  <div>
    <el-container>
      <el-main>
        <el-form :model="detail_message" ref="form" :rules="rules" label-width="100px" class="demo-form"
            cell-style="font-weight: 700;">
            <el-form-item label="姓名">{{detail_message.teacher_name}}</el-form-item>
            <el-form-item label="证件号">{{detail_message.teacher_id}}</el-form-item>
            <el-form-item label="邮箱" v-show="unchangeshow">{{detail_message.email}}</el-form-item>
            <el-form-item label="联系电话" v-show="unchangeshow">{{detail_message.mobile}}</el-form-item>
            <el-form-item label="邮箱" v-show="changeshow">
                <el-input v-model="detail_message.email" type="textarea"></el-input>
            </el-form-item>
            <el-form-item label="联系电话" v-show="changeshow">
                <el-input v-model="detail_message.mobile" type="textarea"></el-input>
            </el-form-item>
            <el-form-item label="研究所">{{detail_message.institute}}</el-form-item>
            <el-form-item label="个人主页" v-show="unchangeshow">{{detail_message.teacher_info}}</el-form-item>
            <el-form-item label="个人主页" v-show="changeshow">
                <el-input v-model="detail_message.teacher_info" type="textarea"></el-input>
            </el-form-item>
        </el-form>
        <el-form>
            <el-button @click="changemessage" type = "primary" v-show="unchangeshow">修改</el-button>
            <el-button @click="commit" type = "primary" v-show="changeshow">提交</el-button>
            <el-button @click="logout">登出</el-button>
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
            detail_message: {},
            unchangeshow: true,
            changeshow: false,
            options: []
        }
    },
    methods: {
        getData() {
            this.$http
                .get('/teacher_center/T_message/')
                .then(result => {
                    this.detail_message = result.body
                    console.log(result.body)
                    if(this.detail_message.msg !== 'ok'){
                        alert(this.detail_message.msg)
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
        },
        changemessage() {
            this.unchangeshow = false
            this.changeshow = true
        },
        commit() {
            var array = {
                "email": this.detail_message.email,
                "mobile": this.detail_message.mobile,
                "teacher_info": this.detail_message.teacher_info
            }
            console.log(array)
            this.$http
                .post('/teacher_center/T_detail/', array)
                .then(result => {
                    if(result.body === 'ok'){
                        this.unchangeshow = true
                        this.changeshow = false
                        alert("个人信息修改完成")
                        this.getData()
                    }else{
                        alert(result.body)
                    }
                })
        },
        yearSelect() {
            var myDate = new Date;
            var year = myDate.getFullYear();
            for(var i = 0; i < 3; i++){
                this.options.push({label: year+i})
            }
            console.log(this.options)
        }
    },
    created() {
        this.getData()
        this.yearSelect()
    }
}
</script>
