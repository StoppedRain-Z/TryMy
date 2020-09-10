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
            highlight-current-row >
            <template v-for='(col) in tableData'>
              <el-table-column
                :show-overflow-tooltip="true"
                :prop="col.dataItem"
                :label="col.dataName"
                :key="col.dataItem"
                style="width:90%">
              </el-table-column>
            </template>
            <el-table-column label="操作" style="width:10%" align="center">
            <template slot-scope="scope">
              <router-link :to="{path:'/progress_student_detail', query:{id:scope.row.id, student_id:scope.row.student_id}}">
              <el-button type="primary">查看详情</el-button>
              </router-link>
            </template>
          </el-table-column>
          </el-table>
        </div>
      </el-main>
    </el-container>
  </div>
</template>


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
          "teacher_ok": '已批改'
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
        })
    }
  },
  created () {
    this.getData()
  }
}
</script>
