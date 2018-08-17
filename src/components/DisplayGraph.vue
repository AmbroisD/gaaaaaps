<template>
  <div v-if="showCharts">
    <highcharts
      v-for="(option, key) in options"
      ref="highcharts"
      :key="key"
      :options="option" >
    </highcharts>
  </div>
</template>

<script>
import Highcharts from 'highcharts';

function sync(vm, event, type) {
  vm.$refs.highcharts.forEach(({ chart }) => {
    if (chart === this.series.chart) return;
    chart.series.forEach((series) => {
      series.data.forEach((point) => {
        if (point.x === this.x) {
          if (type === 'over') {
            point.setState('hover');
            chart.tooltip.refresh(point);
            chart.xAxis[0].drawCrosshair(event, point);
          } else {
            point.setState();
            chart.tooltip.hide();
            chart.xAxis[0].hideCrosshair();
          }
        }
      });
    });
  });
}

export default {
  props: ['station'],

  data() {
    return {
      showCharts: false,
      options: {
        chartRms: null,
        chartStddev: null,
        chartAverage: null,
        chartMax: null,
        chartMin: null
      }
    }
  },

  mounted () {
    this.initCharts()
  },

  watch: {
    station (newValue, oldValue) {
      console.log(this.station, newValue);
      this.initCharts()
    }
  },

  methods: {
    initCharts () {
      console.log('init charts');
      let self = this
      let defaultChartOption = {
        chart: { type: 'spline', zoomType: 'xy'},
        xAxis: { crosshair: true, type: 'datetime' },
        plotOptions: {
          series: {
            point: {
              events: {
                mouseOver: function(event) {
                  sync.call(this, self, event, 'over');
                },
                mouseOut: function(event) {
                  sync.call(this, self, event, 'out');
                }
              }
            }
          }
        }
      }

      this.showCharts = false
      this.options.chartAverage = Object.assign({
        yAxis: { title: { text: 'Average' } },
        title: { text: 'Average' },
        series: [{
          name: 'avg',
          data: this.station.average,
          color: '#6fcd98'
        }]
      }, defaultChartOption)
      this.options.chartMax = Object.assign({
        yAxis: { title: { text: 'Max' } },
        title: { text: 'Max' },
        series: [{
          name: 'max',
          data: this.station.max,
          color: '#6fcd98'
        }]
      }, defaultChartOption)
      this.options.chartMin = Object.assign({
        yAxis: { title: { text: 'Min' } },
        title: { text: 'Min' },
        series: [{
          name: 'min',
          data: this.station.min,
          color: '#6fcd98'
        }]
      }, defaultChartOption)
      this.options.chartRms = Object.assign({
        yAxis: { title: { text: 'Rms' } },
        title: { text: 'RMS' },
        series: [{
          name: 'rms',
          data: this.station.rms,
          color: '#6fcd98'
        }]
      }, defaultChartOption)
      this.options.chartStddev = Object.assign({
        yAxis: { title: { text: 'stddev' } },
        title: { text: 'stddev' },
        series: [{
          name: 'stddev',
          data: this.station.stddev,
          color: '#6fcd98'
        }]
      }, defaultChartOption)
      this.showCharts = true
    }
  }
}
</script>

<style>

</style>
