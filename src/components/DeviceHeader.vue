<template>
  <el-menu
    :default-active="value"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
    background-color="#545c64"
    text-color="#fff"
    active-text-color="#ffd04b">
    <el-menu-item index="gaps">Gaaaaaps</el-menu-item>
    <el-menu-item index="home">Home</el-menu-item>
    <el-menu-item index="userSettings" class="pull-right"><i class="el-icon-setting"></i></el-menu-item>
  </el-menu>
</template>

<script>
  export default {
    props: ['value'],
    methods: {
      handleSelect(key, keyPath) {
        this.$emit('input', key)
        console.log(key, keyPath);
      }
    }
  }
</script>

<style>

.el-menu-item.pull-right {
  float: right;
}

</style>
