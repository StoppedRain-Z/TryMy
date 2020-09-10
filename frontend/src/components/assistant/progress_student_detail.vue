<template>
  <div>
    <el-container>
      <el-main>
        <el-form :model="detail_message" ref="form" :rules="rules" label-width="100px" class="demo-form">
            <el-form-item label="进度名称">detail_message.lalala</el-form-item>
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
            student_id:'',
            detail_message: {"lalala":123456}
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
            this.$http
                .get('assistant_center/progress_student_detail', array)
                .then(result => {
                    this.detail_message = result.body
                    if(this.detail_message.msg != 'ok'){
                        alert(this.detail_message)
                    }
                })
        }
    }
}
</script>