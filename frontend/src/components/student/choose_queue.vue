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
            <el-table-column label="操作" style="width:5%" align="center">
            <template slot-scope="scope">
              <el-button type="info" @click="cancel(scope.row)" v-show= "scope.row.teacher_choice!=='已取消'">取消</el-button>
            </template>
          </el-table-column>
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
          console.log(this.tables)
        })
      
    },
    cancel(row){
      console.log(row)
      var array = {
        'teacher_id': row.teacher_id
      }
      console.log(array)
      this.$http
        .post('student_center/cancel_choose/', array)
        .then(result => {
          console.log(result.body)
          if (result.body === 'ok') {
            alert('已取消')
          } else {
            alert(result.body)
          }
          this.getData()
        })
    }
  },
  created () {
    this.getData()
  }
}

</script>

