# Task Manager

Gerenciador de tarefas de linha de comando em Python (somente biblioteca padrão).

## Funcionalidades

- Adicionar tarefa (descrição vazia é rejeitada)
- Listar tarefas
- Marcar tarefa como concluída
- Excluir tarefa

As tarefas ficam em `tasks.json` no diretório atual (ignorado pelo git). Se o arquivo
estiver corrompido, o programa avisa e começa com lista vazia.

## Requisitos

- Python 3.9+

## Execução

```bash
git clone https://github.com/Lelolima/Task-manager-app.git
cd Task-manager-app
python task_manager.py
```

## Testes e lint

```bash
pip install pytest ruff
ruff check .
pytest -q
```

## Variáveis de ambiente

Nenhuma.

## CI

`.github/workflows/ci.yml` roda lint (ruff), testes (pytest) e compilação a cada push/PR.

## Licença

MIT — ver `LICENSE`.
