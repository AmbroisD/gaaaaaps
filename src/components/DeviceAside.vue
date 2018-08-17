<template>
  <el-menu
    :default-active="value"
    class="el-menu-vertical-demo"
    @select="handleSelect"
    background-color="#D3DCE6"
    text-color="#545b64"
    active-text-color="#569bff">
    <el-menu-item index="1">
      <i class="el-icon-edit"></i>
      <span>Form</span>
    </el-menu-item>
    <el-submenu index="2" :disabled="table == false">
      <template slot="title">
        <i class="el-icon-menu"></i>
        <span>Data availability</span>
      </template>
      <el-menu-item-group>
        <el-menu-item index="2">By day</el-menu-item>
        <el-menu-item index="4">Average</el-menu-item>
      </el-menu-item-group>
    </el-submenu>
    <el-menu-item index="3">
      <i class="el-icon-info"></i>
      <span> About</span>

    </el-menu-item>
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
