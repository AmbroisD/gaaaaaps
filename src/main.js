import Vue from 'vue'
import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'
import 'element-ui/lib/theme-chalk/index.css'

Vue.config.productionTip = false


// install Element-UI
Vue.use(ElementUI, { size: 'small', locale })

// load custom components
//import DisplayTable from './components/DisplayTable.vue'
//import DeviceForm from './components/DeviceForm.vue'
//import DeviceTools from './components/DeviceTools.vue'
import DisplayLegend from './components/DisplayLegend.vue'

// install globally cutom components
//Vue.component('display-table', DisplayTable)
Vue.component('display-legend', DisplayLegend)
//Vue.component('device-form', DeviceForm)
//Vue.component('device-tools', DeviceTools)
/*Vue.use(Element)*/   /* to do importer un par un */
/* eslint-disable no-new */

import App from './App.vue'

new Vue({
  el: '#app',
  template: '<App/>',
  components: { App },
  data :{
    visible : false
  }
})
