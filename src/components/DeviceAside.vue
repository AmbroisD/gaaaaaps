<template>
  <el-menu
    :collapse="isCollapse"
    :default-active="value"
    class="el-menu-vertical-demo"
    @select="handleSelect"
    background-color="#D3DCE6"
    text-color="#545b64"
    active-text-color="#569bff">
    <el-button
      class="collapse"
      type="text"
      v-if="isCollapse == false"
      @click.prevent="isCollapse = true">
      <i class="el-icon-arrow-left"></i>
    </el-button>
    <el-button
      class="collapse"
      type="text"
      v-if="isCollapse == true"
      @click.prevent="isCollapse = false">
      <i class="el-icon-arrow-right"></i>
    </el-button>
    <el-menu-item index="1">
      <i class="el-icon-edit"></i>
      <span slot="title">Form</span>
    </el-menu-item>
    <el-submenu index="2" :disabled="table == false">
      <template slot="title">
        <i class="el-icon-menu"></i>
        <span slot="title">Data availability</span>
      </template>
      <el-menu-item-group>
        <el-menu-item index="2">By day</el-menu-item>
        <el-menu-item index="4">By period</el-menu-item>
      </el-menu-item-group>
    </el-submenu>
    <el-menu-item index="3">
      <i class="el-icon-info"></i>
      <span slot="title">About</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
  export default {
    data () {
      return {
        isCollapse: false
             };
           },
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
.collapse {
   display: block;
   margin : auto;
}
</style>
