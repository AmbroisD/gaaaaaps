<template>
  <div>
     <data-tables
      id="table"
      v-loading="value.loading"
      :pagination-props="{ pageSizes: [15, 20, 30, 50] }"
      :table-props="{ cellClassName: handleCellClassName }"
      @cell-click="activeCell"
      @cell-mouse-enter="displayInfo"
      :data="value.data.result"
      style="width: 90%"
      height="500">
      <el-table-column
        fixed
        prop="station"
        label="Stations"
        sortable
        width="80">
      </el-table-column>
      <el-table-column
        fixed
        prop="network"
        label="Network"
        sortable
        width="80">
      </el-table-column>
      <el-table-column
        fixed
        prop="cha"
        label="Channel"
        sortable
        width="80">
      </el-table-column>
      <el-table-column
        v-for="key in value.data.keys"
        :render-header="renderHeader"
        :prop="key"
        :key="key"
        :label="value.data.result[0][key].info.date"
        width="20">
        <template slot-scope="scope"></template>
      </el-table-column>
    </data-tables>
    <div
      class="center"
      v-if="infoDay != null">
      <ul class="inline" >
        <li class="list" >Date : {{ infoDay.day }}</li>
        <li class="list" >Network : {{ infoDay.network }}</li>
        <li class="list" >Station : {{ infoDay.station }}</li>
        <li class="list" >Channel : {{ infoDay.cha }}</li>
        <li class="list" >Percent : {{ infoDay.percent }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
  export default {
    data () {
      return {
        infoDay: null
   };
 },
    props: ['value', 'settings','infos','detail', 'station'],
    methods: {
      handleCellClassName (ev) {
        let result = []
        if (['station', 'network', 'cha'].indexOf(ev.column.property) >= 0) {
          result.push('cell-header')
          if (ev.column.property == 'station') {
            result.push('cursor-pointer')
          }
        } else {
          result = result.concat(['cell-data', ev.row[ev.column.property].color])
        }
        if (this.detail.active) {
          let checkRow = true
          let checkColumn = true
          let rowToCheck = ['station', 'network', 'cha', 'location']
          let columnToCheck = ['property', 'label']
          for (let k of rowToCheck) {
            if (this.detail[k] != ev.row[k]) {
              checkRow = false
              break
            }
          }
          for (let [i, k] of columnToCheck.entries()) {
            if (this.detail.day[i] != ev.column[k]) {
              checkColumn = false
              break
            }
          }
          if (checkRow && checkColumn) {
            result.push('active')
          }
        }
        return result.join(' ')
      },
      displayInfo (row, column, cell, event) {
        if (['station', 'network', 'cha'].indexOf(column.property) < 0) {
          console.log(['station', 'network', 'cha'].indexOf(column.property))
          this.infos.visible = false

          this.infoDay = {
            active: true,
            station:row.station,
            network: row.network,
            cha: row.cha,
            percent:row[column.property].info.percent,
            day: column.label
          }
        }
      },
      activeCell (row, column, cell, event) {
        if (['station', 'network', 'cha'].indexOf(column.property) < 0) {
          console.log(['station', 'network', 'cha'].indexOf(column.property))
          this.infos.visible = false

          var new_detail = Object.assign({}, this.detail, {
            active: false,
            station:row.station,
            network: row.network,
            cha: row.cha,
            location: row.location,
            gaps: row[column.property].info.gaps,
            percent:row[column.property].info.percent,
            day: [column.property, column.label],
            total_gap:row[column.property].info.total_gap,
            overlap:row[column.property].info.overlap
          })
          // this.$emit('detail', new_detail)
          this.$emit('dayActive', new_detail)
        }
        if (['station'].indexOf(column.property) == 0) {
          this.activeStation(row)
        }
      },
      activeStation (row) {
        var focus_station = Object.assign({}, this.station, {
          active: false,
          station:row.station,
          network: row.network,
          cha: row.cha,
          location: row.location
        })
        this.$emit('station', focus_station)
        this.$emit('stationActive', focus_station)

      },

      renderHeader (h, { column }) {
      return h('div', { 'class': 'rotate' }, column.label)
      }
   }
 }
 // selectCells (row, column, cell, event) {
 //   if (['station', 'network', 'cha'].indexOf(column.property) <= 0) {
 //     console.log(row, column, cell, event);
 //     // let target = document.getElementById(column.id)
 //     this.addClass(cell, 'active');
 //            }
 // },
</script>

<style>


.el-table .cell {
  padding-left: 0px;
  line-height: 20px;
  border-bottom: 0px;
}

.el-table .cell, .el-table th div {
  padding-right: 0px;
  overflow: visible;
}

.el-table .cell, .el-table th div, .el-table--border td:first-child .cell, .el-table--border th:first-child .cell {
    padding-left: 0px;
}

.el-table td {
  padding-left: 0px;
  border-bottom: 0px;}

.el-table--small td, .el-table--small th {padding: 0 0}


th.rotate {

  height: 60px;
  white-space: nowrap;
}

div.rotate {
  transform:
    /* code hardcode */
    translate(6px, 40px)
    /* 45 est egale 360 - 45 */
    rotate(-90deg);
  width: 5px;
}

div.cell {
 /* border-collapse: collapse; */
}


td.cell-data:hover {
  box-shadow: inset 0 0 0 2px black;
  /* border-width: 2px;
  border-color: black; */
}

td.cell-data.active {
  box-shadow: inset 0 0 0 2px red;
  /* border-width: 2px;
  border-color: red; */
}

.main-table, .main-table td {
  border-collapse: collapse;
  border: 1px solid black;
}
.cell-header {border: 0;}

.el-table__body,
.el-table__footer,
.el-table__header {
  border-collapse: collapse;
}

.el-table--striped .el-table__body tr.el-table__row--striped.current-row td,
.el-table__body tr.current-row>td,
.el-table__body tr.hover-row.current-row>td,
.el-table__body tr.hover-row.el-table__row--striped.current-row>td,
.el-table__body tr.hover-row.el-table__row--striped>td,
.el-table__body tr.hover-row>td {
  background-color: rgba(255, 255, 255, 0.3);
}

#table {
  /* display: table; */
  margin: 0 auto;
}

td.cell-data {
  border: 1px solid #333;
  position: relative;
  /* border-width: 20px; */
  height: 20px;
  border-collapse: collapse;
}
.inline li{
font-size: medium;
display:inline;
padding : 0 1em; }

.inline li.list:before {
  content: '\ffed';
  margin-right: 0.5em;

}
.center{
  text-align: center;
  line-height: 0px;
  font-size: 20px;
}
</style>
