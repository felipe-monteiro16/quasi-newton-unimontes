# Projeto de Otimização

## Descrição
Implementação de método Quasi-Newton com backend em FastAPI e frontend em Vue.js.


## Estrutura

```
backend/
├── main.py
├── routes.py
└── algorithm/
    ├── interface.py
    ├── core/
    └── problems/
frontend/
docs/
```


## Organização

- Backend: API
- Algoritmo: lógica de otimização
- Frontend: visualização
- Design: Figma


## Fluxo

```
Frontend → Backend → Algoritmo → JSON → Frontend
```


## Observações

- Sem persistência (inicialmente)
- Algoritmo não faz visualização
- Cada integrante atua em uma parte
