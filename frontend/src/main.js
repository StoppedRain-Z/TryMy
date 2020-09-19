// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import App from './App.vue'
import VueRouter from 'vue-router'
import router from './router.js'
import VueResource from 'vue-resource'
import Vuex from 'vuex'
import store from './store.js'
import axios from 'axios'

//Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.use(VueResource)
Vue.use(Vuex)

Vue.prototype.$axios = axios

Vue.http.options.root = 'http://127.0.0.1:8000'
Vue.http.options.emulateJSON = true


/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store
})

router.beforeEach((to, from, next) =>{
  if (to.matched.some(record => record.meta.login)) {
    if (store.state.islogin) {
      console.log(store.state.islogin)
      next()
    } else {
      next({path: '/login', query: {redirect: to.fullPath}})
    }
  } else {
    next()
  }
})
