<template>
  <el-container style="height: 100vh;">
    <el-header>
      <device-header v-model="indexHeader" ></device-header>
    </el-header>
    <el-container>
      <device-aside :table="activeTable" v-on:goHome="indexHeader = 'home'" v-model="activeIndex"></device-aside>
        <el-main class="datatable-style" v-if="indexHeader == 'home'">
          <device-form v-model="sdsForm" v-on:submitForm="getData" v-if="activeIndex == '1'"></device-form>
          <display-legend v-if="activeIndex == '2'"></display-legend>
          <display-table :settings="settings" v-model="dataTable" v-if="activeIndex == '2'"></display-table>
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
</template>

<script>
import settings from './settings.json'
import axios from 'axios'

const STORAGE_KEY = 'settings'


export default {
  data() {
    return {
      settings: {},
      indexHeader: 'home',
      activeIndex: '1',
      activeTable: false,
      dataTable: {data: '',
                  loading: false},
      sdsForm: {}
    };
  },
  mounted () {
  this.loadSettings()
  this.initStyle()
  },
  methods: {
    getData: function () {
      console.log('click');
      this.activeTable = true
      this.activeIndex = '2'
      this.dataTable.loading = true;
      axios.get("ws/get_data?sds=ecuador&start=100,2016&end=210,2016")
      .then((response)  =>  {
        this.dataTable.data = response.data;
        this.dataTable.loading = false;
        // this.$emit('input', this.data)
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
        // color[key.split('.')[0]]: storedValue != null ? storedValue : defaultValue
      }
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

  /* .pover, .cellpover { background-color: #75cae6 !important;
              }
  .no_data, .cellno_data { background-color: #f8f8f8 !important;
              }
  .p100, .cellp100 { background-color: #6ec47e !important;
              }
  .p99-100, .cellp99-100 { background-color: #a7d380 !important;
              }
  .p90-99, .cellp90-99 { background-color: #cfdf83 !important;
               }
  .p75-90, .cellp75-90 { background-color: #f7eb85 !important;
              }
  .p50-75, .cellp50-75 { background-color: #fcaa79 !important;
            }
  .p25-50, .cellp25-50 { background-color: #fb9d9d !important;
              }
  .p0-25, .cellp0-25 { background-color: #d59bd6 !important;
              } */

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
