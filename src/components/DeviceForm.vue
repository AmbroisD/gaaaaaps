<template>
  <div>
    <el-steps id="steps" :space="200" :active="active" finish-status="success" >
      <el-step title="Date" description="Choose you time period"></el-step>
      <el-step title="Filter"  description="Filtered data by criteria"></el-step>
      <el-step title="Resume" description="Submit form"></el-step>
    </el-steps>
    <el-form
     id="form"
      :model="value"
      :rules="rules"
      ref="value"
      label-width="120px"
      class="value">
      <div
        v-if="active == 0">
        <h3>Choose you time period</h3>
      <div
        v-if="value.julian_day== false">
        <el-form-item
          label="Time period"
          prop="rangedate">
          <el-date-picker
            v-model="value.rangedate"
            type="daterange"
            label-position="top"
            align="right"
            unlink-panels
            range-separator="To"
            start-placeholder="Start date"
            end-placeholder="End date"
            :picker-options="pickerOptions2">
          </el-date-picker>
        </el-form-item>
      </div>
      <div
        v-if="value.julian_day == true">
      <el-row>
        <el-col :span="6">
          <el-form-item
            label="Year"
            prop="y_date">
            <el-date-picker
              type="year"
              :picker-options="datePickerOptions"
              placeholder="Pick a year"
              :default-time="'03:00:00'"
              v-model="value.y_date">
            </el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item
            label="Start Date"
            prop="s_date">
            <el-input-number
              v-model="value.s_date"
              :min="1"
              :max="366">
            </el-input-number>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item
            label="End Date"
            prop="e_date">
            <el-input-number
              v-model="value.e_date"
              :min="2"
              :max="366">
            </el-input-number>
          </el-form-item>
        </el-col>
        </el-row>
        </div>
        <el-form-item>
          <el-switch
            disabled
            prop="julian_day"
            v-model="value.julian_day"
            active-text="julian day"
            inactive-text="date">
          </el-switch>
        </el-form-item>
        <el-form-item
          v-if="value.y_date != null">
          <el-button class="buttonform" type="primary" @click.prevent="updateDate(value)">Next</el-button>
        </el-form-item>
       </div>
       <div
        v-if="active == 1 && options.result != null && options.result.no_data[0]">
       <h3>No data for {{ options.result.no_data[1] }}</h3>
       <el-form-item>
         <el-button class="buttonform" @click.prevent="active = 0">Previous</el-button>
       </el-form-item>
       </div>
       <div
         v-if="active == 1 && options.result != null && !options.result.no_data[0]">
       <h3>You can filter data by criteria</h3>
      </el-form-item>
      <el-form-item
        label="Network"
        prop="network">
        <el-checkbox-group
          v-model="value.network">
          <el-checkbox
            v-for="net in options.result.net"
            :key="net"
            :label="net"
            :value="net"
            name="network">
          </el-checkbox>
          <el-button class="buttonform" size="mini" round type="text" @click.prevent="selectAll('net','network')">Select all</el-button>
          <el-button class="buttonform" size="mini" round type="text" @click.prevent="deselectAll('network')">Deselect all</el-button>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item
        label="Channel prefix"
        prop="type">
        <el-checkbox-group
          v-model="value.type">
          <el-checkbox
            v-for="type in options.result.type"
             :key="type"
             :label="type"
             :value="type"
             name="type">
           </el-checkbox>
            <el-button class="buttonform" size="mini" round type="text" @click.prevent="selectAll('type','type')">Select all</el-button>
            <el-button class="buttonform" size="mini" round type="text" @click.prevent="deselectAll('type')">Deselect all</el-button>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item
        label="Component"
        prop="comp">
        <el-checkbox-group
          v-model="value.comp">
          <el-checkbox
            v-for="comp in options.result.comp"
            :key="comp"
            :label="comp"
            :value="comp"
            name="comp">
          </el-checkbox>
          <el-button class="buttonform" size="mini" round type="text" @click.prevent="selectAll('comp','comp')">Select all</el-button>
          <el-button class="buttonform" size="mini" round type="text" @click.prevent="deselectAll('comp')">Deselect all</el-button>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item
        label="Location Code"
        prop="loc">
        <el-checkbox-group
          v-model="value.loc">
          <el-checkbox
            v-for="loc in options.result.loc"
            :key="loc"
            :label="loc"
            :value="loc"
            name="loc">
          </el-checkbox>
          <el-button class="buttonform" size="mini" round type="text" @click.prevent="selectAll('loc','loc')">Select all</el-button>
          <el-button class="buttonform" size="mini" round type="text" @click.prevent="deselectAll('loc')">Deselect all</el-button>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item>
        <h3>Select station by station</h3>
        <el-transfer
          style="text-align: left; display: inline-block"
          filterable
          :titles="['All Stations', 'Your List']"
          :button-texts="['Remove', 'Add']"
          v-model="value.sta"
          :data="options.sta">
        </el-transfer>
      </el-form-item>
      <el-form-item>
        <el-button class="buttonform" @click.prevent="active = 0">Previous</el-button>
        <el-button class="buttonform" type="primary" @click.prevent="active = 2">Next</el-button>
      </el-form-item>
      </div>
      <div v-if="active == 2">
        <h3>Resume form</h3>
        <ul class="resume">
         <li v-if="value.julian_day">Time period: {{ value.y_date }}   Start: {{ value.s_date }}    End: {{ value.e_date }}</li>
         <li v-if="!value.julian_day">Time period: {{ value.rangedate }}</li>
         <li>Network: {{ value.network }}</li>
         <li>Channel prefix: {{ value.type }}</li>
         <li>Component: {{ value.comp }}</li>
         <li>Location code: {{ value.loc }}</li>
        </ul>
        <el-form-item>
          <el-button
          class="buttonform"
          @click.prevent="active = 1">Previous</el-button>
          <el-button
            type="primary"
            @click="submitForm(value)">
            Submit</el-button>
        </el-form-item>
      </div>
    </el-form>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        active: 0,
        load: null,
        datePickerOptions: {
          disabledDate: this.disabledDateY
        },
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
        rules: {
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
                { type: 'array', required: true, message: 'Please select at least one channel prefix', trigger: 'change' }
              ],
              loc: [
                { type: 'array', required: true, message: 'Please select at least one location', trigger: 'change' }
              ],
              network: [
                { type: 'array', required: true, message: 'Please select at least one network', trigger: 'change' }
              ],
              comp : [
                { type: 'array', required: true, message: 'Please select at least one component', trigger: 'change' }
              ],

              julian_day: [
                { required: false, message: 'Please select network', trigger: 'change' }
              ]
            }
          };
        },
        props: ['value', 'options', 'loadedOption','validDate'],
        mounted () {
          this.load = this.loadedOption
        },
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
          },
          deselectAll(val) {
            this.value[val] = []
          },
          selectAll(val, val2) {
            this.value[val2] = this.options.result[val]
          },
          disabledDateY (date) {
            if (this.validDate.indexOf(String(date.getFullYear())) >= 0) {
              return false
            } else {
              return true
            }
          },
          updateDate(formName) {
            if (this.value.y_date == this.load) {
              this.active = 1
          } else {
              this.$emit('updateDate', formName)
              this.active = 1
              this.load = this.value.y_date
          }}
        }
      }
  </script>


  <style>
  #form {
    line-height: 20px;
    margin-left: auto;
    margin-right: auto;
  }
  #steps {
    line-height: 0px;
    margin-left: 150px;
  }

.buttonform {
    margin-left: 12px;
}
.resume {
    font-size: medium;
    line-height: 30px;
    width: 90%;
}
  </style>
