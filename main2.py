import discord
from discord.ext import commands,tasks
import random
import asyncio
from dotenv import load_dotenv
import os
load_dotenv()

bot = commands.Bot(command_prefix="^^", description="Bot de Soyergold")


@bot.event
async def on_ready():
    print('Le bot est OK')
    print('------')



@bot.event
async def on_message(message):
    fichier = open("messageLog", "a")
    m = "message:", message.content,"de",message.author.name
    fichier.write("\n")
    fichier.write(str(m))
    fichier.close()

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
