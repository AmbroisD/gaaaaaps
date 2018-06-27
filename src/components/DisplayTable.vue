<template>
  <div>
    <button id="btn" class="" v-on:click="getData">Get Data</button>
    <h3  v-if="table.loading == false" >Not loaded</h3>
    <el-table
      v-if="table.loading"
      :data="table.data.result"
      style="width: 70%"
      height="500">
      <el-table-column
        fixed
        prop="station"
        label="Stations"
        width="80">
      </el-table-column>
      <el-table-column
        fixed
        prop="network"
        label="Network"
        width="80">
      </el-table-column>
      <el-table-column
        fixed
        prop="cha"
        label="Channel"
        width="80">
      </el-table-column>
      <el-table-column
        v-for="key in table.data.keys"
        :prop="key"
        :label="key"
        width="20">
        <template scope="scope">
          <div :class="scope.row[key].color"></div>
        </template>
      </el-table-column>

    </el-table>
    <h3
      v-if="table.loading">{{ table.data.status }}</h3>
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

<style>

.el-table .cell {
  padding-left: 0px;
  line-height: 20px;
  border-bottom: 0px;
}

.el-table td {
  padding-left: 0px;
  border-bottom: 0px;}

.el-table--small td, .el-table--small th {padding: 0 0}

.cellpover { background-color: black;
            border: 1px solid #333;
            width: 20px;
            height: 20px;}
.cellno_data { background-color: #DBDBDB;
            border: 1px solid #333;
            width: 20px;
            height: 20px;}
.cellp100 { background-color: #393;
            border: 1px solid #333;
            width: 20px;
            height: 20px;}
.cellp99-100 { background-color: #90EE90;
            border: 1px solid #333;
            width: 20px;
            height: 20px;}
.cellp90-99 { background-color: #33F;
            border: 1px solid #333;
            width: 20px;
            height: 20px; }
.cellp75-90 { background-color: #ADD8E6;
            border: 1px solid #333;
            width: 20px;
            height: 20px;}
.cellp50-75 { background-color: #FFB733;
            border: 1px solid #333;
            width: 20px;
            height: 20px;}
.cellp25-50 { background-color: #939;
            border: 1px solid #333;
            width: 20px;
            height: 20px;}
.cellp0-25 { background-color: #F33;
            border: 1px solid #333;
            width: 20px;
            height: 20px;}

</style>
