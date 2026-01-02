import subprocess


def reset():
    subprocess.run(["uv", "run", "alembic", "downgrade", "base"])
    subprocess.run(["uv", "run", "alembic", "upgrade", "head"])


def migrate():
    subprocess.run(["uv", "run", "alembic", "upgrade", "head"])
