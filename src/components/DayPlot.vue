<template>
  <div class="my-canvas-wrapper">

    <canvas ref="canvas"></canvas>
    <slot></slot>
  </div>
</template>

<script>
export default {
  data() {
    return {
      canvas: null,
      height: 60,
      padding: 7,
      context: {}
    }
  },
  props: ['value'],
  mounted () {
    this.canvas = this.$refs.canvas
    this.context = this.canvas.getContext('2d')
    this.drawRect()
  },
  methods: {
    getWidth () {
      return this.canvas.width - 2 * this.padding
    },
    getXPos (p) {
      let d = new Date(p)
      let day_start = new Date()
      day_start.setTime(d - (d % 86400000))
      return .5 + Math.floor(this.padding + ((d - day_start) * this.getWidth()) / 86400000)
    },
    drawRect () {
      this.canvas.width = this.canvas.parentElement.clientWidth
      this.canvas.height = this.canvas.parentElement.clientHeight
      let width = this.getWidth()
      let x0 = this.padding + .5
      let y0 = .5
      this.context.save()
      this.context.strokeStyle = 'black'
      this.context.fillStyle = '#6ec47e'
      this.context.rect(x0, y0, width, this.height)
      this.context.fill()
      this.context.clip()

      for (let rect of this.value) {
          let x = this.getXPos(rect.StartTime)
          let w = this.getXPos(rect.EndTime) - x
          if (w < 0) {
            w += width
          }
          // console.log(`x: ${x}, w: ${w}`);
          this.context.fillStyle = rect.color
          this.context.fillRect(x, y0, w, this.height)
      }
      this.context.restore()
      this.context.strokeRect(x0, y0, width, this.height)

      var grid_size = width / 24
      this.context.font = '12px Arial'
      this.context.textBaseline = 'top'
      this.context.fillStyle = 'black'
      this.context.textAlign = 'center'
      for (let i = 0; i < 25; i++) {
        let tickPos = x0 + Math.floor(grid_size*i)
        this.context.moveTo(tickPos , this.height + 3)
        this.context.lineTo(tickPos, this.height)
        this.context.fillText(i , tickPos, this.height + 3)
      }
      this.context.stroke()
      this.context.font = 'bold 15px Arial'
      this.context.fillText('Time (UTC)' , this.canvas.width / 2, this.height + 20);
      this.context.restore()
    }
  }
}

</script>
