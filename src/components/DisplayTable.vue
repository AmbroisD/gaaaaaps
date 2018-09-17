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
        <template slot-scope="scope">
          <i
            v-if="value.data.result[0][key].info.comment != null"
            class="el-icon-info center-icon">
          </i>
        </template>
      </el-table-column>
    </data-tables>
    <div
      class="center"
      v-if="infoDay != null">
      <ul class="inline" >
        <li class="list" >{{ infoDay.day }}</li>
        <li class="list" >{{ infoDay.network }}.{{ infoDay.station }}.{{ infoDay.cha }}</li>
        <li class="list" >Percent : {{ infoDay.percent }}%</li>
      </ul>
    </div>
    <el-button v-if="mode == 'admin'" class="buttonform" @click.prevent="addComment = true">Add comment</el-button>
    <div
      class="add-comment"
      v-if="addComment">
      <h3>Station selected</h3>
      <ul>
        <li
          v-for="day in selectedDay"
          class="list" >{{ day.network }}.{{ day.station }}.{{ day.cha }} : {{ day.day[1] }} 
        </li>
      </ul>
      <h3>Status</h3>
          <el-radio v-model="status" label="1">
           Info
           <i
           class="el-icon-info center-icon">
           </i>
         </el-radio>
         <el-radio v-model="status" label="2">
           Warning
           <i
           class="el-icon-warning center-icon">
           </i>
         </el-radio>
         <el-radio v-model="status" label="3">
           Question
           <i
           class="el-icon-question center-icon">
           </i>
         </el-radio>
      <h3>Your comment</h3>
      <el-input type="textarea" v-model="comment"></el-input>
      <el-button class="buttonform buttoncomment" type="primary" @click.prevent="updateComment()">Submit</el-button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
  export default {
    data () {
      return {
        status: null,
        selectedDay: [],
        comment: null,
        addComment: false,
        infoDay: null
   };
 },
    props: ['value', 'settings', 'infos', 'detail', 'station', 'mode'],
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
        for (let day of this.selectedDay) {
          if (this.addComment) {
            let checkRow = true
            let checkColumn = true
            let rowToCheck = ['station', 'network', 'cha', 'location']
            let columnToCheck = ['property', 'label']
            for (let k of rowToCheck) {
              if (day[k] != ev.row[k]) {
                checkRow = false
                break
              }
            }
            for (let [i, k] of columnToCheck.entries()) {
              if (day.day[i] != ev.column[k]) {
                checkColumn = false
                console.log(false)
                break
              }
            }
            if (checkRow && checkColumn) {
              result.push('selected')
            }
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
        if (this.addComment) {
          this.selectCells(row, column, cell, event)
        } else {
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

          this.$emit('dayActive', new_detail)
        }
        if (['station'].indexOf(column.property) == 0) {
          this.activeStation(row)
        }
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

      selectCells (row, column, cell, event) {
          if (['station', 'network', 'cha'].indexOf(column.property) <= 0) {
            // let checkRow = true
            // let index = 0
            // let rowToCheck = ['station', 'network', 'cha', 'location']
            // if ( this.selectedDay.length != 0 ) {
            //   for (let [i, day] of this.selectedDay.entries()) {
            //     console.log(i)
            //     console.log(day)
            //     for (let k of rowToCheck) {
            //       if (day[k] != row[k]) {
            //         checkRow = false
            //         break
            //       }
            //     }
            //   index = i
            //   console.log(index)
            //   }
            //   if (checkRow == false) {
            //     this.selectedDay.remove(index)
            //   // let target = document.getElementById(column.id)
            //   } else {
            this.selectedDay.push({ 'network': row.network,
                                    'station': row.station,
                                    'cha': row.cha,
                                    'location': row.location,
                                    'day': [column.property, column.label]})
        //     }
        //   }
        }
      },
      renderHeader (h, { column }) {
      return h('div', { 'class': 'rotate' }, column.label)
      }
   }
 }
</script>

<style>


.el-table .cell {
  /* padding-left: 0px; */
  line-height: 20px;
  /* border-bottom: 0px; */
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
  border-bottom: 0px;
}

.el-table--small td, .el-table--small th {
  /* padding: 0 0 */
}


th.rotate {
  height: 60px;
  white-space: nowrap;
}

div.rotate {
  transform:
    translate(6px, 40px)
    rotate(-90deg);
  width: 5px;
}


td.cell-data:hover {
  box-shadow: inset 0 0 0 2px black;
}

td.cell-data.active {
  box-shadow: inset 0 0 0 2px red;
}

td.cell-data.selected {
  box-shadow: inset 0 0 0 2px blue;
}

/* .main-table, .main-table td {
  border-collapse: collapse;
  border: 1px solid black;
} */
.cell-header {
  border: 0;
}

/* .el-table__body,
.el-table__footer,
.el-table__header {
  border-collapse: collapse;
} */

.el-table--striped .el-table__body tr.el-table__row--striped.current-row td,
.el-table__body tr.current-row>td,
.el-table__body tr.hover-row.current-row>td,
.el-table__body tr.hover-row.el-table__row--striped.current-row>td,
.el-table__body tr.hover-row.el-table__row--striped>td,
.el-table__body tr.hover-row>td {
  background-color: rgba(255, 255, 255, 0.3);
}

#table .el-table__body,
#table .el-table__footer,
#table .el-table__header,
#table table,#table table td {
  border-collapse: collapse;
  /* border: 1px solid transparent; */
}

#table table td.cell-data {
  /* border-collapse: collapse; */
  border: 1px solid black;
}
.el-table--small td {
  padding: 0;
}
.el-table td {
  padding: 0;
  position: inherit;
}

#table {
  margin: 0 auto;
}

.inline li{
  font-size: medium;
  display:inline;
  padding : 0 1em;
 }

.inline li.list:before {
  content: '\ffed';
  margin-right: 0.5em;

}
.center {
  text-align: center;
  line-height: 0px;
  font-size: 20px;
}
.center-icon {
  padding-left: 3px;
}
.add-comment {
  line-height: 15px;
  margin: 0 auto;
  width: 60%

}
.buttoncomment {
    margin-top: 12px;
}

.el-pagination {
    line-height: 0;
}

</style>
