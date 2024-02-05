import discord
from discord.ext import commands, tasks
import random
import asyncio
import basique
import repeat
import profile
import jeux

# import admins
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
    await bot.add_cog(profile.Profile(bot))
    await bot.add_cog(basique.commandeBasique(bot))
    await bot.add_cog(jeux.Jeux(bot))
bot.run('NzYyMzYwMTAyODk2MDA5MjU2.GoBW9M.6rInUq3IWmrr-SykX6-VP2fGWGcaJkKdVfvZkE')
