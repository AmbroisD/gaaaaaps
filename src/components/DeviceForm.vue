<template>
  <el-form
    :model="sdsForm"
    :rules="rules"
    ref="sdsForm"
    label-width="120px"
    class="sdsForm">
    <el-form-item
      label="Project"
      prop="project">
      <el-select
        v-model="sdsForm.project"
        placeholder="please select your project">
        <el-option
          label="Ecuador"
          value="ecuador"></el-option>
        <el-option
          label="Corinthe"
          value="corinthe"></el-option>
        <el-option
          label="Alparray"
          value="alparray"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      label="Start Date"
      prop="s_date">
        <el-date-picker
          type="date"
          placeholder="Pick a start date"
          v-model="sdsForm.s_date"></el-date-picker>
    </el-form-item>
    <el-form-item
      label="End Date"
      prop="e_date">
      <el-date-picker
        type="date"
        placeholder="Pick a end date"
        v-model="sdsForm.e_date"></el-date-picker>
    </el-form-item>
    <el-form-item
      label="More option"
      prop="more_option">
      <el-switch v-model="sdsForm.more_option">
    </el-switch>
    </el-form-item>
    <el-form-item
      v-if="sdsForm.more_option == true"
      label="Component"
      prop="type">
      <el-checkbox-group
        v-model="sdsForm.type">
        <el-checkbox label="HH" name="type"></el-checkbox>
        <el-checkbox label="HN" name="type"></el-checkbox>
        <el-checkbox label="DN" name="type"></el-checkbox>
        <el-checkbox label="EH" name="type"></el-checkbox>
        <el-checkbox label="SH" name="type"></el-checkbox>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item
      v-if="sdsForm.more_option == true"
      label="Network"
      prop="network">
      <el-checkbox-group
        v-model="sdsForm.network">
        <el-checkbox label="FR" name="network"></el-checkbox>
        <el-checkbox label="RA" name="network"></el-checkbox>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item>
      <el-button
        type="primary"
        @click="submitForm('sdsForm')">
        Submit</el-button>
      <el-button
        @click="resetForm('sdsForm')">
        Reset</el-button>
    </el-form-item>
  </el-form>
</template>
<script>
  export default {
    data() {
      return {
        sdsForm: {
          project: '',
          s_date: '',
          e_date: '',
          type: ['HN','HH','DN','EH', 'SH'],
          more_option: false,
          network: ['FR','RA']
        },
        rules: {
              project: [
                { required: true, message: 'Please select Project', trigger: 'change' }
              ],
              s_date: [
                { type: 'date', required: true, message: 'Please pick a start date', trigger: 'change' }
              ],
              e_date: [
                { type: 'date', required: true, message: 'Please pick a end date', trigger: 'change' }
              ],
              type: [
                { type: 'array', required: false, message: 'Please select at least one component', trigger: 'change' }
              ],
              network: [
                { required: false, message: 'Please select network', trigger: 'change' }
              ]
            }
          };
        },
        methods: {
          submitForm(formName) {
            this.$refs[formName].validate((valid) => {
              if (valid) {
                alert('submit!');
              } else {
                console.log('error submit!!');
                return false;
              }
            });
          },
          resetForm(formName) {
            this.$refs[formName].resetFields();
          }
        }
      }
  </script>
