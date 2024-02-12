import csv

import pymysql
from db_config import db_config
from repository.listGuildRepository import get_guild, add_guild
from repository.utilisateurs_guildsRepository import add_user_to_guild_if_not_exists


def get_messages():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM message"
    cursor.execute(query)
    messages = cursor.fetchall()
    connection.close()
    return messages

def get_message_by_id(message_id):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM message WHERE id = %s"
    cursor.execute(query, (message_id,))
    message = cursor.fetchone()
    connection.close()
    return message

def get_message_by_userId(userId):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM message WHERE userId = %s"
    cursor.execute(query, (userId,))
    messages = cursor.fetchall()
    connection.close()
    return messages


def new_message(user_id, message):

    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO message (userId, message) VALUES (%s, %s)"
    cursor.execute(query, (user_id, message))
    connection.commit()
    connection.close()


def export_all_user_message_to_csv(user_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM message WHERE userId = %s"
    cursor.execute(query, (user_id,))
    messages = cursor.fetchall()
    with open('messages.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'message'])
        for message in messages:
            writer.writerow([message['id'], message['message']])
    conn.close()

