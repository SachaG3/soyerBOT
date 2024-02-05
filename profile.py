import discord
from discord.ext import commands,tasks
import random
import logging
log = logging.getLogger("bot.moderation")
import asyncio
from profilePartage import profil
import pymysql
from db_config import db_config


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def NP2(self,ctx):
        with open('profile.txt', 'r') as f:
            lines = [line.strip('\n') for line in f.readlines()]
            a = 0
            while 0 == 0:
                if a > len(lines) :
                    await ctx.send("création du profil")
                    profil.modif(self,ctx.author,ctx.author.id,ctx)
                    return

                elif lines[a] == str(ctx.author.id):
                    await ctx.send("tu as déjà un profil")
                    return
                else:
                    a = a+4

    @commands.command()
    async def NP(self, ctx):
        idUtilisateur = ctx.author.id
        pseudo = ctx.author.name
        score_initial = 0

        connection = None
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Vérifier d'abord si l'utilisateur existe déjà
                sql_check = "SELECT * FROM utilisateurs WHERE idUtilisateur = %s"
                cursor.execute(sql_check, (idUtilisateur,))
                existing_user = cursor.fetchone()

                if existing_user:
                    await ctx.send("Un profil existe déjà pour cet utilisateur.")
                else:
                    # Insérer un nouveau profil puisque l'utilisateur n'existe pas encore
                    sql_insert = "INSERT INTO utilisateurs (idUtilisateur, pseudo, score) VALUES (%s, %s, %s)"
                    cursor.execute(sql_insert, (idUtilisateur, pseudo, score_initial))
                    connection.commit()
                    await ctx.send("Profil créé avec succès!")
        except pymysql.MySQLError as e:
            print(e)
            await ctx.send("Une erreur est survenue lors de la création du profil.")
        finally:
            if connection:
                connection.close()

    @commands.command()
    async def score(self, ctx):
        a=profil.profiles(self,ctx.author,ctx.author.id,ctx,1)
        await ctx.send(a)











