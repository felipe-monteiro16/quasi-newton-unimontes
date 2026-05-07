<script setup>
import { computed, reactive, ref } from 'vue'
import { runQuasiNewton } from './services/optimizerApi'

const initialForm = {
  objectiveFunction: 'x₁² + 2x₂² - 2x₁x₂ + 4x₁ - 6x₂',
  x1: '0',
  x2: '0',
  tolerance: '0.0001',
  stoppingCriterion: 'gradient_norm',
  maxIterations: '100',
}

const form = reactive({ ...initialForm })
const activeView = ref('surface')
const isRunning = ref(false)
const result = ref(null)
const errorMessage = ref('')

const hasResult = computed(() => Boolean(result.value))

const iterations = computed(() => {
  if (!Array.isArray(result.value?.iterations)) {
    return []
  }

  return result.value.iterations
})

const statusLabel = computed(() => {
  if (isRunning.value) {
    return 'Executando'
  }

  return hasResult.value ? 'Convergido' : 'Aguardando'
})

const solutionDisplay = computed(() => {
  const point =
    result.value?.solution ??
    result.value?.final_point ??
    result.value?.x ??
    result.value?.point

  if (!Array.isArray(point) || point.length < 2) {
    return '-'
  }

  return `x* = (${formatNumber(point[0])}, ${formatNumber(point[1])})`
})

const objectiveDisplay = computed(() => {
  const value = result.value?.objective_value ?? result.value?.fx ?? result.value?.f
  const formatted = formatNumber(value)

  return formatted ? `f(x*) = ${formatted}` : '-'
})

const iterationsCount = computed(() => {
  const count = result.value?.iterations_count ?? iterations.value.length

  return count || '-'
})

const stoppingDisplay = computed(() => {
  return result.value?.stopping_criterion_label ?? criterionLabels[form.stoppingCriterion]
})

const tabs = [
  { id: 'surface', label: 'Superfície 3D', icon: 'cube' },
  { id: 'contour', label: 'Contorno', icon: 'circle' },
  { id: 'trajectory', label: 'Trajetória', icon: 'route' },
  { id: 'feasible', label: 'Região Viável', icon: 'square' },
  { id: 'convergence', label: 'Convergência', icon: 'trend' },
  { id: 'table', label: 'Tabela', icon: 'table' },
]

const chartTitle = computed(() => {
  const titles = {
    surface: 'Superfície 3D da Função Objetivo',
    contour: 'Curvas de Contorno',
    trajectory: 'Trajetória das Iterações',
    feasible: 'Região Viável',
    convergence: 'Convergência',
    table: 'Tabela de Iterações',
  }

  return titles[activeView.value]
})

const criterionLabels = {
  gradient_norm: '||∇f(x)|| < ε',
  step_difference: '||xₖ₊₁ - xₖ|| < ε',
  objective_difference: '|f(xₖ₊₁) - f(xₖ)| < ε',
}

const canSubmit = computed(() => {
  return (
    form.objectiveFunction.trim() &&
    form.x1 !== '' &&
    form.x2 !== '' &&
    form.tolerance !== '' &&
    form.stoppingCriterion &&
    form.maxIterations !== ''
  )
})

function formatNumber(value) {
  const number = Number(value)

  if (!Number.isFinite(number)) {
    return ''
  }

  return new Intl.NumberFormat('pt-BR', {
    maximumFractionDigits: 8,
  }).format(number)
}

async function handleSubmit() {
  if (!canSubmit.value) {
    errorMessage.value = 'Preencha todos os campos antes de executar o metodo.'
    return
  }

  isRunning.value = true
  errorMessage.value = ''
  result.value = null

  try {
    result.value = await runQuasiNewton({
      objective_function: form.objectiveFunction.trim(),
      initial_point: [Number(form.x1), Number(form.x2)],
      tolerance: Number(form.tolerance),
      stopping_criterion: form.stoppingCriterion,
      max_iterations: Number(form.maxIterations),
    })
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Nao foi possivel executar o metodo.'
  } finally {
    isRunning.value = false
  }
}

function resetForm() {
  Object.assign(form, initialForm)
  result.value = null
  errorMessage.value = ''
  activeView.value = 'surface'
}
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24">
          <path d="M10 2v6a2 2 0 0 1-.24.96L4.24 19.04A2 2 0 0 0 6 22h12a2 2 0 0 0 1.76-2.96L14.24 8.96A2 2 0 0 1 14 8V2" />
          <path d="M8.5 2h7" />
          <path d="M7 15h10" />
        </svg>
      </div>

      <div class="brand-copy">
        <h1>Quasi-Newton Visualizer</h1>
        <p>Visualizador de Otimização Numérica</p>
      </div>

      <div class="topbar-actions">
        <span class="status-badge" :class="{ active: hasResult }">
          {{ statusLabel }}
        </span>
        <span class="project-badge">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M22 10v6" />
            <path d="m21.4 10.9-8.6 3.9a2 2 0 0 1-1.6 0L2.6 10.9a1 1 0 0 1 0-1.8l8.6-3.9a2 2 0 0 1 1.6 0l8.6 3.9a1 1 0 0 1 0 1.8Z" />
            <path d="M6 12.5V16c0 1.7 2.7 3 6 3s6-1.3 6-3v-3.5" />
          </svg>
          Protótipo Acadêmico
        </span>
      </div>
    </header>

    <div class="layout">
      <aside class="sidebar">
        <form class="config-form" @submit.prevent="handleSubmit">
          <div class="sidebar-title">
            <span class="sidebar-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24">
                <path d="M12 15.5A3.5 3.5 0 1 0 12 8a3.5 3.5 0 0 0 0 7.5Z" />
                <path d="M19.4 15a1.8 1.8 0 0 0 .3 2l.1.1a2.1 2.1 0 0 1-3 3l-.1-.1a1.8 1.8 0 0 0-2-.3 1.8 1.8 0 0 0-1.1 1.7v.2a2.1 2.1 0 0 1-4.2 0v-.2a1.8 1.8 0 0 0-1.1-1.7 1.8 1.8 0 0 0-2 .3l-.1.1a2.1 2.1 0 0 1-3-3l.1-.1a1.8 1.8 0 0 0 .3-2 1.8 1.8 0 0 0-1.7-1.1h-.2a2.1 2.1 0 0 1 0-4.2h.2a1.8 1.8 0 0 0 1.7-1.1 1.8 1.8 0 0 0-.3-2l-.1-.1a2.1 2.1 0 0 1 3-3l.1.1a1.8 1.8 0 0 0 2 .3 1.8 1.8 0 0 0 1.1-1.7V2a2.1 2.1 0 0 1 4.2 0v.2a1.8 1.8 0 0 0 1.1 1.7 1.8 1.8 0 0 0 2-.3l.1-.1a2.1 2.1 0 0 1 3 3l-.1.1a1.8 1.8 0 0 0-.3 2 1.8 1.8 0 0 0 1.7 1.1h.2a2.1 2.1 0 0 1 0 4.2h-.2A1.8 1.8 0 0 0 19.4 15Z" />
              </svg>
            </span>
            <h2>Configuração do Problema</h2>
          </div>

          <label class="field full">
            <span>Função Objetivo f(x₁, x₂)</span>
            <input
              v-model="form.objectiveFunction"
              type="text"
              name="objectiveFunction"
              autocomplete="off"
            />
          </label>

          <div class="field-label">Ponto Inicial x₀</div>
          <div class="field-grid">
            <label class="field">
              <span>x₁</span>
              <input v-model="form.x1" type="number" step="any" name="x1" />
            </label>
            <label class="field">
              <span>x₂</span>
              <input v-model="form.x2" type="number" step="any" name="x2" />
            </label>
          </div>

          <label class="field full">
            <span>Tolerância ε</span>
            <input
              v-model="form.tolerance"
              type="number"
              step="any"
              min="0"
              name="tolerance"
            />
          </label>

          <label class="field select-field">
            <span>Critério de Parada</span>
            <select v-model="form.stoppingCriterion" name="stoppingCriterion">
              <option value="gradient_norm">||∇f(x)|| &lt; ε</option>
              <option value="step_difference">||xₖ₊₁ - xₖ|| &lt; ε</option>
              <option value="objective_difference">|f(xₖ₊₁) - f(xₖ)| &lt; ε</option>
            </select>
          </label>

          <label class="field full">
            <span>Máximo de Iterações</span>
            <input
              v-model="form.maxIterations"
              type="number"
              min="1"
              step="1"
              name="maxIterations"
            />
          </label>

          <p v-if="errorMessage" class="message message-error">
            {{ errorMessage }}
          </p>

          <button class="primary-button" type="submit" :disabled="isRunning">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M5 5a2 2 0 0 1 3-1.73l12 7a2 2 0 0 1 0 3.46l-12 7A2 2 0 0 1 5 19Z" />
            </svg>
            {{ isRunning ? 'Executando...' : 'Executar Método Quasi-Newton' }}
          </button>

          <button class="secondary-button" type="button" @click="resetForm">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M3 12a9 9 0 1 0 3-6.7L3 8" />
              <path d="M3 3v5h5" />
            </svg>
            Reiniciar Problema
          </button>
        </form>
      </aside>

      <main class="content">
        <div class="results-header">
          <h2>Resultados</h2>
          <span class="status-badge main-status" :class="{ active: hasResult }">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <path d="M20 6 9 17l-5-5" />
            </svg>
            {{ statusLabel }}
          </span>
        </div>

        <section class="summary-grid">
          <article class="summary-card">
            <div>
              <span>Solução Aproximada</span>
              <strong>{{ solutionDisplay }}</strong>
              <p>Ponto ótimo encontrado</p>
            </div>
            <span class="card-icon">
              <svg viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="8" />
                <circle cx="12" cy="12" r="3" />
              </svg>
            </span>
          </article>

          <article class="summary-card">
            <div>
              <span>Valor Final da Função</span>
              <strong>{{ objectiveDisplay }}</strong>
              <p>Valor objetivo no ótimo</p>
            </div>
            <span class="card-icon">
              <svg viewBox="0 0 24 24">
                <path d="m4 7 5 5 4-4 7 7" />
                <path d="M18 15h2v-2" />
              </svg>
            </span>
          </article>

          <article class="summary-card">
            <div>
              <span>Iterações</span>
              <strong>{{ iterationsCount }}</strong>
              <p>Total de iterações</p>
            </div>
            <span class="card-icon">
              <svg viewBox="0 0 24 24">
                <path d="M5 9h14" />
                <path d="M5 15h14" />
                <path d="M10 3 8 21" />
                <path d="m16 3-2 18" />
              </svg>
            </span>
          </article>

          <article class="summary-card">
            <div>
              <span>Critério de Parada</span>
              <strong>{{ stoppingDisplay }}</strong>
              <p>Condição de convergência</p>
            </div>
            <span class="card-icon">
              <svg viewBox="0 0 24 24">
                <path d="M6 4h12" />
                <path d="M8 20h8" />
                <path d="m9 4 6 8-6 8" />
              </svg>
            </span>
          </article>
        </section>

        <section class="analysis-section">
          <h2>Análise Gráfica</h2>

          <div class="tabs" role="tablist" aria-label="Visualizações">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              :class="{ active: activeView === tab.id }"
              type="button"
              @click="activeView = tab.id"
            >
              <svg v-if="tab.icon === 'cube'" viewBox="0 0 24 24" aria-hidden="true">
                <path d="m12 3 8 4.5v9L12 21l-8-4.5v-9Z" />
                <path d="m4 7.5 8 4.5 8-4.5" />
                <path d="M12 12v9" />
              </svg>
              <svg v-else-if="tab.icon === 'circle'" viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="12" cy="12" r="7" />
                <circle cx="12" cy="12" r="2" />
              </svg>
              <svg v-else-if="tab.icon === 'route'" viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="6" cy="6" r="2" />
                <circle cx="18" cy="18" r="2" />
                <path d="M8 6h5a3 3 0 0 1 0 6h-2a3 3 0 0 0 0 6h5" />
              </svg>
              <svg v-else-if="tab.icon === 'square'" viewBox="0 0 24 24" aria-hidden="true">
                <rect x="5" y="5" width="14" height="14" rx="1" />
              </svg>
              <svg v-else-if="tab.icon === 'trend'" viewBox="0 0 24 24" aria-hidden="true">
                <path d="m4 7 5 5 4-4 7 7" />
                <path d="M18 15h2v-2" />
              </svg>
              <svg v-else viewBox="0 0 24 24" aria-hidden="true">
                <path d="M4 6h16" />
                <path d="M4 12h16" />
                <path d="M4 18h16" />
                <path d="M9 4v16" />
                <path d="M15 4v16" />
              </svg>
              {{ tab.label }}
            </button>
          </div>

          <article class="chart-card">
            <h3>{{ chartTitle }}</h3>

            <div v-if="activeView !== 'table'" class="visual-stage">
              <svg class="surface-visual" viewBox="0 0 520 300" aria-hidden="true">
                <path class="axis" d="M190 220V82" />
                <path class="axis" d="M190 220h170" />
                <path class="axis" d="M190 220 90 170" />
                <path class="grid-line" d="M110 170h210" />
                <path class="grid-line" d="M130 180h210" />
                <path class="grid-line" d="M150 190h210" />
                <path class="grid-line" d="M170 200h210" />
                <path class="grid-line" d="M120 160 240 220" />
                <path class="grid-line" d="M150 150 270 210" />
                <path class="grid-line" d="M180 140 300 200" />
                <path class="surface-fill" d="M125 174c48-52 85-65 123-27 35 35 62 23 88-28v61c-48 20-91 24-128 5-32-17-59-19-83-11Z" />
                <path class="surface-line" d="M110 158c44-82 94-67 130-29 44 46 79 14 96-45" />
                <path class="surface-line thin" d="M140 168c42-60 80-48 114-15 32 31 63 15 82-26" />
                <circle class="opt-point" cx="270" cy="118" r="7" />
                <text x="180" y="80">f</text>
                <text x="360" y="238">x₁</text>
                <text x="98" y="248">x₂</text>
              </svg>
              <p>Superfície f(x₁, x₂) com eixos x₁, x₂ e f(x₁, x₂)</p>
            </div>

            <div v-else-if="iterations.length > 0" class="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>k</th>
                    <th>x₁</th>
                    <th>x₂</th>
                    <th>f(x)</th>
                    <th>||∇f||</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in iterations" :key="index">
                    <td>{{ item.k ?? index }}</td>
                    <td>{{ formatNumber(item.x1 ?? item.x?.[0]) || '-' }}</td>
                    <td>{{ formatNumber(item.x2 ?? item.x?.[1]) || '-' }}</td>
                    <td>{{ formatNumber(item.objective_value ?? item.fx) || '-' }}</td>
                    <td>{{ formatNumber(item.gradient_norm) || '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div v-else class="table-placeholder">
              Nenhuma iteração recebida da API.
            </div>
          </article>
        </section>
      </main>
    </div>
  </div>
</template>
