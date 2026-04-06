# DataLens Sync Repo

Локальный `pull/status/push` для хранения объектов DataLens как файлов.

Основная реализация sync-инструмента живёт внутри skill:

- [sync.py](/Users/timur/.codex/skills/datalens/scripts/sync.py)
- [sync.config.json](/Users/timur/.codex/skills/datalens/sync.config.json)
- [datalens_sync_repo](/Users/timur/.codex/skills/datalens/src/datalens_sync_repo)

В этом репозитории оставлен только thin wrapper [scripts/sync.py](/Users/timur/Documents/datalens/code/scripts/sync.py), локальный `src` здесь больше не используется.

Пока реализован первый безопасный шаг:

- pull одного workbook в структурированные папки
- экспорт dashboard/chart/dataset/connection в локальные JSON-файлы
- manifest с путями и базовыми зависимостями
- status по локальным правкам и remote drift после последнего pull
- push обратно в DataLens
  - update для существующих `dataset/chart/dashboard`
  - create для новых локальных `dataset/chart/dashboard` draft-папок
  - поддержка локальных ссылок между новыми draft-объектами:
    - `local:datasets/<slug>`
    - `local:charts/<slug>`
  - delete для удалённых локально `dataset/chart/dashboard` через явный `--prune`
- connection сохраняются в redacted-виде

## Конфиг

Файл [datalens-sync.json](/Users/timur/Documents/datalens/code/datalens-sync.json) задаёт:

- путь до соседнего репозитория с текущим CLI
- путь до `.env`
- директорию вывода
- список `workbooks` для пакетного `pull-all`
- ветки `published/saved` для pull

## Запуск

```bash
python scripts/sync.py pull --workbook-id yfrhu31k1hgun
python scripts/sync.py pull-all
python scripts/sync.py status --workbook-id yfrhu31k1hgun
python scripts/sync.py push --workbook-id yfrhu31k1hgun --dry-run
python scripts/sync.py push --workbook-id yfrhu31k1hgun
python scripts/sync.py push --workbook-id yfrhu31k1hgun --dry-run --prune
python scripts/sync.py push --workbook-id yfrhu31k1hgun --prune
```

## Структура

После pull появляется директория вида:

```text
workbooks/<slug>--<workbook_id>/
  workbook.json
  manifest.json
  dashboards/<slug>--<id>/
    dashboard.json
    meta.json
  charts/<slug>--<id>/
    chart.json
    meta.json
  datasets/<slug>--<id>/
    dataset.full.json
    dataset.update.json
    meta.json
  connections/<slug>--<id>/
    connection.redacted.json
    meta.json
  datasets/<new-slug>/
    dataset.create.json  # or dataset.update.json
    meta.json  # optional
  charts/<new-slug>/
    chart.json
    meta.json  # optional
  dashboards/<new-slug>/
    dashboard.json
    meta.json  # optional
```

## Ограничения MVP

- `pull` пока не удаляет устаревшие локальные файлы
- `push` не поддерживает `connection`, `workbook`
- `push` делает `create` только для `dataset/chart/dashboard`
- `push` не поддерживает `create` для `editor chart`
- `delete` включается только через явный `--prune`
- при remote drift `push` блокируется, если не передан `--allow-remote-drift`
- connection выгружаются с редактированием чувствительных полей, чтобы не складывать секреты в репозиторий
