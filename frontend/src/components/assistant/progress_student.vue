<template>
  <div>
    <el-container>
      <el-main style="width:100%">
        <div>
          <el-table
            :data = "tables"
            ref = "multipleTable"
            tooltip-effect="dark"
            style="width:100%"
            :row-class-name="tableRowClassName"
            highlight-current-row>
            <template v-for='(col) in tableData'>
              <el-table-column
                :show-overflow-tooltip="true"
                :prop="col.dataItem"
                :label="col.dataName"
                :key="col.dataItem"
                style="width:60%">
              </el-table-column>
            </template>
            <el-table-column label="操作" style="width:40%" align="center">
            <template slot-scope="scope">
              <el-button type="primary" @click="send_to_teacher(scope.row)" size="small" v-show="scope.row.teacher_ok=='未批改'">提醒老师</el-button>
              <router-link :to="{path:'/progress_student_detail', query:{id:scope.row.id, student_id:scope.row.student_id}}">
             查看详情
              </router-link>
            </template>
          </el-table-column>
          </el-table>
          <router-link to="/check_progress">
        <el-button  type="primary">返回</el-button>
        </router-link>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<style>
  .el-table .warning-row {
    background: #FFA29B;
  }
  .el-table .success-row {
    background: #A9FC9E;
  }
</style>

<script>
export default {
  data () {
    return {
      id:0,
      radio:{},
      tables: [{
          "id":1,
          "title": 'test1',
          "student_name": '我是13',
          "student_id": '13',
          "student_ok": '已完成',
          "teacher": 'a',
          "teacher_ok": '未批改'
        },
        {
          "id":1,
          "title": 'test1',
          "student_name": '我是12',
          "student_id": '12',
          "student_ok": '已完成',
          "teacher": 'a',
          "teacher_ok": '未达到预期'
        },{
          "id":1,
          "title": 'test1',
          "student_name": '我是11',
          "student_id": '11',
          "student_ok": '已完成',
          "teacher": 'b',
          "teacher_ok": '超进度完成'
        }],
      tableData:[{
        dataItem: 'id',
        dataName: '作业序号'
      },{
        dataItem: 'student_name',
        dataName: '学生姓名'
      },{
        dataItem: 'student_ok',
        dataName: '提交情况'
      },{
        dataItem: 'teacher',
        dataName: '老师'
      },{
        dataItem: 'teacher_ok',
        dataName: '批改情况'
      }]
    }
  },
  methods: {
    getData () {
      this.id = this.$route.query.id
      console.log(this.id)
      var array = {'id': this.id}
      console.log(array)
      this.$http
        .get('assistant_center/progress_student/', {params: array})
        .then(result => {
          this.tables = result.body
          console.log(result.body)
        })
    },
    tableRowClassName({row, rowIndex}){
      if(row.teacher_ok== '未达到预期'){
        return 'warning-row';
      }else if (row.teacher_ok == '未批改'){
        return ''
      }else {
        return 'success-row'
      }
      
    },
    send_to_teacher(row){
      var array = {
        'teacher_id': row.teacher_id,
        'student_name': row.student_name,
        'title': row.title
      }
      console.log(array)
      this.$http
        .post('assistant_center/progress_student/send_mail_teacher', array)
        .then(result => {
          console.log(result.body)
          if (result.body === 'ok') {
            alert('提醒教师成功')
          } else {
            alert(result.body)
          }
        })
    }
  },
  created () {
    this.getData()
  }
}
</script>
