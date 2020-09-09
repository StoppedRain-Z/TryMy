<template>
  <div>
    <el-container>
      <el-main style="width:100%">
        <div class = "choose_student">
          <el-table
            :data = "tables"
            ref = "multipleTable"
            tooltip-effect="dark"
            style="width:100%">
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
    </el-container>
  </div>
</template>


<script>
  export default {
    data () {
      return {
        tables: [],
        tableData: [{
          dataItem: 'student_id',
          dataName: '学生证号'
        }]
      }
    },
    methods: {
      getData () {
        this.$http
          .get('teacher_center/choose_student')
          .then(result => {
            console.log(result.body)
            this.tables = result.body
          })
      }
    }
  }
</script>
