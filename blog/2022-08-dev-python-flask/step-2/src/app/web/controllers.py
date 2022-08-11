import logging as log
import os
import time

from app import settings
from flask import Blueprint, jsonify, render_template, request

bp = Blueprint("web", __name__, url_prefix="/")


class SubscriberExistsError(Exception):
    '''
    Exception to be raised when a subscriber already exists
    '''

    pass


processing_jobs = []

subscriber_file = os.path.join(settings.OUTPUT_DIR, 'subscribers.txt')
with open(subscriber_file, 'w') as f:
    log.info(f"Created subscribers file at {subscriber_file} if it didn't exist")


@bp.route('/', methods=['GET', 'POST'])
def index():
    error = None

    # subscription form submission
    if request.method == 'POST':
        email = request.form.get('email')
        if email and email.strip() != "":
            try:
                add_subscriber(email)
                process_subscription(email)
            except SubscriberExistsError:
                error = f'{email} is already subscribed'
            except Exception as e:
                log.error(e)
                error = 'Error adding subscription, please try again later!'
        else:
            error = 'Please enter an email'
    return render_template(
        "index.html",
        greeting=settings.GREETING,
        error=error,
        subscribers=get_subscribers(),
    )


@bp.route('/processing', methods=['GET'])
def processing():
    '''
    Return the list of processing jobs
    '''
    return jsonify({"count": len(processing_jobs), "jobs": processing_jobs})


def add_subscriber(email: str):
    '''
    Add a new subscriber to the list.
    '''
    log.info(f'Adding {email} to subscribers')
    with open(subscriber_file, 'a') as f:
        f.write(email + '\n')


def get_subscribers():
    '''
    Return all emails subscribed so far
    '''
    with open(subscriber_file, 'r') as f:
        return f.read().splitlines()


def process_subscription(email: str):
    '''
    Some long operation to process a new subscription
    e.g. sending a welcome mail and setting up custom jobs
    '''
    log.info(f'Processing subscription for {email}')
    global processing_jobs
    processing_jobs.append(email)
    time.sleep(10)
    log.info(f'Finished processing subscription for {email}')
    processing_jobs.remove(email)
