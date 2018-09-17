<template>
  <div>
    <el-container style="height: 100vh;">
      <el-header>
        <device-header
          v-model="indexHeader" >
        </device-header>
      </el-header>
      <el-container>
        <device-aside
          :table="activeTable"
          v-on:goHome="indexHeader = 'home'"
          v-model="activeIndex">
        </device-aside>
          <el-main
            class="datatable-style"
            v-if="indexHeader == 'home'">
            <device-form
              v-model="sdsForm"
              :options="options"
              :validDate="validDate"
              :loadedOption="loadedOption"
              v-on:submitForm="getData"
              v-on:updateDate="loadOption"
              v-if="activeIndex == '1'">
            </device-form>
            <display-average
              v-if="activeIndex == '4'"
              v-model="dataTable"
              :settings="settings">
            </display-average>
            <display-legend
              v-if="activeIndex == '2'">
            </display-legend>
            <display-table
              :mode="mode"
              :detail="detail"
              :infos="infos"
              :settings="settings"
              :station="station"
              v-model="dataTable"
              v-on:stationActive="loadStation"
              v-on:dayActive="loadInfos"
              v-if="activeIndex == '2'">
            </display-table>
            <el-dialog
              :visible.sync="detail.active"
              v-if="activeIndex == '2' && detail.active"
              width="70%">
            <info-device
              :detail="detail"
              :infos="infos">
            </info-device>
          </el-dialog>
          <el-dialog
            :visible.sync="showStationGraph"
            width="70%">
            <h2> {{ station.sta_info.station }}  </h2>
            <display-graph
              v-if="station.visible"
              v-loading="loading"
              :station="station">
            </display-graph>
          </el-dialog>
          </el-main>
          <el-main v-if="indexHeader == 'userSettings'">
            <keep-alive>
              <device-settings
                 v-model="settings"
                 @settings-updated="storeSettings">
             </device-settings>
          </keep-alive>
          </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import settings from './settings.json'
import axios from 'axios'

const STORAGE_KEY = 'settings'


export default {
  data() {
    return {
      mode:'public',
      settings: {},
      options:{},
      validDate: [],
      loadedOption: null,
      loading: false,
      showStationGraph: false,
      indexHeader: 'home',
      activeIndex: '1',
      activeTable: false,
      dataTable: {data: '',
                  loading: false},
      sdsForm: {
                rangedate:'',
                s_date: null,
                e_date: null,
                y_date: null,
                comp: [],
                type: [],
                loc:[],
                sta:[],
                more_option: false,
                network: [],
                julian_day: true,
                visible: false
              },
      infos: {
        visible: false,
        data: {},
        gapList: []
      },
      detail: {active: false},
      station: {visible: false,
                data:{},
                sta_info: {}}
    };
  },
  mounted () {
  this.loadSettings()
  this.initStyle()
  this.getYearAvail()
  },
  methods: {
    loadOption(val) {
      console.log('load')
      axios.post("ws/form", {val}).then((response)  =>  {
        this.options = response.data
        this.sdsForm.type = this.options.result.type
        this.sdsForm.network = this.options.result.net
        this.sdsForm.loc = this.options.result.loc
        this.sdsForm.comp = ['Z']
        this.loadedOption = val.y_date
        this.options.sta = []
        this.generateTransferList()
      }, (error)  =>  {
        console.log('error');
                      })
    },
    getYearAvail() {
      console.log('year')
      axios.post("ws/year", {}).then((response)  =>  {
        this.validDate = response.data.result
        console.log('year')
      }, (error)  =>  {
        console.log('error');
                      })
    },
    getData (val) {
      this.sdsForm = val
      this.activeTable = true
      this.activeIndex = '2'
      this.dataTable.loading = true;
      axios.post("ws/get_data", this.sdsForm)
      .then((response)  =>  {
        this.dataTable.data = response.data;
        this.dataTable.loading = false;
      }, (error)  =>  {
        this.dataTable.loading = false
        console.log('error');
                      })
    },
    storeSettings () {
        let toStore = {}
        for (let [k, v] of Object.entries(this.settings)) {
          if (v.value != v.default) {
            toStore[k] = v.value
          }
        }
        localStorage.setItem(STORAGE_KEY, JSON.stringify(toStore))
        this.$notify.success({ message: 'Settings successfully saved' })
        this.initStyle()
      },
    initStyle () {
        let color = {}
        for (let [key, field] of Object.entries(this.settings)) {
           let [mainKey, subKey] = key.split('.')
           color[subKey] = field.value
        }
        let styleId = 'table-style';
        let styleEl = document.getElementById(styleId)
        if (styleEl != null) {
          styleEl.parentNode.removeChild(styleEl)
        }

        let s = document.createElement('style');
        s.id = styleId;
        s.innerHTML = `
        .pover { background-color: ${color.pover} !important;
                    }
        .no_data { background-color: ${color.no_data} !important;
                    }
        .p100 { background-color: ${color.p100} !important;
                    }
        .p99_100 { background-color: ${color.p99_100} !important;
                    }
        .p90_99 { background-color: ${color.p90_99} !important;
                     }
        .p75_90 { background-color: ${color.p75_90} !important;
                    }
        .p50_75 { background-color: ${color.p50_75} !important;
                  }
        .p25_50 { background-color: ${color.p25_50} !important;
                    }
        .p0_25 { background-color: ${color.p0_25} !important;
                    }`;

        document.head.appendChild(s);

},

    loadSettings () {
      let storedSettings = localStorage.getItem(STORAGE_KEY)
      storedSettings = storedSettings != null ? JSON.parse(storedSettings) : {}
      for (let [key, defaultValue] of Object.entries(settings)) {
        let storedValue = storedSettings[key]
        this.$set(this.settings, key, {
          default: defaultValue,
          value: storedValue != null ? storedValue : defaultValue
        })
      }
    },
    julianToDatetime(julian_day, year) {
        let d = new Date()
        d.setTime(Date.UTC(year, 0 , 1, 0, 0, 0, 0))
        d.setUTCDate(julian_day)
        return d
    },
    initColorProgress () {
      for (let [key, field] of this.dataTable.data.result.entries() ){
        // let field = this.dataTable.data.result[f]
        console.log(field.avg)
        if (field.avg >= 99.99) {
          this.dataTable.data.result[key].coloravg = this.settings['tableColor.p100'].value
        } else if (field.avg < 99.99 && field.avg >= 99) {
          this.dataTable.data.result[key].coloravg = this.settings['tableColor.p99_100'].value
        } else if (field.avg < 99 && field.avg >= 90) {
          this.dataTable.data.result[key].coloravg = this.settings['tableColor.p90_99'].value
        } else if (field.avg < 90 && field.avg >= 75) {
          this.dataTable.data.result[key].coloravg = this.settings['tableColor.p75_90'].value
        } else if (field.avg < 75 && field.avg >= 50) {
          this.dataTable.data.result[key].coloravg = this.settings['tableColor.p50_75'].value
        } else if (field.avg < 50 && field.avg >= 25) {
          this.dataTable.data.result[key].coloravg = this.settings['tableColor.p25_50'].value
        } else if (field.avg < 25 && field.avg > 0) {
          this.dataTable.data.result[key].coloravg = this.settings['tableColor.p0_25'].value
        } else {
          this.dataTable.data.result[key].coloravg = this.settings['tableColor.no_data'].value
        }
      }
    },
    generateTransferList(){
      let sta = this.options.result.station
      for (let i = 1; i <= sta.length - 1; i++) {
        this.options.sta.push({
          key: i,
          label: sta[i],
          disabled: false
        });
      }
    },
    loadInfos: function (val) {
      this.detail = val
      axios.post('ws/day', this.detail).then((response)  =>  {
        this.infos.data = response.data;
        if (this.infos.data.status == 'error') {
          this.$notify.info('No Data Available')
        } else {
          this.infos.gapList = response.data.result.Gap.PeriodList.map(x => Object.assign(x, { color: '#ff0000' }))
          this.detail.active = true
          this.infos.visible = true
        }
      }, (error)  =>  {
        this.infos.visible = false
        console.log('error');
      })
    },

    loadStation: function (val) {
      this.showStationGraph = true
      this.station.sta_info = val
      this.station.sta_info.y_date = this.sdsForm.y_date
      this.loading = true
      axios.post('ws/station', this.station.sta_info).then((response)  =>  {
        this.station.data = response.data;
        if (this.station.data.status == 'error') {
          this.$notify.error(this.station.data.message)
        } else {
          this.station.visible = true
          this.station.average = []
          this.station.max = []
          this.station.min = []
          this.station.rms = []
          this.station.stddev = []

          for (let index in this.dataTable.data.keys ) {
            let key = this.dataTable.data.keys[index]
            let day_date = (this.julianToDatetime(key.split(".")[1],
            key.split(".")[0]).getTime())

            if (this.station.data.result[key] == null) {
              this.station.average.push([ day_date, null ])
              this.station.max.push([ day_date, null ])
              this.station.min.push([ day_date, null ])
              this.station.rms.push([ day_date, null ])
              this.station.stddev.push([ day_date, null ])
            } else {
              let val = this.station.data.result[key]
              this.station.average.push([ day_date, val.DataMetrics.Avg ])
              this.station.max.push([ day_date, val.DataMetrics.Max ])
              this.station.min.push([ day_date, val.DataMetrics.Min ])
              this.station.rms.push([ day_date, val.DataMetrics.Rms ])
              this.station.stddev.push([ day_date, val.DataMetrics.Stddev ])
            }
          }

          let sortByFirstElement = (a, b) => {
            a = a[0]
            b = b[0]
            return a == b ? 0 : a < b ? -1 : 1
          }

          this.station.average.sort(sortByFirstElement)
          this.station.min.sort(sortByFirstElement)
          this.station.max.sort(sortByFirstElement)
          this.station.rms.sort(sortByFirstElement)
          this.station.stddev.sort(sortByFirstElement)
          this.station = Object.assign({}, this.station)
          this.loading = false
        }
      }, (error)  =>  {
        this.station.visible = false
        console.log('error');
      })
    }
  }
}

</script>

<style>

  body {
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    font-size: 13px;
    line-height: 1.42857143;
    color: #333;
    background-color: #fff;
    padding: 0;
    margin: 0;
  }

  .el-header {
    background-color: #545c64;
    color: #333;
    text-align: left;
    line-height: 60px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .el-main {
    background-color: #ffffff;
    color: #333;
    line-height: 110px;
  }

  body > .el-container {
    /*margin-bottom: 40px;*/
  }


  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

.el-collapse-item__header {
    font-size: large;}

.cursor-pointer {
  cursor: pointer;
}
</style>
