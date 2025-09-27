# Trading-algo-backtest — Minimal Working Project

Projeto mínimo funcional para o case de Trading Algorítmico — API de Backtests.

## Como rodar (local)
Requisitos: Python 3.11+, pip

1. Crie e ative um virtualenv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux / macOS
   .\.venv\Scripts\activate # Windows PowerShell
   ```
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Rode a API:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Abra `http://localhost:8000/docs` para testar.

## Endpoints principais
- `POST /backtests/run` — roda um backtest simples (SMA crossover)
- `GET  /backtests/{id}/results` — obtém resultado salvo do backtest (em Postgres)
- `GET  /health` — ok

## Notas
- Banco usado: Postgres (arquivo `app.db`) para facilitar execução local.
- Backtest engine implementado de forma simples em `app/core/backtest_engine.py` (pandas).
