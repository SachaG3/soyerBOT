import discord
from discord.ext import commands,tasks
import random
import asyncio
import pymysql
from db_config import db_config
from dotenv import load_dotenv
import os
load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="^^",intents=intents, description="Bot de Soyergold")


@bot.event
async def on_ready():
    print('Le bot est OK')
    print('------')


@bot.event
async def on_message(message):
    # Exclure les messages du bot pour éviter une boucle infinie
    if message.author.bot:
        return

    idUtilisateur = message.author.id
    pseudo = message.author.name

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM utilisateurs WHERE idUtilisateur = %s", (idUtilisateur,))
            utilisateur = cursor.fetchone()

            if not utilisateur:
                cursor.execute("INSERT INTO utilisateurs (idUtilisateur, pseudo, score) VALUES (%s, %s, %s)",
                               (idUtilisateur, pseudo, 0))  # Ajoutez d'autres champs si nécessaire
                connection.commit()
                userId = cursor.lastrowid
            else:
                # Si l'utilisateur existe, utiliser son ID existant
                userId = utilisateur['id']

            sql = "INSERT INTO message (message, userId) VALUES (%s, %s)"
            cursor.execute(sql, (message.content, userId))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'insertion du message ou de l'utilisateur dans la base de données : {e}")
    finally:
        if connection:
            connection.close()
    await bot.process_commands(message)



@bot.event
async def on_message_delete(message):
    fichier = open("suppriméLog", "a")
    m = "Le message supprimé de ",message.author.name,"été", message.content
    fichier.write("\n")
    fichier.write(str(m))
    fichier.close()
@bot.event
async def on_message_edit(before, after):
    fichier = open("changeMessageLog.txt", "a")
    m = before.content, "a était changé en", after.content, "par", before.author.name
    fichier.write("\n")
    fichier.write(str(m))
    fichier.close()



bot.run(os.environ.get("TOKEN_DISCORD"))
