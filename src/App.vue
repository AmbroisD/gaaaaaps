<template>
  <el-container style="height: 100vh;">
    <el-header>
      <device-header></device-header>
    </el-header>
    <el-container>
        <device-aside v-model="activeIndex"></device-aside>
        <el-main>
          <device-form v-if="activeIndex == '1'"></device-form>
          <display-legend v-if="activeIndex == '2'"></display-legend>
          <display-table v-if="activeIndex == '2'"></display-table>
        </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      activeIndex: '1'
    };
  },
  methods: {
  }
}

</script>

<style>

  body {
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    font-size: 13px;
    line-height: 1.42857143;
    color: #333;
    background-color: #fff;
    padding: 0;
    margin: 0;
  }

  .el-header {
    background-color: #545c64;
    color: #333;
    text-align: left;
    line-height: 60px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    line-height: 160px;
  }

  body > .el-container {
    /*margin-bottom: 40px;*/
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
