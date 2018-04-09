<template>
  <el-container>
    <el-header>Gaaaaaps</el-header>
    <el-container>
        <el-aside width="200px">Menu</el-aside>
        <el-main id="app">
          <el-button @click="visible = false">Legend</el-button>
          <display-legend :visible.sync="visible" ></display-legend>
          <h1>Data avaibility</h1>
          <p></p>
        </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'app'
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
    background-color: #B3C0D1;
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
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
