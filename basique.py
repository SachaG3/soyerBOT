import discord
from discord.ext import commands, tasks
import logging

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






