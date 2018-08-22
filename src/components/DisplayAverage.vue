<template>
  <div>
    <h1 class="center">Percent average on the time period</h1>
    <display-legend></display-legend>
    <data-tables
     id="table-process"
     v-loading="value.loading"
     :pagination-props="{ pageSizes: [15, 20, 30, 50] }"
     :data="value.data.result"
     style="width: 70%"
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
       prop="avg"
       label='Percent Average'
       sortable
       width="500">
       <template slot-scope="scope">
         <el-progress
           class="row-progress test"
           :text-inside="true"
           :stroke-width="18"
           :percentage="scope.row.avg"
           :color="scope.row.coloravg">
         </el-progress>
       </template>
     </el-table-column>
   </data-tables>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        show: false,
        color:''
   };
  },
  props: ['value', 'settings']
  }


</script>

<style>
.progress-bar {
  line-height: 12px;
}
.row-progress {
  /* display: table; */
  display: block;
  font-size: 13px;
  padding-left: 12px;
  top: 0;
  right: 8px;
}
#table-process {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 40%;
}
.center{
  text-align: center;
  line-height: 50px;
  font-size: 25px;
}
.test svg > path:first-of-type{
  stroke: red !important;
}
</style>
