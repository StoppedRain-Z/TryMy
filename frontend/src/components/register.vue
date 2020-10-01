<template>
  <div>
    <el-form :model="registerData" ref="form">
      <el-form-item label="我是" prop="user_type">
        <el-select @change="showChange" v-model="registerData.user_type">
          <el-option key="学生" label="学生" value="S"></el-option>
          <el-option key="教师" label="教师" value="T"></el-option>
          <el-option key="辅导员" label="辅导员" value="A"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="证件号（学生证号/教师证号）" prop="cardID">
        <el-input v-model="registerData.cardID"></el-input>
      </el-form-item>
      <el-form-item label="姓名">
        <el-input v-model="registerData.name"></el-input>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="registerData.password" type="password"></el-input>
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="registerData.email"></el-input>
      </el-form-item>
      <el-form-item label="联系电话">
        <el-input v-model="registerData.mobile"></el-input>
      </el-form-item>
      <el-form-item label="研究所" v-show="showT">
        <el-select v-model="registerData.institute">
          <el-option label="图所" value="图所"></el-option>
          <el-option label="网络所" value="网络所"></el-option>
          <el-option label="系统所" value="系统所"></el-option>
          <el-option label="信息所" value="信息所"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="个人主页" v-show="showT">
        <el-input v-model="registerData.teacher_info"></el-input>
      </el-form-item>
      <el-form-item label="身份选择" prop="student_type" v-show="showS">
        <el-select v-model="registerData.student_type">
          <el-option key="非留学生" label="非留学生" value="U"></el-option>
          <el-option key="留学生" label="留学生" value="F"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="毕业年份" v-show="showS">
        <el-select v-model="registerData.grade" value-key="label" placeholder="请选择">
          <el-option v-for="item in options" :label="item.label" :key="item.label" :value="item.label">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="辅导的学生的毕业年份" v-show="showA">
        <el-select v-model="registerData.grade" value-key="label" placeholder="请选择">
          <el-option v-for="item in options" :label="item.label" :key="item.label" :value="item.label">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="register">注册</el-button>
        <router-link to="/login">
          <el-button>返回</el-button>
        </router-link>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import DateSelect from './DateSelect'
export default {
  components: {DateSelect},
  data(){
    return {
      registerData: {
        cardID: '',
        name: '',
        password: '',
        email: '',
        mobile: '',
        teacher_info: '',
        institute: '',
        student_type: '',
        grade: ''
      },
      options: [],
      showA: false,
      showT: false,
      showS: true
    }
  },
  methods: {
    register () {
      console.log(this.registerData)
      this.$http
        .post('register/', this.registerData)
        .then(result => {
          console.log(result.body.msg);
          if(result.body.msg === 'ok'){
            alert("注册成功")
            this.$router.push({path:'/login'})
          }else if(result.body.msg === "缺少注册信息"){
            alert(result.body.msg)
          }else{
            alert(result.body.msg)
          }
          /*if(result.body.msg === 'ok'){
            alert("注册成功");
            this.$router.push({path:'/login'})
          }else{
            alert("注册失败");
          }*/
        });
    },
    showChange (value) {
      if (value === 'T') {
        this.showA = false
        this.showT = true
        this.showS = false
      } else if (value === 'A') {
        this.showA = true
        this.showT = false
        this.showS = false
      } else {
          this.showA = false
          this.showT = false
          this.showS = true
      }
    },
    yearSelect() {
      var myDate = new Date;
      var year = myDate.getFullYear();
      for(var i = 0; i < 3; i++){
        this.options.push({label: year+i})
      }
    }
  },
  created () {
    this.yearSelect()
  }
}
</script>
