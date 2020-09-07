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
            <el-table-column width="45px">
              <template scope="scope">
                <el-radio v-model="radio" :label="scope.$index" @change="changeTeacher">{{''}}</el-radio>
              </template>
            </el-table-column>
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
      radio:'',
      tables: [],
      tableData:[{
        dataItem: 'teacher_name',
        dataName: '教师姓名'
      },{
        dataItem: 'teacher_institute',
        dataName: '研究所'
      },
      {
        dataItem: 'teacher_info',
        dataName: '个人主页'
      }]
    }
  },
  methods: {
    getData () {
      this.$http
        .get('student_center/choose_teacher')
        .then(result => {
          this.tables = result.body
        })
    },
    commit () {
      var selectData = this.$refs.multipleTable.selection
      console.log(this.radio)
      this.$http
        .post('student_center/choose_teacher.', selectData)
        .then(result => {
          console.log(result.body)
        })
    },
    changeTeacher(row) {
        console.log(row)
        console.log(this.tables[row].teacher_name)
        //this.radio = this.tables[row]
    }
  },
  created () {
    this.getData()
  }
}
</script>
