import csv

import pymysql
from db_config import db_config

def get_messages():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM message_edit"
    cursor.execute(query)
    messages = cursor.fetchall()
    connection.close()
    return messages

def get_message_by_id(message_id):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM message_edit WHERE id = %s"
    cursor.execute(query, (message_id,))
    message = cursor.fetchone()
    connection.close()
    return message

def get_message_by_userId(userId):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM message_edit WHERE userId = %s"
    cursor.execute(query, (userId,))
    messages = cursor.fetchall()
    connection.close()
    return messages

def new_message(userId, old_message, new_message):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO message_edit (userId, message, new_message) VALUES (%s, %s, %s)"
    cursor.execute(query, (userId, old_message, new_message))
    connection.commit()
    connection.close()


def export_all_user_message_to_csv(user_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM message_edit WHERE userId = %s"
    cursor.execute(query, (user_id,))
    messages = cursor.fetchall()
    with open('messages.csv', 'w', newline='', encoding='utf-8') as file:  # Ajout de newline='' pour éviter les lignes vides dans le CSV
        writer = csv.writer(file)
        writer.writerow(['id', 'message', 'new_message'])  # Ajout de 'new_message' dans l'en-tête
        for message in messages:
            writer.writerow([message['id'], message['message'], message.get('new_message', '')])  # Utiliser get() pour la compatibilité
