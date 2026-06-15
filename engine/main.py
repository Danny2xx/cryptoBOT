"""Skeleton entrypoint — proves the Docker Compose stack (Postgres + Redis) is wired up.

This will grow into the strategy engine orchestration loop (Epic 2+). For now it just
verifies connectivity so `docker compose up` has something meaningful to confirm E1-US2.
"""

import os

import psycopg2
import redis


def check_redis() -> None:
    host = os.environ["REDIS_HOST"]
    port = int(os.environ["REDIS_PORT"])
    client = redis.Redis(host=host, port=port)
    client.ping()
    print("Redis OK")


def check_postgres() -> None:
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    )
    conn.close()
    print("Postgres OK")


def main() -> None:
    check_redis()
    check_postgres()


if __name__ == "__main__":
    main()
