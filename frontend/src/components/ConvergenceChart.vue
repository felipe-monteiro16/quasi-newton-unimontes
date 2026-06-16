<template>
  <div class="plot-container" ref="chart"></div>
</template>

<script setup>
import Plotly from 'plotly.js-dist-min'
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  data: Object
})

const chart = ref(null)

function render() {

  if (!props.data) return
  if (!Array.isArray(props.data.f_iteracoes)) return

  const iteracoes = props.data.f_iteracoes.map(
    (_, i) => i + 1
  )

  Plotly.newPlot(
    chart.value,
    [
      {
        x: iteracoes,
        y: props.data.f_iteracoes,
        type: 'scatter',
        mode: 'lines+markers'
      }
    ],
    {
      title: 'Convergência',
      xaxis: {
        title: {
          text: 'Iteração'
        }
      },
      yaxis: {
        title: {
          text: 'f(x)'
        }
      }
    },
    {
      responsive: true,
      displayModeBar: false
    }
  )
}

onMounted(() => {
  render();
})

watch(
  () => props.data,
  render,
  {}
)

</script>

<style scoped>
  .plot-container {
    display: block;
    margin: auto;
    width:100%;
    min-height: 420px;
  }
</style>