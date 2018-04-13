<template>
  <div>
    <button id="btn" class="" v-on:click="getData">Get Data</button>
    <h3  v-if="table.loading == false" >Not loaded</h3>
    <el-table
      v-if="table.loading"
      :data="table"
      style="width: 100%">
      <el-table-column
        prop="station"
        label="Stations"
        width="180">
      </el-table-column>
      <el-table-column
        prop="network"
        label="Network"
        width="180">
      </el-table-column>
      <el-table-column
        prop="cha"
        label="Channel">
      </el-table-column>
 </el-table>
    <h3   >{{ table.data.status }}</h3>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    data () {
      return {
        table: {
          data: '',
          loading: false
     }
   };
 },
    methods: {
      getData: function () {
        console.log('click');
        this.table.loading = true;
        axios.get("ws/get_data?sds=ecuador&start=100,2016&end=110,2016")
        .then((response)  =>  {
          this.loading = false;
          this.table.data = response.data;
        }, (error)  =>  {
          this.table.loading = false
          console.log('error');
        })
      }
    }
  }
</script>
