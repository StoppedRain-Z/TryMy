<template>
  <div>
    <el-container>
      <el-main style="width:100%">
        <div>
          <el-table
            :data="tables"
            ref="multipleTable"
            tooltip-effect="dark"
            style="width: 100%"
            highlight-current-row>
            <template v-for="(col) in tableData">
              <el-table-column
                :show-overflow-tooltip="true"
                :prop="col.dataItem"
                :label="col.dataName"
                :key="col.dataItem"
                style="width: 100%">
              </el-table-column>
            </template>
            <el-table-column label="操作" style="width: 100%" align="center">
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
      id: 0,
      tables: [],
      tableData: [{
        dataItem: 'id',
        dataName: '作业序号'
      }, {
        dataItem: 'student_name',
        dataName: '学生姓名'
      }, {
        dataItem: 'student_ok',
        dataName: '提交情况'
      }, {
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
        .get('teacher_center/T_unfinished/', {params: array})
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
