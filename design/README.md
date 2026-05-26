# Design System — Quasi-Newton BFGS Visualizer

🔗 **[Arquivo Figma](https://www.figma.com/design/fdsgvMJI7q5VjkUam8r6jF/Quasi-Newton-BFGS-—-Visualizador-v2?node-id=0-1&t=F4MKRl6a6MUneCnd-1)**

---

## Estrutura do aplicativo

O app é composto por duas janelas:

**Janela Principal** — tela inicial. Contém o formulário de configuração, os gráficos de convergência e a tabela de iterações.

**Janela Solução Gráfica** — acessada pelo botão "Solução Gráfica" na sidebar. Exibe as visualizações geométricas: superfície 3D, curvas de nível, região de viabilidade e trajetória no plano x₁-x₂.

## Janela Principal

### Sidebar — campos do formulário

| Campo | Tipo | Valores |
|---|---|---|
| Função Objetivo f(x₁, x₂) | `text` | Ex: `x1**2 + 2*x2**2 - 2*x1*x2` |
| Ponto Inicial x₁ | `number` | Qualquer real |
| Ponto Inicial x₂ | `number` | Qualquer real |
| Tolerância ε | `number` | Ex: `0.0001` |
| Critério de Parada | `select` | Ver opções abaixo |
| Máximo de Iterações | `number` | Ex: `100` |

Critérios de parada disponíveis:

| value | label |
|---|---|
| `gradient_norm` | `\|\|∇f(x)\|\| < ε` |
| `step_difference` | `\|\|xₖ₊₁ − xₖ\|\| < ε` |
| `objective_difference` | `\|f(xₖ₊₁) − f(xₖ)\| < ε` |

### Botões da sidebar

- **Executar** — envia o formulário (`POST /optimize`)
- **Reiniciar** — limpa o formulário e o resultado
- **Solução Gráfica** — abre a Janela Solução Gráfica. Estilo: outline verde (não sólido), diferente dos dois acima. Classe `.graphic-button` em `tokens.css`

### Cards de resumo (4 cards no topo do conteúdo)

Exibem o resultado após execução. Enquanto não há resultado, exibem `—`.

| Card | Dado |
|---|---|
| Solução Aproximada | x* = (x₁, x₂) |
| Valor Final f(x*) | valor numérico |
| Iterações | número total |
| Critério de Parada | label do critério usado |

### Abas

Duas abas na Janela Principal:

- **Convergência** — exibe os 3 gráficos abaixo lado a lado
- **Tabela** — exibe a tabela de iterações

### Gráficos de convergência

Renderizados com **Chart.js**. Os três ficam lado a lado.

| Gráfico | Dado | Cor | Escala Y |
|---|---|---|---|
| Convergência de f(x) | `history.f[]` | `#3dca8d` | Logarítmica |
| Variáveis x₁ e x₂ | `history.x[]` colunas 0 e 1 | x₁ `#5baaf4` · x₂ `#fcbc5e` | Linear |
| Norma do gradiente ‖∇f‖ | `history.grad_norm[]` | `#bf7af9` | Logarítmica |

Eixo X: número da iteração k (0, 1, 2, ...).

### Tabela de iterações

| Coluna | Dado |
|---|---|
| k | índice da iteração |
| x₁ | `iterations[k].x[0]` |
| x₂ | `iterations[k].x[1]` |
| f(xₖ) | `iterations[k].fx` |
| ‖∇f(xₖ)‖ | `iterations[k].gradient_norm` |
| αₖ (step) | `iterations[k].alpha` |
| Convergido | `iterations[k].converged` — exibir `✓` quando `true` |

### Badge de status (topbar)

| Estado | Classe CSS | Cor | Texto |
|---|---|---|---|
| Aguardando | — | `--muted-foreground` | `Aguardando` |
| Executando | `.running` | `#fcbc5e` | `Executando...` |
| Convergido | `.active` | `--primary` | `Convergido` |
| Erro | `.error` | `#ef5350` | `Erro` |

---

## Janela Solução Gráfica

### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  [← Voltar]   Janela Principal / Solução Gráfica   [badges] │
├────────────────┬─────────────────────────────────────────────┤
│  Nav lateral   │                                             │
│                │         Área do gráfico ativo               │
│  ○ Sup. 3D     │                                             │
│  ○ Curvas Nív. │                                             │
│  ○ Reg. Viável │                                             │
│  ○ Trajetória  │                                             │
│  ──────────    │                                             │
│  [result-card] │                                             │
└────────────────┴─────────────────────────────────────────────┘
```

### Nav lateral

Quatro opções. Apenas uma ativa por vez. O `result-card` abaixo do nav exibe x*, f(x*) e nº de iterações do resultado atual.

### Gráficos — renderização com Plotly.js

**Superfície 3D**
- `type: 'surface'`
- Grade de pontos: x₁ e x₂ de −5 a 5, calcular f(x₁, x₂) para cada par
- Marcar x* com `scatter3d`
- Colorscale: `'Plasma'`

**Curvas de Nível + Trajetória x₁-x₂**
- `type: 'contour'` com a mesma grade da superfície
- Sobrepor `type: 'scatter'` com os pontos de `history.x[]`
- Marcar início (triângulo `#ffd166`) e ótimo (estrela `#43e8c8`)
- Numerar cada ponto com o índice k

**Região de Viabilidade**
- Problema irrestrito: preencher o plano com verde translúcido, exibir nota "Domínio: ℝ²"
- Com restrições: linhas tracejadas para `g(x) = 0`, sombrear região inviável

**Trajetória x₁-x₂**
- Scatter 2D com `history.x[]`
- Setas indicando direção entre iterações consecutivas
- Pontos numerados com o índice k

---

## Estrutura de componentes Vue

```
App.vue
├── <header class="topbar">
├── <aside class="sidebar">
│   └── <form class="config-form">
│       ├── campos do formulário
│       ├── <button class="primary-button">   Executar
│       ├── <button class="secondary-button"> Reiniciar
│       └── <button class="graphic-button">   Solução Gráfica
├── <main class="content">
│   ├── summary-grid (4 cards)
│   ├── abas [Convergência | Tabela]
│   ├── 3× <canvas> Chart.js  (aba Convergência)
│   └── <table>               (aba Tabela)
└── <GraphicWindow v-if="showGraphicWindow" :result="result" @close="...">
    ├── <header class="gw-topbar">
    ├── <nav class="vis-nav">  (4 opções + result-card)
    └── <main class="gw-content">
        └── gráfico Plotly.js correspondente à opção ativa
```

---

## Dependências de UI

```bash
npm install chart.js vue-chartjs   # gráficos de convergência
npm install plotly.js              # superfície 3D, contorno, viabilidade, trajetória
```

---

## Estilos

As variáveis CSS e classes novas estão em `design/tokens.css`. O conteúdo deve ser incorporado ao `frontend/src/styles.css`.

Classes novas relevantes:

| Classe | Descrição |
|---|---|
| `.graphic-button` | Botão Solução Gráfica (outline verde) |
| `.graphic-button-hint` | Texto de dica abaixo do botão |
| `.graphic-window` | Container fullscreen da Janela 2 |
| `.gw-topbar` | Topbar da Janela 2 com breadcrumb |
| `.back-btn` | Botão "← Voltar" |
| `.gw-layout` | Grid: nav lateral + área de gráfico |
| `.vis-nav` | Nav lateral com botões de visualização |
| `.result-card` | Mini-card de resultado no nav |
| `.gw-content` | Área dos gráficos |
| `.chart-row` | Dois gráficos lado a lado |
| `.status-badge.running` | Badge âmbar |
| `.status-badge.error` | Badge vermelho |
