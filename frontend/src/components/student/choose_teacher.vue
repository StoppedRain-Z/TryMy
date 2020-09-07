<template>
  <div>
    <el-container>
      <el-main style="width:100%">
        <div>
          <el-table :data="tables" style="width: 100%">
            <el-table-column type="expand">
              <template slot-scope="props">
                <el-form label-position="left">
                  <el-form-item label="姓名">
                    <span>{{props.row.teacher_name}}</span>
                  </el-form-item>
                  <el-form-item label="研究所">
                    <span>{{props.row.teacher_insititute}}</span>
                  </el-form-item>
                  <el-form-item label="个人主页">
                    <span>{{props.row.teacher_info}}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
            <el-table-column label="姓名" prop="teacher_name"></el-table-column>
            <el-table-column label="研究所" prop="teacher_institute"></el-table-column>
            <el-table-column label="个人主页" prop="teacher_info"></el-table-column>

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
      tables: []
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
