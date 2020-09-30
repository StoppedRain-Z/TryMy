<template>
  <div>
    <el-container>
      <el-main>
        <el-form label="导入文件">
            <input style="width: 260px" type="file" 
              ref= "pathClear" @change="getFile($event)"></input>
            <span>仅支持扩展名为.xls .xlsx的文件</span>
        </el-form>
        <el-button type="primary" @click="commit">提交</el-button>
        <el-form v-show = "isshow">成功导入以下同学信息，若有同学未成功导入，请查看.xls/.xlsx文件中未导入的第一个同学相关信息是否有误</el-form>
        <el-table
          :data = "tables"
          ref = "multipleTable"
          tooltip-effect="dark"
          style="width:100%"
          highlight-current-row
          v-show = "isshow">
          <el-table-column type="expand">
            <template slot-scope = "scope">
              <el-form label-position="left">
                <el-form-item label="学号">
                  <span>{{scope.row.id}}</span>
                </el-form-item>
                <el-form-item label="姓名">
                  <span>{{scope.row.name}}</span>
                </el-form-item>
                <el-form-item label="电话">
                  <span>{{scope.row.mobile}}</span>
                </el-form-item>
                <el-form-item label="邮箱">
                  <span>{{scope.row.email}}</span>
                </el-form-item>
                <el-form-item label="身份">
                  <span>{{scope.row.type}}</span>
                </el-form-item>
              </el-form>
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
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
    data() {
        return {
            tables: [],
            tableData: [{
                dataItem: 'id',
                dataName: '学号'
            },{
                dataItem: 'name',
                dataName: '姓名'
            }],
            formData: {
                'file': ''
            },
            isshow: false
        }
    },
    methods: {
        getFile(event) {
            var file = event.target.files[0]
            console.log(file.name)
            var index = file.name.lastIndexOf(".")
            var type = file.name.substr(index+1)
            if(type !== "xls" && type !== "xlsx"){
                this.$refs.pathClear.value = ''
                alert("不支持该文件类型")
                return 
            }
            this.formData.file = event.target.files[0]
            console.log(this.formData.file)
        },
        commit() {
            var formData = new window.FormData();
            formData.append('file',this.formData.file)
            console.log(array)
            this.$http
                .post('assistant_center/create_many_student/', array, {
                    headers:{
                        'Contene-Type': 'multipart/form-data'
                    }
                })
                .then(result => {
                    console.log(result.body)
                    this.tables = result.body
                    this.isshow = true
                })
        }
    }
}
</script>