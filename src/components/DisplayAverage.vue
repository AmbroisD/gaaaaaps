<template>
  <div>
    <data-tables
     id="table"
     v-loading="value.loading"
     :pagination-props="{ pageSizes: [15, 20, 30, 50] }"
     :data="value.data.result"
     width="700"
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
       width="400">
       <template slot-scope="scope">
         <el-progress
           class="row-progress"
           :text-inside="true"
           :stroke-width="18"
           :percentage="50"
           color="rgba(142, 113, 199, 0.7)">
         </el-progress>
         <h3>{{ scope.row.avg }}</h3>
       </template>
     </el-table-column>
   </data-tables>
  </div>
</template>

<script>
  export default {
    data () {
      return {
   };
  },
  props: ['value']
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
  color: #fff;
  padding-top : 12px;
  top: 0;
  right: 8px;
}
.progress-title {
      padding-left: 30%;
}
</style>
