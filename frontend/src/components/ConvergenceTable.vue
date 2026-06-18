<template>
  <div class="table-wrap">
    <table v-if="hasData">
      <thead>
        <tr>
          <th>Iteração</th>
          <th>x₁</th>
          <th>x₂</th>
          <th>f(x)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(p, i) in dados.X_iteracoes" :key="i">
          <td>{{ i + 1 }}</td>
          <td>{{ formatNumber(p[0]) }}</td>
          <td>{{ formatNumber(p[1]) }}</td>
          <td>{{ formatNumber(dados.f_iteracoes[i]) }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else class="table-placeholder">
      Nenhuma iteração recebida da API.
    </div>
  </div>
</template>

<script setup>

import { computed } from 'vue'

const props = defineProps({
  dados: Object
})

const hasData = computed(() => {
  return (
    props.dados &&
    Array.isArray(props.dados.X_iteracoes) &&
    props.dados.X_iteracoes.length > 0
  )
})

function formatNumber(value) {

  const number = Number(value);

  if (!Number.isFinite(number)) {
    return '-'
  }

  return new Intl.NumberFormat(
    'pt-BR',
    {
      maximumFractionDigits: 8
    }
  ).format(number)
}

</script>

<style scoped>
.table-wrap {
  width: 100%;
  overflow-x: auto;
}

table {
  background-color: #ffff;
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  font-weight: 800;
  text-align: center;
}

td {
  border-color: #aba4a4;
  color:#4a5056;
}

th {
  background-color: #2b50b5;
  color: #ffff;
}

thead {
  font-weight: bold;
}

.table-placeholder {
  text-align: center;
  padding: 24px;
}

table tbody tr:nth-child(odd) {
  background-color: #f8fafc;
}

table tbody tr:nth-child(even) {
  background-color: #e2e8f0;;
}

table tbody tr:hover {
  background-color: #d6eaf8;
}
</style>