import logging as log
import time

import redis
from rq import Queue, get_current_job

redis_conn = redis.StrictRedis(host="redis", port=6379, db=0)

jobqueue = Queue(connection=redis_conn)


def process_subscription(email: str) -> dict:
    job = get_current_job()
    log.info(f"Processing subscription for {email}...")
    time.sleep(10)
    log.info(f"Completed processing subscription for {email}")
    return {
        "email": email,
        "job_id": job.id,
        "status": "success",
    }


def add_processing_job(email: str) -> dict:
    job = jobqueue.enqueue(process_subscription, email)
    return {
        "email": email,
        "job_id": job.get_id(),
        "status": job.get_status(),
    }


def get_processing_jobs() -> list[dict]:
    return [
        {
            "email": job.args[0],
            "job_id": job.get_id(),
            "status": job.get_status(),
        }
        for job in jobqueue.get_jobs()
    ]
