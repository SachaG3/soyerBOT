import pymysql
from db_config import db_config

def add_log(event_type, description):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO logs (event_type, description) VALUES (%s, %s)"
    cursor.execute(query, (event_type, description))
    conn.commit()
    conn.close()

def get_log_by_id(log_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM logs WHERE id = %s"
    cursor.execute(query, (log_id,))
    log = cursor.fetchone()
    conn.close()
    return log

def get_all_logs():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM logs"
    cursor.execute(query)
    logs = cursor.fetchall()
    conn.close()
    return logs

def update_log_description(log_id, description):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "UPDATE logs SET description = %s WHERE id = %s"
    cursor.execute(query, (description, log_id))
    conn.commit()
    conn.close()

def delete_log(log_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM logs WHERE id = %s"
    cursor.execute(query, (log_id,))
    conn.commit()
    conn.close()
