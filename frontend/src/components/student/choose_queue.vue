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
      tables:[],
      tableData:[{
        dataItem: 'name',
        dataName: '教师姓名'
      },{
        dataItem: 'teacher_choice',
        dataName: '教师反馈'
      }]
    }
  },
  methods: {
    getData() {
      this.$http
        .get('student_center/choose_queue')
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

