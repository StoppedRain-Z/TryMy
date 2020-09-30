<template>
  <div>
    <el-container>
      <el-main>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  mounted() {
    this.$router.push({path: '/choose_student'})
  },
  methods:{
  }
}
</script>