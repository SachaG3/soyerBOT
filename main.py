import discord
from discord.ext import commands, tasks
import random
import asyncio
import basique
import repeat
import profile
import jeux
from dotenv import load_dotenv
import os

import valorant

load_dotenv()

# import admins
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# import supp
bot = commands.Bot(command_prefix="^^",intents=intents ,description="Bot de Soyer")


@bot.event
async def on_ready():
    print('Le bot est OK !!!!')
    print('------')

    await bot.add_cog(repeat.Repeat(bot))
    await bot.add_cog(valorant.Valorant(bot))
    await bot.add_cog(profile.Profile(bot))
    await bot.add_cog(basique.commandeBasique(bot))
    await bot.add_cog(jeux.Jeux(bot))

bot.run(os.environ.get("TOKEN_DISCORD"))
