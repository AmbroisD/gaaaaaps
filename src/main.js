import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

import Element from 'element-ui'


Vue.use(Element)   /* to do importer un par un */
/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App }
})
