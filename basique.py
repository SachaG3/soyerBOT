import discord
from discord.ext import commands, tasks
import logging

from repository.token_discordRepository import new_token
from repository.utilisateurRepository import get_user_by_idUtilisateur

log = logging.getLogger("bot.moderation")
import asyncio


class commandeBasique(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverInfo(self, ctx):
        server = ctx.guild
        numberOfTextChannels = len(server.text_channels)
        numberOfVoiceChannels = len(server.voice_channels)
        numberOfPerson = server.member_count
        serverName = server.name
        message = f"Le serveur **{serverName}** contient *{numberOfPerson}* personnes ! \nCe serveur possède {numberOfTextChannels} salons écrit et {numberOfVoiceChannels} salon vocaux."
        await ctx.send(message)
    @commands.command()
    async def jeux(self, ctx):
        await ctx.send("https://discord.gg/jszvZm36r8")

    @commands.command()
    async def link(self, ctx):
        user_id = get_user_by_idUtilisateur(ctx.message.author.id)
        token = new_token(user_id['id'])
        url = f"https://www.soyerbot.fr/token/{token}"
        await ctx.author.send(f"Voici votre lien : {url}")





