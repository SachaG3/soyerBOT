import discord
from discord.ext import commands,tasks
import random
import logging
log = logging.getLogger("bot.moderation")
import asyncio
from profile.profilePartage import profil
import pymysql
from db_config import db_config
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter


async def generate_score_image(user_profile_url, score):
    # Télécharge l'image de profil
    response = requests.get(user_profile_url)
    avatar = Image.open(BytesIO(response.content)).resize((100, 100))

    # Crée un masque pour l'effet arrondi
    mask = Image.new('L', (100, 100), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0) + (100, 100), fill=255)

    # Applique le masque à l'avatar pour l'arrondir
    avatar_rounded = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    avatar_rounded.putalpha(mask)

    # Crée l'image de fond avec une couleur plus sombre
    image = Image.new("RGBA", (300, 200), (45, 50, 60, 255))
    draw = ImageDraw.Draw(image)

    # Sélectionne la police et la taille
    try:
        font = ImageFont.truetype("Arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()
    print('test')

    # Ajoute le texte du score
    draw.text((120, 80), f"Score: {score}", fill=(255, 255, 255), font=font)

    # Colle l'avatar arrondi sur l'image de fond
    image.paste(avatar_rounded, (10, 50), avatar_rounded)

    # Convertit l'image en bytes
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr





class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def NP(self, ctx):
        idUtilisateur = ctx.author.id
        pseudo = ctx.author.name
        score_initial = 0

        connection = None
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                # Vérifier d'abord si l'utilisateur existe déjà
                sql_check = "SELECT * FROM utilisateurs WHERE idUtilisateur = %s"
                cursor.execute(sql_check, (idUtilisateur,))
                existing_user = cursor.fetchone()

                if existing_user:
                    await ctx.send("Un profil existe déjà pour cet utilisateur.")
                else:
                    # Insérer un nouveau profil puisque l'utilisateur n'existe pas encore
                    sql_insert = "INSERT INTO utilisateurs (idUtilisateur, pseudo, score) VALUES (%s, %s, %s)"
                    cursor.execute(sql_insert, (idUtilisateur, pseudo, score_initial))
                    connection.commit()
                    await ctx.send("Profil créé avec succès!")
        except pymysql.MySQLError as e:
            print(e)
            await ctx.send("Une erreur est survenue lors de la création du profil.")
        finally:
            if connection:
                connection.close()

    @commands.command(

    help = """Affiche votre score actuel.

        **Utilisation :**
        Tapez la commande dans le canal pour voir votre score. Le score est calculé en fonction de vos activités et participations."""
    )
    async def score(self, ctx):
        score = profil.profiles(self,ctx.author,ctx.author.id,ctx,1)
        profile_url = ctx.author.avatar.url  # Obtient l'URL de l'image de profil Discord de l'utilisateur
        pseudo = ctx.author.name
        print(profile_url)
        # Génère l'image avec le score et l'image de profil
        score_image = await generate_score_image(profile_url, score)

        # Envoie l'image dans le canal
        await ctx.send(file=discord.File(BytesIO(score_image), "score.png"))












