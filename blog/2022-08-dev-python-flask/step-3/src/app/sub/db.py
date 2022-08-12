import psycopg2
from app import settings


class SubscriberExistsError(Exception):
    '''
    Exception to be raised when a subscriber already exists
    '''

    pass


def new_connection():
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        database=settings.DB_DATABASE,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
    )
    return conn


# Get subscribers from database
def get_subscribers() -> list[str]:
    conn = new_connection()
    cur = conn.cursor()
    cur.execute("SELECT email FROM subscribers")
    res = cur.fetchall()
    conn.close()
    return [e[0] for e in res]


# Add new email to database
def add_subscriber(email: str):
    if email in get_subscribers():
        raise SubscriberExistsError
    conn = new_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO subscribers (email) VALUES (%s)", (email,))
    conn.commit()
    conn.close()
