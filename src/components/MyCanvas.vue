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
      padding: 7,
      context: {}
    }
  },
  props: ['canvasValue'],
  mounted () {
    this.canvas = this.$refs.canvas
    this.context = this.canvas.getContext('2d')
    this.drawRect()
  },
  methods: {
    getXPos (p) {
      return Math.floor(p * (this.canvas.width - 2 * this.padding) + this.padding) + .5
    },
    drawRect () {
      this.canvas.width = this.canvas.parentElement.clientWidth
      this.canvas.height = this.canvas.parentElement.clientHeight
      let width = this.canvas.width - 2 * this.padding
      this.context.save()
      this.context.rect(this.getXPos(0), .5, width, 60)
      this.context.clip()

      for (let rect of this.canvasValue) {
          let x = this.getXPos(rect[0])
          let w = this.getXPos(rect[1]) - x
          // console.log(`x: ${x}, w: ${w}`);
          this.context.fillStyle = rect[2]
          this.context.fillRect(x, .5, w, 60)
      }
      this.context.restore()
      this.context.strokeRect(this.getXPos(0), .5, width, 60)

      var grid_size = width / 24
      this.context.font = '12px Arial';
      this.context.textBaseline = 'top'
      this.context.fillStyle = 'black';
      this.context.textAlign = 'center';
      for ( let i=0; i<(25); i++) {

        let tickPos = this.getXPos(0) + Math.floor(grid_size*i)
        this.context.moveTo(tickPos , 3+60);
        this.context.lineTo(tickPos, 60);
        this.context.stroke();

        this.context.fillText(i , tickPos, 60+3);
     }
     this.context.font = 'bold 15px Arial';
     this.context.fillText('Time (UTC)' , this.canvas.width/2, 60+20);
     this.context.restore()
    }
  }
}

</script>
