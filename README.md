# Setup

Copy `.env.example` and provide your credentials in `.env`.

```shell
cp .env.example .env
```

Initialize docker image with database.

```shell
docker compose up -d
```

Apply migrations.

```shell
uv run db-migrate
```

# Run

```shell
uv sync
uv run dev
```

# Migrations

```shell
uv run alembic revision --autogenerate -m "message"

# Drop and apply migrations
uv run db-reset

# Apply migrations
uv run db-migrate
```
