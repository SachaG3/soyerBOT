import discord
from discord.ext import commands,tasks
import pymysql

from repository.messageRepository import new_message as new_message_repo
from repository.message_deleteRepository import new_message as new_message_delete_repo
from repository.message_editRepository import new_message as new_message_edit
from repository.utilisateurRepository import get_user_by_idUtilisateur, new_user

import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$$$$$$$$",intents=intents, description="Bot de Soyergold")


@bot.event
async def on_ready():
    print('Le bot est OK')
    print('------')


@bot.event
async def on_message(message):

    idUtilisateur = message.author.id
    pseudo = message.author.name
    try:
        utilisateur = get_user_by_idUtilisateur(idUtilisateur)
        if not utilisateur:
            new_user(idUtilisateur, pseudo)
            userId = idUtilisateur
        else:
            userId = utilisateur['id']
        new_message_repo(userId, message.content)
    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'insertion du message ou de l'utilisateur dans la base de données : {e}")
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    idUtilisateur = message.author.id
    try:
        utilisateur = get_user_by_idUtilisateur(idUtilisateur)
        if utilisateur:
            userId = utilisateur['id']
            new_message_delete_repo(userId, message.content)
    except pymysql.MySQLError as e:
         print(f"Erreur lors de l'insertion du message supprimé dans la base de données : {e}")
@bot.event
async def on_message_edit(before, after):
    idUtilisateur = before.author.id
    try:
        utilisateur = get_user_by_idUtilisateur(idUtilisateur)
        if utilisateur and before.content != after.content:
            userId = utilisateur['id']
            new_message_edit(userId,before.content, after.content)
    except pymysql.MySQLError as e:
         print(f"Erreur lors de l'insertion du message modifié dans la base de données : {e}")



bot.run(os.environ.get("TOKEN_DISCORD"))
