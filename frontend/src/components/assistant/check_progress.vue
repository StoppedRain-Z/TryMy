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
            <template v-for='(col) in tableData'>
              <el-table-column
                :show-overflow-tooltip="true"
                :prop="col.dataItem"
                :label="col.dataName"
                :key="col.dataItem"
                style="width:100%">
              </el-table-column>
            </template>
            <el-table-column label="操作" style="width:10%" align="center">
            <template slot-scope="scope">
              <router-link :to="{path:'/progress_student', query:{id:scope.row.id}}">
              <el-button type="primary">查看详情</el-button>
              </router-link>
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
      radio:{},
      tables: [],
      tableData:[{
        dataItem: 'id',
        dataName: '序号'
      },{
        dataItem: 'title',
        dataName: '进度名称'
      },{
        dataItem: 'start_time',
        dataName: '开始时间'
      },{
        dataItem: 'end_time',
        dataName: '结束时间'
      }]
    }
  },
  methods: {
    getData () {
      this.$http
        .get('assistant_center/check_progress')
        .then(result => {
          this.tables = result.body
        })
    },
  },
  created () {
    this.getData()
  }
}
</script>
