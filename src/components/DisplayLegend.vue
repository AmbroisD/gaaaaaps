<template>
  <div id="legend-block">
    <table id="table-legend">
      <tbody>
        <tr>
          <td class="legend">
            <div class="color p100"></div> 100 %
          </td>
          <td class="legend">
            <div class="color p99_100"></div> 99 - 100 %
          </td>
          <td class="legend">
            <div class="color p90_99"></div> 90 - 99 %
          </td>
          <td class="legend">
            <div class="color p75_90"></div> 75 - 90 %
          </td>
        </tr>
        <tr>
          <td class="legend">
            <div class="color p50_75"></div> 50 - 75 %
          </td>
          <td class="legend">
            <div class="color p25_50"></div> 25 - 50 %
          </td>
          <td class="legend">
            <div class="color p0_25"></div> 0 - 25 %
          </td>
          <td class="legend">
            <div class="color no_data"></div> No data
          </td>
        </tr>
      </tbody>
    </table>
    <div id="inset-label">Legend</div>
  </div>
</template>

<script>

</script>

<style>

#legend-block {
  line-height: 10px;
  border: 1px solid;
  padding: 5px;
  position: relative;
  /*margin-top: 40px;*/
  margin: 40px auto 0 auto;
  width: 45%;
}
#table-legend {
  width: 100%
}
#table-legend td {
  padding: 5px;
}

#inset-label {
  padding: 2px 5px;
  position: absolute;
  z-index: 1;
  background-color: #ffffff;
  left: 30px;
  top: -1em;
}

#legend-block div.color {
  display: inline-block;
  vertical-align: middle;
  border: 1px solid gray;
  margin-right: 10px;
  width: 60px;
  height: 20px;
}

#legend-block td.legend {
  /*width: 20%;*/
}

</style>
