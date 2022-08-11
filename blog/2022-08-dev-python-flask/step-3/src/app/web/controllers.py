import logging as log

import app.sub as subs
from app import settings
from flask import Blueprint, jsonify, render_template, request

bp = Blueprint("web", __name__, url_prefix="/")


@bp.route('/', methods=['GET', 'POST'])
def index():
    error = None

    # subscription form submission
    if request.method == 'POST':
        email = request.form.get('email')
        if email and email.strip() != "":
            try:
                subs.add_subscriber(email)
                subs.add_processing_job(email)
            except subs.SubscriberExistsError:
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
        subscribers=subs.get_subscribers(),
    )


@bp.route('/processing', methods=['GET'])
def processing():
    '''
    Return the list of processing jobs
    '''
    queued_jobs = subs.get_processing_jobs()
    return jsonify({"count": subs.jobqueue.count, "jobs": queued_jobs})
