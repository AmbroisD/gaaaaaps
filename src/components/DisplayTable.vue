<template>
  <div>
     <data-tables
      id="table"
      v-loading="value.loading"
      :pagination-props="{ pageSizes: [15, 20, 30, 50] }"
      :table-props="{ cellClassName: handleCellClassName }"
      @cell-click="activeCell"
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
        :label="value.data.result[0][key].info.date"
        width="20">
        <template slot-scope="scope"></template>
      </el-table-column>

    </data-tables>
    <div  id="detail" v-if="detail.active">
      <el-collapse
        id="detail"
        v-if="detail.active"
        v-model="activeNames"
        @change="handleChange">
        <el-collapse-item title="Station infos" name="1">
          <div>
            <ul>
              <li>Station : {{ detail.station }}</li>
              <li>Network : {{ detail.network }}</li>
              <li>Location : {{ detail.location }}</li>
              <li>Channel : {{ detail.cha }}</li>
            </ul>
          </div>
        </el-collapse-item>
        <el-collapse-item title="Data information" name="2">
          <div></div>
        </el-collapse-item>
        <el-collapse-item title="Data quality" name="3">
          <div></div>
        </el-collapse-item>
      </el-collapse>
    </div>
  </div>
</template>

<script>
  export default {
    data () {
      return {
          activeNames: ['1','2'],
          detail: {
            active: false
          }
   };
 },
    props: ['value', 'settings'],
    methods: {
      handleCellClassName (ev) {
        let result = []
        if (['station', 'network', 'cha'].indexOf(ev.column.property) >= 0) {
          result.push('cell-header')
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
      activeCell (row, column, cell, event) {
        if (['station', 'network', 'cha'].indexOf(column.property) <= 0) {
          console.log(row, column, cell, event)

          this.detail = Object.assign({}, this.detail, {
            active: true,
            station:row.station,
            network: row.network,
            cha: row.cha,
            location: row.location,
            day: [column.property, column.label]
          })
        }
      },
      // selectCells (row, column, cell, event) {
      //   if (['station', 'network', 'cha'].indexOf(column.property) <= 0) {
      //     console.log(row, column, cell, event);
      //     // let target = document.getElementById(column.id)
      //     this.addClass(cell, 'active');
      //            }
      // },
      renderHeader (h, { column }) {
      return h('div', { 'class': 'rotate' }, column.label)
    },
    handleChange(val) {
        console.log(val);
      }
   }
 }
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

td.cell-data {
  border: 1px solid #333;
  border-  width: 20px;
  height: 20px;
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

#detail {
  line-height: 15px;
  margin: 0 auto;
  width: 90%
}

</style>
