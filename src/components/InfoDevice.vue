<template>
  <div  id="detail">
    <h2 class="center">{{ detail.day[1] }}</h2>
    <el-collapse
      id="detail"
      v-if="detail.active"
      v-model="activeNames"
      @change="handleChange">
      <el-collapse-item title="Station infos" name="1">
        <div>
          <ul class="inline" >
            <li class="list" >Station : {{ detail.station }}</li>
            <li class="list" >Network : {{ detail.network }}</li>
            <li class="list" >Location : {{ detail.location }}</li>
            <li class="list" >Channel : {{ detail.cha }}</li>
          </ul>
        </div>
      </el-collapse-item>
      <el-collapse-item title="Data availability" name="2">
        <div>
          <day-plot id="data-canvas" :value="infos.gapList" style="width: 90%; height: 100px;"></day-plot>
          <ul class="inline" >
            <li class="list" >Percent of data : {{ detail.percent }} %</li>
            <li class="list" >Nb Gaps : {{ detail.gaps }} ({{ detail.total_gap }} s in total)</li>
            <li class="list" >Nb Overlaps : {{ detail.overlap }}</li>
          </ul>
        </div>
      </el-collapse-item>
      <el-collapse-item title="Data quality" name="3">
        <div v-if="infos.visible == true" >
          <el-table
           id="table_data_metric"
           :data="dataMetrics"
           style="width: 90%">
           <el-table-column
             prop="Average"
             label="Average">
           </el-table-column>
           <el-table-column
             prop="Max"
             label="Max">
           </el-table-column>
           <el-table-column
             prop="Min"
             label="Min">
           </el-table-column>
           <el-table-column
             prop="Rms"
             label="Rms">
           </el-table-column>
           <el-table-column
             prop="Stddev"
             label="Stddev">
           </el-table-column>
         </el-table>
        </div>
      </el-collapse-item>
      <el-collapse-item title="List Gaps" name="4">
        <div>
          <ul>
            <li
            v-for="gap in infos.data.result.Gap.PeriodList.slice(0, detail.gaps)"
            class="list" >Start : {{ gap['StartTime'] }} - End  : {{ gap['EndTime'] }}</li>
          </ul>
        </div>
      </el-collapse-item>
      <el-collapse-item title="List Overlaps" name="5">
        <div>
          <ul>
            <li v-for="overlap in infos.data.result.Overlap.PeriodList"
            class="list" >Start : {{ overlap['StartTime'] }} - End  : {{ overlap['EndTime'] }}</li>
          </ul>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
export default {
  data () {
    return {
      activeNames: ['1','2','3'],
      dataMetrics: []
           };
         },
  props: ['infos', 'detail'],
  mounted () {
  this.dataMetrics.push({
          Average : this.infos.data.result.DataMetrics.Avg.toFixed(2),
          Max : this.infos.data.result.DataMetrics.Max.toFixed(2),
          Min : this.infos.data.result.DataMetrics.Min.toFixed(2),
          Rms : this.infos.data.result.DataMetrics.Rms.toFixed(2),
          Stddev : this.infos.data.result.DataMetrics.Stddev.toFixed(2)
        })
  },
  methods: {
    handleChange(val) {
      console.log(val);
       }
     }
   }

 // export default {
 //   data () {
 //     return {
 //         infos: {visible: false,
 //                 data:{},
 //                 canvas:[]},
 //         activeNames: ['1','2'],
 //            };
 //       }
 //   }
</script>

<style>

h2.center {
  text-align: center;
  width: 90%
}

#detail {
  line-height: 15px;
  margin: 0 auto;
  width: 90%
}

#data-canvas {
  margin: 0 auto;
  width: 90%
}

#table_data_metric div.cell {
  line-height: 30px;
  width: 90%;
  font-size: medium;

}

.inline li{
font-size: medium;
display:inline;
padding : 0 1em; }

.inline li.list:before {
  content: '\ffed';
  margin-right: 0.5em;
}
</style>
