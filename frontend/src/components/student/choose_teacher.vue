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
            <el-table-column type="expand">
              <template slot-scope = "scope">
                <el-form label-position="left">
                  <el-form-item label="教师姓名">
                    <span>{{scope.row.teacher_name}}</span>
                  </el-form-item>
                  <el-form-item label="个人主页">
                    <span>{{scope.row.teacher_info}}</span>
                  </el-form-item>
                  <el-form-item label="教师邮箱">
                    <span>{{scope.row.email}}</span>
                  </el-form-item>
                  <el-form-item label="教师电话">
                    <span>{{scope.row.mobile}}</span>
                  </el-form-item>
                </el-form>
              </template>
            </el-table-column>
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
      row:0,
      radio:{},
      tables: [{
        'teacher_name':'陈倩',
        'teacher_institute':'垃圾所',
        'teacher_info':'ads',
        'student_count':0,
        'foreign_count':0,
        'email':'chenqianshmily@126.com',
        'mobile':'13260256266'
      },{
        'teacher_name':'陈倩',
        'teacher_institute':'垃圾所',
        'teacher_info':'ads',
        'student_count':0,
        'foreign_count':0,
        'email':'chenqianshmily@126.com',
        'mobile':'13260256266'
      }],
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
      },{
        dataItem: 'student_count',
        dataName: '非留学生'
      },{
        dataItem: 'foreign_count',
        dataName: '留学生'
      }]
    }
  },
  methods: {
    getData () {
      this.$http
        .get('student_center/choose_teacher')
        .then(result => {
          this.tables = result.body
          console.log(result.body)
        })
    },
    commit () {
      console.log(this.row)
      var array = {
          //"teacher_name": this.tables[this.row].teacher_name,
          //"teacher_institute": this.tables[this.row].teacher_institute,
          //"teacher_info": this.tables[this.row].teacher_info,
          "teacher_id": this.tables[this.row].teacher_id
        }
      this.radio = array
      console.log(this.radio)
      this.$http
        .post('student_center/choose_teacher/', this.radio)
        .then(result => {
          console.log(result.body)
          if (result.body === 'ok') {
            alert('加入已选志愿')
          } else if (result.body === 'max') {
            alert('该老师名额已满，请重新选择')
          } else {
            alert(result.body)
          }
        })
    },
    changeTeacher(row) {
        console.log(row)
        this.row = row

        //console.log(this.radio)
        //this.radio = this.tables[row]
    }
  },
  created () {
    //this.getData()
  }
}
</script>
