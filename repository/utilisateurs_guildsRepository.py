import pymysql
from db_config import db_config


def get_user_guilds(user_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT id_guild FROM utilisateur_guilds WHERE id_user = %s"
    cursor.execute(query, (user_id,))
    user_guilds_ids = cursor.fetchall()
    user_guilds = []
    for guild_id in user_guilds_ids:
        query = "SELECT * FROM list_guild WHERE id_guild = %s"
        cursor.execute(query, (guild_id,))
        guild = cursor.fetchone()
        user_guilds.append(guild)
    conn.close()
    return user_guilds

def new_utilisateur_guild(user_id, guild_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    query = "INSERT INTO utilisateur_guilds (id_user, id_guild) VALUES (%s, %s)"
    cursor.execute(query, (user_id, guild_id))
    conn.commit()
    conn.close()

def add_user_to_guild_if_not_exists(user_id, guild_id):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    query = "SELECT * FROM utilisateur_guilds WHERE id_user = %s AND id_guild = %s"
    cursor.execute(query, (user_id, guild_id))
    existing_entry = cursor.fetchone()

    if not existing_entry:
        query = "INSERT INTO utilisateur_guilds (id_user, id_guild) VALUES (%s, %s)"
        cursor.execute(query, (user_id, guild_id))
        conn.commit()
    conn.close()