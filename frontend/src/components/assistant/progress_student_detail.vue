<template>
  <div>
    <el-container>
      <el-main>
        <el-form :model="detail_message" ref="form" :rules="rules" label-width="100px" class="demo-form"
            cell-style="font-weight: 700;">
            <el-form-item label="进度名称">{{detail_message.title}}</el-form-item>
            <el-form-item label="详细描述">{{detail_message.desc}}</el-form-item>
            <el-form-item label="学生姓名">{{detail_message.student_name}}</el-form-item>
            <el-form-item label="提交内容">{{detail_message.student_text}}</el-form-item>
            <el-form-item label="指导教师">{{detail_message.teacher_name}}</el-form-item>
            <el-form-item label="教师反馈">{{detail_message.teacher_text}}</el-form-item>
        </el-form>
        <router-link to="/progress_student">
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
            this.$http
                .get('assistant_center/progress_student_detail', array)
                .then(result => {
                    this.detail_message = result.body
                    if(this.detail_message.msg != 'ok'){
                        alert(this.detail_message.msg)
                    }
                })
        }
    }
}
</script>