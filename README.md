# Quasi-Newton Unimontes

## 📋 Descrição

Aplicação web interativa para exploração e visualização do **método Quasi-Newton** de otimização não-linear. O projeto implementa um algoritmo otimizado para encontrar mínimos/máximos de funções multivariadas, com interface amigável em tempo real.

**Tecnologias:**
- **Backend**: FastAPI (Python 3.11) com NumPy, SymPy e JAX
- **Frontend**: Vue 3 com Vite
- **Validação**: Typer (para mensagens de erro bem formatadas)

---

## 🎯 Visão Geral

### Arquitetura

```
┌─────────────┐         HTTP          ┌──────────────┐
│  Frontend   │◄────────────────────► │   Backend    │
│  (Vue.js)   │      JSON/REST        │  (FastAPI)   │
└─────────────┘                       └──────────────┘
                                              │
                                              ▼
                                      ┌──────────────┐
                                      │  Algoritmo   │
                                      │ Quasi-Newton │
                                      └──────────────┘
```

### Fluxo de Dados

```
Frontend (UI) → Backend (API) → Algoritmo (Cálculo) → JSON → Frontend (Visualização)
```

---

## 📁 Estrutura do Projeto

```
quasi-newton-unimontes/
├── backend/                    # API e lógica de otimização
│   ├── main.py                # Inicialização do servidor
│   ├── routes.py              # Rotas HTTP
│   ├── pyproject.toml         # Dependências (Poetry)
│   └── src/optimizer/         # Núcleo do algoritmo
│       ├── __main__.py
│       ├── functions.py       # Funções objetivo
│       └── methods.py         # Implementação Quasi-Newton
├── frontend/                  # Interface Vue.js
│   ├── src/
│   │   ├── App.vue            # Componente principal
│   │   ├── main.js
│   │   └── services/
│   │       └── optimizerApi.js # Cliente HTTP
│   └── package.json
├── design/                    # Tokens e estilos (Figma)
└── docs/                      # Documentação
```

---

## 🚀 Instalação e Execução

### Pré-requisitos

- **Python 3.11** ([Download](https://www.python.org/downloads/release/python-3119/))
- **Node.js** (v16+)
- **Poetry** (gerenciador de dependências Python)

### Backend

1. **Clone o repositório**
   ```bash
   git clone <seu-repositorio>
   cd quasi-newton-unimontes
   ```

2. **Configure o ambiente Python**
   
   **Windows:**
   ```bash
   cd backend
   py -3.11 -m venv venv
   venv\Scripts\activate
   ```

   **Linux/macOS:**
   ```bash
   cd backend
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install poetry
   poetry install
   ```

4. **Inicie o servidor**
   ```bash
   python main.py
   ```
   
   O servidor estará disponível em `http://127.0.0.1:8000`

### Frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

A aplicação estará acessível em `http://localhost:5173`

---

## ⚙️ Configuração

### Variáveis de Ambiente (Frontend)

Crie um arquivo `.env` na pasta `frontend` para customizar a URL da API:

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🛠️ Tecnologias e Dependências

### Backend
- **FastAPI**: Framework web assíncrono
- **Uvicorn**: Servidor ASGI
- **NumPy**: Cálculos numéricos
- **SymPy**: Álgebra simbólica
- **JAX**: Diferenciação automática
- **Pydantic**: Validação de dados
- **Typer**: Formatação de erros em terminal

### Frontend
- **Vue 3**: Framework JavaScript
- **Vite**: Build tool e dev server

---

## 📊 Status do Projeto

### ✅ Implementado
- API FastAPI funcional
- Algoritmo Quasi-Newton core
- Interface Vue.js básica
- Comunicação Frontend-Backend

### 🔄 Em Desenvolvimento
- Seleção dinâmica de funções objetivo
- Critérios de parada customizáveis
- Gráficos e visualizações avançadas

---

## 👥 Autores

- [Davi Santos](https://github.com/davi-ssantos1) - Algoritmo de Quasi-Newton
- [Felipe Monteiro](https://github.com/felipe-monteiro16) - Backend e Integrações
- [Arthur Anderson](https://github.com/artarc) - Frontend
- [MariRAmorim](https://github.com/MariRAmorim) - Frontend
- [Iury Oliveira](https://github.com/IuryOliveira567) - Frontend(Gráficos)
- [Enzo Emanuel](https://github.com/EnzoEVS) - Design
- 
