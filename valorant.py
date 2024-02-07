import discord
from discord.ext import commands
import aiohttp
import logging

log = logging.getLogger("bot.moderation")


async def get_valorant_rank(username, tag):
    url = f"https://splendid-groovy-feverfew.glitch.me/valorant/eu/{username}/{tag}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                rank_info = await response.text()
                return rank_info
            else:
                return "Erreur lors de la récupération des données."
class Valorant(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def valo(self,ctx, username: str, tag: str):
        rank = await get_valorant_rank(username, tag)
        await ctx.send(f"Infos de rang pour {rank}")