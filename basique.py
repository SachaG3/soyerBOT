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

    @commands.command(

    help = """Liez votre compte Discord à notre site web facilement.

        **Instructions :**
        - Tapez la commande dans n'importe quel canal où le bot est présent.
        - Vous recevrez un message privé avec un lien unique.
        - Suivez ce lien pour compléter la liaison de votre compte.

        **Sécurité :**
        - Le lien est à usage unique et expire après un certain temps pour garantir votre sécurité.
        - Assurez-vous de ne pas partager ce lien avec d'autres personnes."""

)
    async def link(self, ctx):
        user_id = get_user_by_idUtilisateur(ctx.message.author.id)
        token = new_token(user_id['id'])
        url = f"https://www.soyerbot.fr/token/{token}"
        await ctx.author.send(f"Voici votre lien : {url}")





