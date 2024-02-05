import discord
from discord.ext import commands,tasks
import logging
log = logging.getLogger("bot.moderation")

class Repeat(commands.Cog):
    '''
    permet de répéter avec ou sans la voix
    rp=sans
    rpt=avec


    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rp(self, ctx):
        await ctx.send('choisi le mot que tu veut répeter')

        def checkMessage(message):
            return message.author == ctx.message.author and ctx.message.channel == message.channel

        try:

            leMessage = await self.bot.wait_for("message", timeout=10, check=checkMessage)

        except:

            return await ctx.send("Veuillez réitérer la commande.")

        await ctx.send("choisi le nombre de fois que tu veut le répéter")

        def checkMessage2(message):
            return message.author == ctx.message.author and ctx.message.channel == message.channel

        try:
            nbrDeFois = await self.bot.wait_for("message", timeout=10, check=checkMessage2)
            w = int(nbrDeFois.content)
        except:
            await ctx.send("Veuillez réitérer la commande.")
            return
        for i in range(w):
            await ctx.send(leMessage.content, )
    @commands.command()
    async def rpt(self, ctx):
        await ctx.send('choisi le mot que tu veut répeter')

        def checkMessage(message):
            return message.author == ctx.message.author and ctx.message.channel == message.channel

        try:
            leMessage = await self.bot.wait_for("message", timeout=10, check=checkMessage)
        except:

            return await ctx.send("Veuillez réitérer la commande.")

        await ctx.send("choisi le nombre de fois que tu veut le répéter")

        def checkMessage2(message):
            return message.author == ctx.message.author and ctx.message.channel == message.channel

        try:
            nbrDeFois = await self.bot.wait_for("message", timeout=10, check=checkMessage2)
            w = int(nbrDeFois.content)
        except:
            await ctx.send("Veuillez réitérer la commande.")
            return
        for i in range(w):
            await ctx.send(leMessage.content, tts=True)

