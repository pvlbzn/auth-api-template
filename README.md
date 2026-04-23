# Setup

Copy `.env.example` and provide your credentials in `.env`.

```shell
cp .env.example .env
```

Initialize docker image with database.

```shell
docker compose up -d
```

Load dependencies and sync the project.

```shell
uv sync
```

Apply migrations.

```shell
uv run db-migrate

# Should return
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> d9e9ff0ca69b, auth
```

Run the app.

```shell
uv run dev

# Should return
INFO:     Will watch for changes in these directories: ['...']
INFO:     Uvicorn running on http://0.0.0.0:35000 (Press CTRL+C to quit)
INFO:     Started reloader process [17450] using WatchFiles
INFO:     Started server process [17452]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

# Migrations

```shell
uv run alembic revision --autogenerate -m "message"

# Drop and apply migrations
uv run db-reset

# Apply migrations
uv run db-migrate
```

# Update Dependencies

```shell
uv lock --upgrade 
uv sync
```
