<template>
  <div>
    <el-container>
      <el-main style="width:100%">
        <div>
          <el-table 
            ref="multipleTable" 
            :data="tables" 
            style="width: 100%" 
            tooltip-effect="dark"
            @selection-change="handleSelectionChange">
            
              <el-table-column type="selection" width="45px"></el-table-column>
              <el-table-column label="序号" style="width:5%" type="index"></el-table-column>
              <template v-for='(col) in tableData'>
                <el-table-column
                  sortable
                  :show-overflow-tooltip="true"
                  :prop="col.dataItem"
                  :label="col.dataName"
                  :key="col.dataItem"
                  style="width:90%">
                </el-table-column>
              </template>
           
          </el-table>
          <el-button type="primary" @click="commit">提交</el-button>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      tables:[{'teacher_name': '123456', 'teacher_institute': '图所', 'teacher_info': '123456'}],
      tableData:[{
        dataItem:'teacher_name',
        dataName:'姓名'
      },{
        dataItem:'teacher_institute',
        dataName:'研究所'
      },{
        dataItem:'teacher_info',
        dataName:'个人主页'
      }]
    }
  },
  methods: {
    getData () {
      this.$http.get('/student_center/choose_teacher').then(result => {
        //console.log(result.body)
        this.tables = result.body
        console.log(this.tables)
      })
    },
    commit () {
      var selectData = this.$refs.multipleTable.selection
      console.log(selectData)
      this.$http
        .post('student_center/choose_teacher.', selectData)
        .then(result => {
          console.log(result.body)
        })
    }
  },
  created () {
    //this.getData()
  }
}
</script>
