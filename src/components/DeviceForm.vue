<template>
  <div>
    <el-form
     id="form"
      :model="sdsForm"
      :rules="rules"
      ref="value"
      label-width="120px"
      class="value">
      <el-form-item
        label="Project"
        prop="project">
        <el-select
          v-model="sdsForm.project"
          placeholder="please select your project">
          <el-option
            v-for="item in options.project"
            :key="item.value"
            :label="item.label"
            :value="item.value" >
          </el-option>
        </el-select>
      </el-form-item>
      <div class="block">
        <span class="demonstration">With quick options</span>
        <el-date-picker
        v-model="sdsForm.rangedate"
        type="daterange"
        align="right"
        unlink-panels
        range-separator="To"
        start-placeholder="Start date"
        end-placeholder="End date"
        :picker-options="pickerOptions2">
        </el-date-picker>
      </div>

      <el-row>
        <el-col :span="4">
          <el-form-item
            label="Year"
            v-if="sdsForm.julian_day== true"
            prop="y_date">
            <el-date-picker
              type="year"
              placeholder="Pick a year"
              v-model="sdsForm.y_date">
            </el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item
            label="Start Date"
            prop="s_date">
            <el-input-number
              v-if="sdsForm.julian_day == true"
              v-model="sdsForm.s_date"
              :min="1"
              :max="366">
            </el-input-number>
            <el-date-picker
              v-if="sdsForm.julian_day== false"
              type="date"
              placeholder="Pick a start date"
              v-model="sdsForm.s_date">
            </el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item
            label="End Date"
            prop="e_date">
            <el-input-number
              v-if="sdsForm.julian_day == true"
              v-model="sdsForm.e_date"
              :min="1"
              :max="366">
            </el-input-number>
            <el-date-picker
              v-if="sdsForm.julian_day== false"
              type="date"
              placeholder="Pick a end date"
              v-model="sdsForm.e_date">
            </el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item>
            <el-switch
              prop="julian_day"
              v-model="sdsForm.julian_day"
              active-text="julian day"
              inactive-text="date">
            </el-switch>
          </el-form-item>
        </el-col>
      </el-row>



      <el-form-item
        label="More option"
        prop="more_option">
        <el-switch
          v-model="sdsForm.more_option">
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
          <el-checkbox
            v-for="net in options.network[sdsForm.network]"
            :key="net"
            :label="net"
            :value="net"
            name="network"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          @click="submitForm(sdsForm)">
          Submit</el-button>
        <el-button
          @click="resetForm(sdsForm)">
          Reset</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        pickerOptions2: {
          shortcuts: [{
            text: 'Last week',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: 'Last month',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: 'Last 3 months',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit('pick', [start, end]);
            }
          }]
        },
        data: '',
        sdsForm: {
                  rangedate:'',
                  project: '',
                  s_date: '',
                  e_date: '',
                  y_date: '',
                  type: ['HN','HH','DN','EH', 'SH'],
                  more_option: false,
                  network: ['8G', 'EC'],
                  julian_day: false,
                },
        options: {
                  project: [{
                              value: 'ecuador',
                              label: 'Ecuador',
                              net: ['8G','EC'],
                              comp: ['HN','HH','DN','EH', 'SH']
                            }, {
                              value: 'corinthe',
                              label: 'Corinthe',
                              net: ['XX','UU'],
                              comp: ['HN','HH','DN','EH', 'SH']
                            }, {
                              value: 'alparray',
                              label: 'Alparray',
                              net: ['Z3'],
                              comp: ['HN','HH','DN','EH', 'SH']
                            }],
                    component: {
                                ecuador: ['HN','HH','DN','EH', 'SH'],
                                corinthe: ['HN','HH','DN','EH', 'SH'],
                                alparray: ['HN','HH','DN','EH', 'SH']
                              },
                    network: {
                                ecuador: ['8G', 'EC'],
                                corinthe: ['XX'],
                                alparray: ['Z3']
                             }
                  },
        rules: {
              project: [
                { required: true, message: 'Please select Project', trigger: 'change' }
              ],
              y_date: [
                { required: false, message: 'Please pick a Year', trigger: 'change' }
              ],
              s_date: [
                { required: false, message: 'Please pick a start date', trigger: 'change' }
              ],
              e_date: [
                { required: false, message: 'Please pick a end date', trigger: 'change' }
              ],
              type: [
                { type: 'array', required: false, message: 'Please select at least one component', trigger: 'change' }
              ],
              network: [
                { required: false, message: 'Please select network', trigger: 'change' }
              ],
              julian_day: [
                { required: false, message: 'Please select network', trigger: 'change' }
              ]
            }
          };
        },
        props: ['value'],
        methods: {
          // submitForm(evt) {
          //   formName.validate(valid) => {
          //     if (valid) {
          //       this.$emit('input', formName)
          //     } else {
          //       console.log('error submit!!');
          //       return false;
          //     }
          //   });
          submitForm(formName){
              this.$emit('submitForm', formName)
          },
          resetForm(formName) {
            this.$refs[formName].resetFields();
          }
        }
      }
  </script>


  <style>
  #form {
    /* display: table; */
    margin: 0 auto;
  }

  </style>
