import logging as log
import os

GREETING = os.getenv("GREETING", "Hello World!")

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOG_LEVEL = "INFO"
log.basicConfig(level=LOG_LEVEL)


DB_HOST = os.getenv("DB_HOST", "db")
DB_DATABASE = os.getenv("DB_DATABASE", "acorn-devspace")
DB_USER = os.getenv("DB_USER", "acorn-devspace")
DB_PASSWORD = os.getenv("DB_PASSWORD", "acorn-devspace")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
