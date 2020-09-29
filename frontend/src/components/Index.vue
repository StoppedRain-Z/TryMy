<template>
  <div>
    <router-link to="/login">
      <el-button>登录</el-button>
    </router-link>
    <router-link to="/register">
      <el-button>注册</el-button>
    </router-link>
  </div>
</template>

<script>
export default {
  mounted() {
    this.$router.push({path: '/login'})
  },
  methods:{
  }
}
</script>