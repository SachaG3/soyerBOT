import pymysql
from db_config import db_config
def get_guild(guild_id):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM list_guild WHERE id_guild = %s"
    cursor.execute(query, (guild_id,))
    guild = cursor.fetchone()
    connection.close()
    return guild

def add_guild(guild_id,guild_name):
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO list_guild (id_guild, name_guild) VALUES (%s, %s)"
    cursor.execute(query, (guild_id, guild_name))
    connection.commit()
    connection.close()

def get_all_guild():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM list_guild"
    cursor.execute(query)
    guilds = cursor.fetchall()
    connection.close()
    return guilds

