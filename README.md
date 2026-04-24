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

## Setup Social Login Provider

### GitHub

Set up:
1. Navigate to [Developer Settings](https://github.com/settings/developers), and create a new OAuth app
2. Get Client ID and put it into `PROJECT_GITHUB_CLIENT_ID` at `.env`
3. Generate Client secrets and put it into `PROJECT_GITHUB_CLIENT_SECRET` at `.env`
4. Set Authorization callback URL to be http://localhost:35000/api/v1/auth/callback/github, substitute address and port if needed

Test it:
1. Navigate to http://localhost:35000/api/v1/auth/login/github
2. Follow the login flow
3. Once done you'll be redirected to http://localhost:35000/auth/callback?token=TOKEN
4. Copy `TOKEN` value, its JWT token
5. Open any HTTP client like Postman, set auth to Bearer Token, and put the token there
6. Call GET http://0.0.0.0:35000/api/v1/auth/user

You will your user details back:
```json
{
    "id": "ad53c641-d666-4670-b6fe-3799bd4fd657",
    "email": "pvlbzn@gmail.com",
    "name": "Pavel Bazin",
    "provider": "github",
    "provider_id": "9218794",
    "avatar_url": "https://avatars.githubusercontent.com/u/9218794?v=4"
}
```

You can connect to the database and see your user there in `users` table.


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
