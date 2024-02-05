import discord
from discord.ext import commands,tasks
import random
import logging
log = logging.getLogger("bot.moderation")
import asyncio
from profilePartage import profil


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def NP(self,ctx):
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
    async def score(self, ctx):
        a=profil.profiles(self,ctx.author,ctx.author.id,ctx,1)
        await ctx.send(a)











