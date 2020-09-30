<template>
  <div id = "myDate">
    <el-select v-model="yearsModel" @change="dateChange(1)" placeholder="请选择">
      <el-option 
        v-for="item in years"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
  </div>
</template>

<script>
export default {
    props: {},
    data() {
        return {
            yearsModel:null,
            years:[]
        }
    },
    created () {
        this.init();
    },
    methods: {
        init() {
            var myDate = new Date;
            var year = myDate.getFullYear();
            this.initSelectYear(year)
            this.yearsModel = year
            let obj={year: this.yearsModel}
            this.$parent.dateChange(obj)
        },
        initSelectYear(year){
            this.years = [];
            for(let i = 0; i < 30; i++){
                this.years.push({value:(year+i),label:(year+i)+"年"});
            }
        }
    }
}
</script>