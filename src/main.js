import Vue from 'vue'
import ElementUI from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueDataTables from 'vue-data-tables'
import HighchartsVue from 'highcharts-vue'

//Vue.use(VueAxios, axios)
//Vue.prototype.$http = axios
Vue.config.productionTip = false

//Vue.use(DataTables.DataTables)
Vue.use(VueDataTables)
Vue.use(HighchartsVue)
// install Element-UI
Vue.use(ElementUI, { size: 'small', locale }, axios)

// load custom components

import DisplayGraph from './components/DisplayGraph.vue'
import DisplayTable from './components/DisplayTable.vue'
import DeviceForm from './components/DeviceForm.vue'
import DeviceHeader from './components/DeviceHeader.vue'
import DeviceAside from './components/DeviceAside.vue'
import DeviceSetting from './components/DeviceSettings.vue'
import DisplayLegend from './components/DisplayLegend.vue'
import DayPlot from './components/DayPlot.vue'
import InfoDevice from './components/InfoDevice.vue'
import DisplayAverage from './components/DisplayAverage.vue'

// install globally cutom components
Vue.component('display-table', DisplayTable)
Vue.component('device-aside', DeviceAside)
Vue.component('device-header', DeviceHeader)
Vue.component('display-legend', DisplayLegend)
Vue.component('device-form', DeviceForm)
Vue.component('device-settings', DeviceSetting)
Vue.component('day-plot', DayPlot)
Vue.component('info-device', InfoDevice)
Vue.component('display-graph', DisplayGraph)
Vue.component('display-average', DisplayAverage)
//Vue.component('device-tools', DeviceTools)
/*Vue.use(Element)*/   /* to do importer un par un */
/* eslint-disable no-new */

import App from './App.vue'

new Vue({
  el: '#app',
  template: '<App/>',
  components: { App }
})
