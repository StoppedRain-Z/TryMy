<template>
  <div>
    <el-form model="form" ref="form" >
      <el-form-item label="证件号（学生证号/教师证号）">
        <el-input v-model="form.cardID" placeholder="请输入证件号"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" placeholder="请输入密码" type="password"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="login">登录</el-button>
        <router-link to="/">
          <el-button>返回</el-button>
        </router-link>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data(){
    return {
      form: {
        cardID:"",
        password:""
      }
    };
  },
  methods:{
    login(){
      this.$http.post("login/",this.form).then(result => {
        console.log(result.body);
        if(result.body.msg === 'ok'){
          //alert("登录成功");

          if(result.body.user_type === 'S'){
            this.$store.commit('login',1)
            this.$router.push({path: '/student_center'})
          }else if(result.body.user_type === 'T'){
            this.$store.commit('login',2)
            this.$router.push({path:'/teacher_center'})
          }else if(result.body.user_type === 'A'){
            this.$store.commit('login',3)
            this.$router.push({path:'/assistant_center'})
          }

        }else{
          alert("登陆失败:证件号或密码错误");

        }
        //this.$store.commit('login',1)
        //this.$store.commit('setSession',this.form.cardID)
      });
    }
  }
}
</script>
