# Configuration de la base de données MySQL

from dotenv import load_dotenv
import os
load_dotenv()
import pymysql


db_config = {
    'host': os.environ.get("DB_HOST"),
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASSWORD"),
    'db': os.environ.get("DB_DATABASE"),
    'port': 3306,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


