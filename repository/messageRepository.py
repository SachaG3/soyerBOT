import csv

import pymysql
from db_config import db_config
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

def new_message(userId, message, id_guild=None):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO message (userId, message, id_guild) VALUES (%s, %s, %s)"
    cursor.execute(query, (userId, message, id_guild))
    connection.commit()
    connection.close()

def export_all_user_message_to_csv(user_id):
    conn = pymysql.connect(**db_config)
    # Utilisation de DictCursor ici
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM message WHERE userId = %s"
    cursor.execute(query, (user_id,))
    messages = cursor.fetchall()
    with open('messages.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'userId', 'message', 'id_guild'])
        for message in messages:
            writer.writerow([message['id'], message['userId'], message['message'], message['id_guild']])


