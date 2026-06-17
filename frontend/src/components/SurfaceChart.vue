<template>
  <div ref="chart" class="plot-container"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import Plotly from 'plotly.js-dist-min'
import { compile } from 'mathjs'

const props = defineProps({
  function: {
    type: String,
    required: true
  },

  xMin: {
    type: Number,
    default: -10
  },

  xMax: {
    type: Number,
    default: 10
  },

  yMin: {
    type: Number,
    default: -10
  },

  yMax: {
    type: Number,
    default: 10
  },

  step: {
    type: Number,
    default: 0.2
  }
})

const chart = ref(null)

function PlotSurface() {

  try {
    const expr = compile(props.function)

    const x = []
    const y = []
    const z = []

    for(let value = props.xMin; value <= props.xMax; value += props.step) {
      x.push(value)
    }

    for(let value = props.yMin; value <= props.yMax; value += props.step) {
      y.push(value)
    }

    let zMin = Infinity
    let zMax = -Infinity
    
    for (let j = 0; j < y.length; j++) {
      const line = []

      for (let i = 0; i < x.length; i++) {
        const value = expr.evaluate({
          x1: x[i],
          x2: y[j]
        })

        line.push(value)
        zMin = Math.min(zMin, value)
        zMax = Math.max(zMax, value)
      }

      z.push(line)
    }

    const data = [
      {
        type: 'surface',
        x,
        y,
        z,
        showscale: false,
        colorscale: 'Rainbow',
        
        contours: {
          z: {
            show: false,
            project: {
              z: true
            }
          }
        }
      }
    ]

    const xRange = props.xMax - props.xMin
    const yRange = props.yMax - props.yMin
    const zRange = zMax - zMin
 
    const layout = {
      title: props.function,
      margin: {
        l: 0,
        r: 0,
        b: 0,
        t: 0
      },
      scene: {
        aspectmode: 'cube',
        camera: {
          eye: {
            x: 1,
            y: 1,
            z: 1
          }
        },
        xaxis: {
          title: 'x₁'
        },
        yaxis: {
          title: 'x₂'
        },
        zaxis: {
          title: 'f(x₁,x₂)',
          range: [-10, 20]
        }
      }
    }

    Plotly.react(
      chart.value,
      data,
      layout,
      {
        responsive: true
      }
    )

  } catch (erro) {
    console.error(
      'Erro ao avaliar função:',
      erro
    )
  }
}

onMounted(() => {
  PlotSurface()
})

watch(
  () => [
    props.function,
    props.xMin,
    props.xMax,
    props.yMin,
    props.yMax,
    props.step
  ],
  () => PlotSurface()
)
</script>

<style scoped>
.plot-container {
  display: block;
  margin: auto;
  width: 100%;
  height: 100%;
}
</style>