<template>
  <div>
    <el-container>
      <el-main>
        <el-main style="width:100%">
        <div>
          <el-table 
            :data = "tables"
            ref = "multipleTable"
            tooltip-effect="dark"
            style="width:100%"
            highlight-current-row >
            <el-table-column label="序号" style="width:5%" type="index"></el-table-column>
            <template v-for='(col) in tableData'>
              <el-table-column
                :show-overflow-tooltip="true"
                :prop="col.dataItem"
                :label="col.dataName"
                :key="col.dataItem"
                style="width:90%">
              </el-table-column>
            </template>
          </el-table>
        </div>
      </el-main>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      tables:[{
          "teacher_name": 'a',
          "student_name": '12',
          "institute": '图索'
          },{
          "teacher_name": 'a',
          "student_name": '13',
          "institute": '图索'
          }],
      tableData:[{
        dataItem: 'student_name',
        dataName: '学生姓名'
      },{
        dataItem: 'teacher_name',
        dataName: '教师姓名'
      },{
        dataItem: 'institute',
        dataName: '研究所'
      }]
    }
  },
  methods: {
    getData() {
      this.$http
        .get('assistant_center/teacher_to_student_selected')
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

