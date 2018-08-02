<template>
  <el-menu
    :default-active="value"
    class="el-menu-vertical-demo"
    @select="handleSelect"
    background-color="#D3DCE6"
    text-color="#545b64"
    active-text-color="#569bff">
    <el-menu-item index="1">Form</el-menu-item>
    <el-menu-item index="2" :disabled="table == false">Data availability</el-menu-item>
    <el-menu-item index="3">About</el-menu-item>
  </el-menu>
</template>

<script>
  export default {
    props: ['value', 'table'],
    methods: {
      handleSelect(key, keyPath) {
        this.$emit('input', key)
        this.$emit('goHome')
        console.log(key, keyPath);
      }
    }
  }
</script>

<style>
</style>
