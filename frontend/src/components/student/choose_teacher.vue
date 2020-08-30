<template>
  <div>
    <el-container>
      <el-main style="width:100%">
        <div>
          <el-table ref="multipleTable" :data="tableData" style="width: 100%" @selection-change="handleSelectionChange">
            <el-form method="post">
              <el-table-column type="selection" width="55"></el-table-column>
              <el-table-column prop="name" label="姓名" width="120"></el-table-column>
              <el-table-column prop="institute" label="研究所" width="120"></el-table-column>
              <el-table-column prop="teacher_info" label="个人主页" show-overflow-tooltip></el-table-column>
            </el-form>
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
      tableData: []
    }
  },
  methods: {
    getData () {
      this.$http.get('/student_center/choose_teacher').then(result => {
        console.log(result.body)
        this.tableData = result.body
        console.log(result.body)
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
    this.getData()
  }
}
</script>
