<template>
  <el-container>
    <el-header>
      <device-header></device-header>
    </el-header>
    <el-container>
        <el-aside width="200px">
          <device-aside></device-aside>
        </el-aside>
        <el-main>
          <display-legend></display-legend>
          <device-form></device-form>
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
