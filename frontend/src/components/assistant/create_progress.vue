<template>
  <div>
    <el-container>
      <el-main>
        <el-form :model="form" ref="form" :rules="rules" label-width="100px" class="demo-form">
          <el-form-item label="进度名称" prop="title">
            <el-input v-model="form.title"></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="desc">
            <el-input type="textarea" v-model="form.desc"></el-input>
          </el-form-item>
          <el-form-item label="开始时间" required>
            <el-col :span="11">
              <el-form-item prop="start_time">
                <el-date-picker
                  type="date"
                  placeholder="选择日期"
                  v-model="form.start_time"
                  style="width: 100%;">
                </el-date-picker>
              </el-form-item>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="11">
              <el-form-item prop="end_time">
                <el-date-picker
                  type="date"
                  placeholder="选择日期"
                  v-model="form.end_time"
                  style="width: 100%;">
                </el-date-picker>
              </el-form-item>
            </el-col>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submit('form')">创建进度，并发送邮件</el-button>
            <el-button @click="reset('form')">重置</el-button>
          </el-form-item>
        </el-form>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      form: {
        title: '',
        desc: '',
        start_time: '',
        end_time: ''
      },
      rules: {
        title: [{required: true, message: '请输入进度名称', trigger: 'blur'}],
        desc: [{required: true, message: '请输入具体描述', trigger: 'blur'}],
        start_time: [{type: 'date', required: true, message: '请选择日期', trigger: 'change'}],
        end_time: [{type: 'date', required: true, message: '请选择日期', trigger: 'change'}]
      }
    }
  },
  methods: {

  }
}
</script>
