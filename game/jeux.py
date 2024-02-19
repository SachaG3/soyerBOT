from discord.ext import commands
import random
import logging
log = logging.getLogger("bot.moderation")
import asyncio
from profile.profilePartage import profil
from game.jeux2 import Carte
from game.jeux2 import carte

class Jeux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="""Lancez-vous dans un jeu de devinettes où vous devez trouver le bon nombre entre 1 et 1000.

        **Comment jouer :**
        - Lancez la commande et attendez le message du bot vous invitant à choisir un nombre.
        - Vous avez 15 secondes pour répondre en envoyant votre devinette.
        - Le bot répondra avec un signe '+' si votre nombre est inférieur au nombre cible, ou un '-' si votre nombre est supérieur.

        **Règles :**
        - Continuez à deviner jusqu'à ce que vous trouviez le bon nombre.
        - Si vous ne répondez pas dans les 15 secondes, le jeu se termine et le nombre correct sera révélé.

        **Objectif :**
        Trouvez le nombre correct avec le moins de tentatives possible pour maximiser vos points."""
    )
    async def juste(self, ctx):
        answer = random.randint(1, 1000)
        await ctx.send('Choisis un nombre entre 1 et 1000.')

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        while True:
            try:
                guess = await self.bot.wait_for('message', check=is_correct, timeout=15.0)
            except asyncio.TimeoutError:
                return await ctx.send(f'Trop lent ! La réponse était {answer}.')

            if int(guess.content) > answer:
                await ctx.send('-')
            elif int(guess.content) < answer:
                await ctx.send("+")
            else:
                await ctx.send("Bien joué, tu as trouvé le nombre !")
                profil.profiles(self, ctx.author, ctx.author.id, ctx, 3)
                break

    @commands.command(
        help="""Tentez votre chance en devinant un nombre entre 1 et 10. Vous avez une seule chance pour trouver le bon nombre sélectionné aléatoirement par le bot.

        **Comment jouer :**
        - Après avoir lancé la commande, vous recevrez un message vous invitant à choisir un nombre entre 1 et 10.
        - Vous avez 5 secondes pour répondre en envoyant le nombre choisi.

        **Règles :**
        - Si vous devinez correctement du premier coup, vous gagnez !
        - Si vous ne répondez pas dans le temps imparti (5 secondes), le jeu prend fin et le bon nombre sera révélé.
        - Si votre réponse est incorrecte, le bon nombre sera également révélé.

        **Récompenses :**
        - En cas de victoire, vous recevrez des points d'expérience ou une récompense spécifique (à définir par l'administrateur du bot).

        **Objectif :**
        Montrez votre flair en trouvant le bon nombre du premier coup !"""
    )
    async def usd(self, ctx):
        await ctx.send('Choisis un nombre entre 1 et 10.')

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        answer = random.randint(1, 10)
        try:
            guess = await self.bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.send('Trop lent ! La réponse était {}.'.format(answer))

        if int(guess.content) == answer:
            await ctx.send('Bravo, tu as gagné !')
            profil.profiles(self, ctx.author, ctx.author.id, ctx, 10)
        else:
            await ctx.send("Dommage, c'était {}. Mieux vaut tenter ta chance la prochaine fois !".format(answer))

    @commands.command(
        name='BJ',
        help="""Jouez au Blackjack contre le bot. Le but du jeu est d'atteindre un total de points le plus proche de 21 sans le dépasser.

        **Instructions :**
        - Cliquez sur `1` pour piocher une nouvelle carte.
        - Cliquez sur `2` pour arrêter votre tour et voir si vous avez gagné.

        **Règles :**
        - Toutes les figures (Valet, Dame, Roi) valent 10 points.
        - L'As peut valoir 1 ou 11 points, selon ce qui est le plus avantageux pour le joueur.
        - Pour faire un 'Blackjack', il faut obtenir un As et une carte valant 10 points (10 ou une figure) avec vos deux premières cartes.

        **Objectif :**
        Être le plus proche de 21 sans dépasser ce total. Le joueur avec un total de points supérieur à 21 perd immédiatement."""
    )
    async def BJ(self, ctx):
        """
        cliquer sur 1 permet de piocher une nouvelle carte
        sur 2 pour voir si vous avez gagner
        l'objectif est d'être le plus proche de 21 et de ne pas dépasser 21
        toute les figures valent 10
        le As peut valoir 1 ou 11
        pour faire un blackjack il faut un As et 10 ou une figure

        """

        await ctx.send("1 pour continuer 2 pour  arrêter.")

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        color = ("Trèfle", "Pique", "Coeur", "Carreau")

        Croupier,Joueur,stop,fin,c,j = 0,0,0,0,0,0

        carte10 = carte.randomC(self, ctx)
        c = carte.testAs(self, ctx, carte10[1], c)

        carte11 = carte.randomC(self, ctx)
        c = carte.testAs(self, ctx, carte11[1], c)

        message = f"Le Croupier a eu **{Carte(carte10[0], str(carte10[2]))}** et une carte retourné "
        await ctx.send(message)

        Croupier = carte10[1] + carte11[1]

        carte10 = carte.randomC(self, ctx)
        j = carte.testAs(self, ctx, carte10[1], j)

        carte11 = carte.randomC(self, ctx)
        j = carte.testAs(self, ctx, carte11[1], j)

        message = f"Ta premiére carte et un **{Carte(carte10[0], str(carte10[2]))}** et la seconde et un **{Carte(carte11[0], str(carte11[2]))}**"
        await ctx.send(message)

        Joueur = Joueur + carte10[1] + carte11[1]


        while fin==0:

            if stop==0:

                try:

                    stopp = await self.bot.wait_for("message", timeout=10, check=is_correct)

                except:

                    return await ctx.send("Veuillez réitérer la commande.")

                if int(stopp.content) == 1:

                    if Joueur-(j*13) >21:

                        stop = 1
                        await ctx.send('Tu as dépassé 21, tu ne peux plus jouer.')

                    else:

                        carte10 = carte.randomC(self, ctx)
                        j = carte.testAs(self, ctx, carte10[1], j)

                        Joueur = Joueur + carte10[1]

                        message= f'Nouvelle carte qui est:\n**{Carte(carte10[0], str(carte10[2]))}**'
                        await ctx.send(message)

                        if Joueur>21 and j==0:

                            stop = 1

                if int(stopp.content) == 2:

                    stop = 1
            else:

                if Croupier-(c*13)>16:
                    fin=1

                else:

                    carte11=carte.randomC(self, ctx)
                    c = carte.testAs(self, ctx, carte11[1], c)

                    Croupier =Croupier+carte11[1]

        Joueur = carte.verifAs(self, ctx, Joueur, j)
        Croupier = carte.verifAs(self, ctx, Croupier, c)

        if Croupier > 21 and Joueur < 22:

            message = f"Gagné, tu as **{Joueur}** points et le Croupier a **{Croupier}** points."
            await ctx.send(message)
            a = profil.profiles(self, ctx.author, ctx.author.id, ctx, 10)

        elif Joueur < Croupier or Joueur > 21:

            message = f"Perdu, le Croupier a **{Croupier}** points et tu as **{Joueur}** points."
            await ctx.send(message)

        elif Joueur > Croupier:

            message = f"Gagné, tu as **{Joueur}** points et le Croupier a **{Croupier}** points."
            await ctx.send(message)
            a = profil.profiles(self, ctx.author, ctx.author.id, ctx, 10)

        elif Croupier == Joueur:

            message = f"Égalité, le Croupier a **{Croupier}** points et tu as **{Joueur}** points."
            await ctx.send(message)




