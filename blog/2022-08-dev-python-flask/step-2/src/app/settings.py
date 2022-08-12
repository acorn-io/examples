import logging as log
import os

GREETING = os.getenv("GREETING", "Hello World!")

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

LOG_LEVEL = "INFO"
log.basicConfig(level=LOG_LEVEL)
