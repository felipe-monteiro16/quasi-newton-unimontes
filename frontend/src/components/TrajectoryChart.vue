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
  optimizationData: {
    type: Object,
    default: null
  },
  xMin: {
    type: Number,
    default: -20
  },
  xMax: {
    type: Number,
    default: 20
  },
  yMin: {
    type: Number,
    default: -10
  },
  yMax: {
    type: Number,
    default: 10
  },
  passo: {
    type: Number,
    default: 0.1
  }
});

const chart = ref(null);

function renderPlot() {
  try {
    const expr = compile(props.function);

    const x = [];
    const y = [];
    const z = [];

    for (let valor = props.xMin; valor <= props.xMax; valor += props.passo) {
      x.push(valor);
    }

    for (let valor = props.yMin; valor <= props.yMax; valor += props.passo) {
      y.push(valor);
    }

    for (let j = 0; j < y.length; j++) {
      const linha = [];

      for (let i = 0; i < x.length; i++) {
        const valor = expr.evaluate({
          x1: x[i],
          x2: y[j]
        })

        linha.push(valor);
      }

      z.push(linha);
    }

    const data = [{
        type: 'contour',
        x,
        y,
        z,
        showscale: false,
        colorscale: 'Viridis',
        contours: {
          coloring: 'lines',
          showlabels: true
        },
        line: {
          width: 1
        }
      }
    ];

    if (props.optimizationData && props.optimizationData.X_iteracoes) {
      const pontosValidos = props.optimizationData.X_iteracoes.filter(
          ([x1, x2]) =>
            Number.isFinite(x1) &&
            Number.isFinite(x2) &&
            Math.abs(x1) < 1e6 &&
            Math.abs(x2) < 1e6
      );

      if(pontosValidos.length > 0) {
        const trajX = pontosValidos.map(
            p => p[0]
        )

        const trajY = pontosValidos.map(
            p => p[1]
        )

        data.push({
          type: 'scatter',
          mode: 'lines+markers',
          x: trajX,
          y: trajY,
          name: 'Trajetória',
          line: {
            width: 3
          },
          marker: {
            size: 8
          }
        });

        data.push({
          type: 'scatter',
          mode: 'markers+text',
          x: [trajX[0]],
          y: [trajY[0]],
          text: ['x₀'],
          textposition: 'top center',
          showlegend: false,
          marker: {
            size: 12,
            symbol: 'circle'
          }
        });
      }
      
      if (props.optimizationData.X_otimo) {
        data.push({
          type: 'scatter',
          mode: 'markers+text',
          x: [
            props.optimizationData.X_otimo[0]
          ],
          y: [
            props.optimizationData.X_otimo[1]
          ],
          text: ['x*'],
          textposition: 'top center',
          showlegend: false,
          marker: {
            size: 14,
            symbol: 'diamond'
          }
        });
      }
    }

    const layout = {
      title: 'Mapa de Contorno',
      showlegend: true,
      margin: {
        l: 50,
        r: 20,
        b: 50,
        t: 50
      },
      xaxis: {
        title: 'x₁',
        zeroline: true
      },
      yaxis: {
        title: 'x₂',
        zeroline: true,
        scaleanchor: 'x'
      }
    }

    Plotly.react(
      chart.value,
      data,
      layout,
      {
        responsive: true
      }
    );
  }
  catch (erro) {
    console.error('Erro ao gerar gráfico:', erro);
  }
}

onMounted(() => {
  renderPlot();
})

watch(
  () => [
    props.function,
    props.optimizationData,
    props.xMin,
    props.xMax,
    props.yMin,
    props.yMax,
    props.passo
  ],
  () => renderPlot(),
  {
    deep: true
  }
)
</script>

<style scoped>

.plot-container {
  width: 100%;
  height: 400px;
}

</style>