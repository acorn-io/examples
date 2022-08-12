import logging as log
import os
import time

from flask import Flask, jsonify, render_template_string, request

from app import settings

tpl = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .container {
            display: flex;
            flex-wrap: wrap;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
    </style>
    <title>Awesome Acorn</title>
</head>
<body>
    <div class="container">
        <h1>Awesome Acorn!</h1>
        <h2 style="color: red">{{ greeting }}</h2>
        <form action="" method="post">
            <input type="email" name="email" placeholder="Email">
            <input type="submit" value="Subscribe">
            {% if error %}
            <p style="color: red">{{ error }}</p>
            {% endif %}
        </form>
        <h2>Subscribers</h2>
        <ul>
            {% for subscriber in subscribers %}
            <li>{{ subscriber }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""


class SubscriberExistsError(Exception):
    '''
    Exception to be raised when a subscriber already exists
    '''

    pass


processing_jobs = []

subscriber_file = os.path.join(settings.OUTPUT_DIR, 'subscribers.txt')
with open(subscriber_file, 'w') as f:
    log.info(f"Created subscribers file at {subscriber_file} if it didn't exist")

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
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
    return render_template_string(
        tpl,
        greeting=settings.GREETING,
        error=error,
        subscribers=get_subscribers(),
    )


@app.route('/processing', methods=['GET'])
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
