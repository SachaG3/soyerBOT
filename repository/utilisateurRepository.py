import pymysql
from db_config import db_config
from repository.listGuildRepository import get_guild, add_guild


def get_user_by_id(id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM utilisateurs WHERE id = %s"
    cursor.execute(query, (id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_idUtilisateur(id_utilisateur):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM utilisateurs WHERE id_utilisateur = %s"
    cursor.execute(query, (id_utilisateur,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT * FROM utilisateurs"
    cursor.execute(query)
    users = cursor.fetchall()
    conn.close()
    return users

def update_score(user_id, score):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "UPDATE utilisateurs SET score = score + %s WHERE id_utilisateur = %s"
    cursor.execute(query, (score, user_id))
    conn.commit()
    conn.close()

def new_user(user_id, name):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO utilisateurs (id_utilisateur, pseudo) VALUES (%s, %s)"
    cursor.execute(query, (user_id, name))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "DELETE FROM utilisateurs WHERE id_utilisateur = %s"
    cursor.execute(query, (user_id,))
    conn.commit()
    conn.close()




