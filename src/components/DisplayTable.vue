<template>
  <el-table
    :data="tableData"
    style="width: 100%">
    <el-table-column
      v-for="station in sds">{{ user.name }}
      prop="date"
      label="Date"
      width="180">
    </el-table-column>
  </el-table>
</template>



<scripts>
data: {
    sds: []
},
axios.get('ws/get_data', {
    params: {
      start : 100,
        end : 110,
        sds : 'ecuador',
        year: 2016,
        net : '*',
        sta : '*',
    }
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
</scripts>
