import asyncio
import logging

import aiohttp
import discord
from discord.ext import commands
import pymysql.cursors
import random
from db_config import db_config
from profilePartage import profil

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

    def get_weapon_with_image(self):
        """Sélectionne aléatoirement une arme avec une image."""
        with pymysql.connect(**db_config) as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM weapons_skins WHERE displayIcon IS NOT NULL")
                weapons_with_image = cursor.fetchall()
                return random.choice(weapons_with_image) if weapons_with_image else None

    def get_similar_weapons(self, correct_weapon, num_samples=3):
        """Récupère un échantillon d'armes similaires en type à l'arme correcte, excluant l'arme correcte elle-même."""
        weapon_type = correct_weapon['weaponType'] or 'Knife'  # Fallback sur 'Knife' si le type est null
        with pymysql.connect(**db_config) as connection:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = """SELECT * FROM weapons_skins 
                           WHERE weaponType = %s AND uuid != %s AND displayIcon IS NOT NULL"""
                cursor.execute(query, (weapon_type, correct_weapon['uuid']))
                similar_weapons = cursor.fetchall()
                if len(similar_weapons) < num_samples:
                    return similar_weapons
                else:
                    return random.sample(similar_weapons, num_samples)

    @commands.command()
    async def rank(ctx, username: str, tag: str):
        rank = get_valorant_rank(username, tag)
        await ctx.send(f"Infos de rang pour {rank}")

    @commands.command()
    async def skin(self, ctx):
        correct_weapon = self.get_weapon_with_image()
        if not correct_weapon:
            await ctx.send("Désolé, impossible de trouver une arme avec une image pour le moment.")
            return

        similar_weapons = self.get_similar_weapons(correct_weapon)
        options = [correct_weapon] + similar_weapons
        random.shuffle(options)

        await ctx.send(correct_weapon['displayIcon'])
        poll_text = '\n'.join(f"{idx + 1}: {weapon['displayName']}" for idx, weapon in enumerate(options))
        poll_message = await ctx.send(poll_text + "\nQuelle est le nom de cette arme ?")

        for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]:
            await poll_message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣"] and reaction.message.id == poll_message.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            index = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"].index(str(reaction.emoji))
            choice = options[index]

            if choice['uuid'] == correct_weapon['uuid']:
                await ctx.send("Félicitations ! Vous avez bien deviné !")
                profil.profiles(self, ctx.author, ctx.author.id, ctx, 2)
            else:
                await ctx.send(f"Désolé, ce n'était pas la bonne réponse. La bonne réponse était {correct_weapon['displayName']}.")
        except asyncio.TimeoutError:
            await ctx.send("Désolé, le temps est écoulé. Essayez encore !")
