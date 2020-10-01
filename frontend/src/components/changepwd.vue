<template>
  <div>
    <el-container>
      <el-main>
        <el-form :model="detail_message" ref="form" :rules="rules" label-width="100px" class="demo-form"
            cell-style="font-weight: 700;">
            <el-form-item label="旧密码">
                <el-input v-model="detail_message.old_pwd" type="password"></el-input>
            </el-form-item>
            <el-form-item label="新密码">
                <el-input v-model="detail_message.new_pwd" type="password"></el-input>
            </el-form-item>
        </el-form>
        <el-form>
            <el-button @click="commit" type = "primary">提交</el-button>
        </el-form>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
    data() {
        return {
            detail_message: {}
        }
    },
    methods: {
        commit() {
            var array = {
                "old_pwd": this.detail_message.old_pwd,
                "new_pwd": this.detail_message.new_pwd
            }
            console.log(array)
            this.$http
                .post('/change_password/', array)
                .then(result => {
                    if(result.body === 'ok'){
                        alert("密码修改完成")
                        this.detail_message = {}
                        //this.$router.push({path:'/login'})
                    }else{
                        alert(result.body)
                    }
                })
        }
    }
}
</script>