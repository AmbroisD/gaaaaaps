<template>
  <div class = "el-main-setting">
    <h1>Settings</h1>
    <div v-for="(form, mainKey) in formStruct">
      <h4>{{ form.label }}</h4>
      <div class="field" v-for="(field, subKey) in form.fields">
        <div class="label">{{ field.label }}</div>
        <component :is="field.component" v-model="field.value" v-bind="field.props"></component>
        <el-button
          v-if="field.value != field.default"
          type="text" size="mini"
          @click="handleResetParameter(mainKey, subKey)">reset</el-button>
      </div>
    </div>
    <div class="text-center">
      <el-button type="primary" size="medium" @click="handleSaveSettings">Save</el-button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['value'],
  data () {
    let formStruct = {
      tableColor: {
        label: 'Table colors',
        fields: {
          pover: {
            label: 'Overlap',
            component: 'el-color-picker',
            props: {}
          },
          no_data: {
            label: 'No data',
            component: 'el-color-picker',
            props: {}
          },
          p100: {
            label: '100 %',
            component: 'el-color-picker',
            props: {}
          },
          p99_100: {
            label: '99 - 100 %',
            component: 'el-color-picker',
            props: {}
          },
          p90_99: {
            label: '90 - 99%',
            component: 'el-color-picker',
            props: {}
          },
          p75_90: {
            label: '75 - 90%',
            component: 'el-color-picker',
            props: {}
          },
          p50_75: {
            label: '50 - 75%',
            component: 'el-color-picker',
            props: {}
          },
          p25_50: {
            label: '25 - 50%',
            component: 'el-color-picker',
            props: {}
          },
          p0_25: {
            label: '0 - 25%',
            component: 'el-color-picker',
            props: {}
          },
        }
      }
    }
    for (let [key, field] of Object.entries(this.value)) {
      let [mainKey, subKey] = key.split('.')
      Object.assign(formStruct[mainKey].fields[subKey], field)
    }
    return {
      formStruct
    }
  },
  methods: {
    handleResetParameter (mainKey, subKey) {
      let field = this.formStruct[mainKey].fields[subKey]
      field.value = field.default
    },
    handleSaveSettings () {
      for (let [key, field] of Object.entries(this.value)) {
        let [mainKey, subKey] = key.split('.')
        field.value = this.formStruct[mainKey].fields[subKey].value
      }
      this.$emit('input', this.value)
      this.$emit('settings-updated')
    }
  }
}
</script>

<style>
.field, .field > * {
  display: inline-block;
  vertical-align: middle;
}
.field {
  font-size: .9em;
  padding: 10px 0;
  width: 400px;
}
.field .label {
  font-size: 15px;
  padding-right: 10px;
  width: 200px;
  text-align: right;
}
.field .el-input {
  width: 30px;
  font-size: 30px;
}
.el-main-setting {
  line-height: 30px;
  font-size: 18px;
}

</style>
