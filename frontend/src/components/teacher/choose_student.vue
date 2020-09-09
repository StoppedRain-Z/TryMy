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
          <el-table-column label="序号" style="width:10%" type="index"></el-table-column>
          <template v-for='(col) in tableData'>
            <el-table-column
              :show-overflow-tooltip="true"
              :prop="col.dataItem"
              :label="col.dataName"
              :key="col.dataItem"
              style="width:80%">
            </el-table-column>
          </template>
          <el-table-column label="操作" style="width:10%" align="center">
            <template slot-scope="scope">
              <el-button type="primary" @click="agree(scope.row)">同意</el-button>
              <el-button type="primary" @click="disagree(scope.row)">拒绝</el-button>
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
        row:0,
        radio: {},
        tables:[],
        tableData: [{
          dataItem: 'student_id',
          dataName: '学生证号'
        }, {
          dataItem: 'name',
          dataName: '姓名'
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
      },
      agree(row){
        console.log(row)
        var array = {
          "student_id": row.student_id,
          "choice": 2
        }
        console.log(array)
        this.radio = array
        this.$http
          .post('teacher_center/choose_student/', array)
          .then(result =>{
            console.log(result.body)
            this.getData()
            if(result.body === 'ok'){
              alert("已同意")
            }else if(result.body === 'max'){
              alert("您同意的学生已经超过可同意范围，故该学生申请已被拒绝")
            }else{
              alert("该学生已有导师，故该学生申请被拒绝")
            }
          })
      },
      disagree(row){
        var array = {
          "student_id": row.student_id,
          "choice": 3
        }
        console.log(array)
        this.radio = array
        this.$http
          .post('teacher_center/choose_student/', array)
          .then(result =>{
            console.log(result.body)
            this.getData()
            if(result.body === 'ok'){
              alert("已拒绝")
            }else{
              alert("请重新选择")
              //this.getData()
            }
          })
      }
    },
    created () {
      this.getData()
    }
  }
</script>
