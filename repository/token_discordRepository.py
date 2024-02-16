

import pymysql
from db_config import db_config

import random
import string

from datetime import datetime


def generate_random_token(length=32):
    """Generate a random string of fixed length."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def new_token(id_utilisateur):
    token = generate_random_token()

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    query = "INSERT INTO token_discord (token, id_utilisateur, date_creation) VALUES (%s, %s, %s)"
    cursor.execute(query, (token, id_utilisateur, datetime.now()))

    conn.commit()
    conn.close()

    return token
