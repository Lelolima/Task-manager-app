# Auditoria — Task-manager-app — 2026-11-22

## Estado anterior

- O repositório continha apenas `LICENSE`, `README.md` e `.github/workflows/blank.yml`.
- `blank.yml` **não era um workflow**: continha uma árvore de diretórios, o código Python
  completo do app e trechos de README/.gitignore colados. O GitHub rejeitava o arquivo
  (run 44978653599 falhou em 0s).
- `README.md` continha apenas comandos `git` soltos.
- Não existia `task_manager.py`, testes, nem CI funcional.

## Problemas

| # | Severidade | Problema | Evidência |
|---|---|---|---|
| 1 | P0 | App não executável: código só existia dentro do YAML | `git ls-files` sem `.py` |
| 2 | P1 | CI quebrado (`blank.yml` YAML inválido) | `gh run list` → failure 0s |
| 3 | P1 | Crash com entrada não numérica nas opções 3/4 | código original + entrada `3`,`abc` → `ValueError: invalid literal for int()` (executado) |
| 4 | P1 | Crash se `tasks.json` corrompido | `tasks.json` = `{x` → `JSONDecodeError` (executado) |
| 5 | P2 | Descrição vazia aceita | inspeção |
| 6 | P2 | Sem testes / README não descreve o projeto | inspeção |

Segredos: nenhum (busca manual nos 3 arquivos e no histórico). Dependências: nenhuma externa
(só stdlib), portanto nada a auditar com pip-audit.

## Mudanças

- `task_manager.py` extraído do `blank.yml` preservando as funções (`load_tasks`, `save_tasks`,
  `add_task`, `view_tasks`, `mark_completed`, `delete_task`, `main`) e o formato do `tasks.json`.
- `read_index()` trata entrada não numérica; `load_tasks()` trata JSON corrompido/não-lista;
  descrição vazia rejeitada; encoding UTF-8 explícito.
- `blank.yml` removido; `ci.yml` novo (ruff + pytest + py_compile), `permissions: contents: read`,
  actions fixadas por SHA.
- `.gitignore`, `pytest.ini`, `tests/test_task_manager.py` (9 testes), README reescrito.

## Testes executados (local, Windows, Python 3.13)

- `ruff check .` → All checks passed
- `pytest -q` → 9 passed
- Reprodução dos crashes 3 e 4 com o código original → confirmados; cobertos por
  `test_main_non_numeric_index_does_not_crash` e `test_corrupted_file_does_not_crash`.

## Riscos residuais

- `LICENSE` diz "Copyright (c) 2023 Your Name" — não alterado (troca de licença/titular é decisão do dono).
- Escrita de `tasks.json` não é atômica (queda no meio da escrita pode corromper; agora tratado na leitura).
