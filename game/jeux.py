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


    @commands.command()
    async def juste(self,ctx):
        answer = random.randint(1, 1000)
        while 0 == 0:
            a = 0 + 1
            await ctx.send('choisi un nombre entre 1 et 1000.')

            def is_correct(m):
                return m.author == ctx.author and m.content.isdigit()

            try:
                guess = await self.bot.wait_for('message', check=is_correct, timeout=15.0)
            except asyncio.TimeoutError:
                return await ctx.send('écrit plus vite {}.'.format(answer))

            if int(guess.content) > answer:
                await ctx.send('-')
            elif int(guess.content) < answer:
                await ctx.send("+")
            elif int(guess.content) == answer:
                await ctx.send("bien joué trouvé ")
                a = profil.profiles(self, ctx.author, ctx.author.id, ctx, 3)
                return

            @commands.command()
            async def Juste2(self, ctx):
                async def vrai(self, ctx):
                    await ctx.send("choisi la limite qui doit être supérieure ou égale 1")

                    def is_correct(m):
                        return m.author == ctx.author and m.content.isdigit()

                    try:
                        choix = await self.bot.wait_for('message', check=is_correct, timeout=15.0)
                    except asyncio.TimeoutError:
                        return await ctx.send('écrit plus vite {}.'.format())
                    return int(choix.content) if int(choix.content) > 0 else True

                choix = await vrai(self, ctx)

                if choix is True:
                    choix = await vrai(self, ctx)

                answer = random.randint(1, choix)
                while 0 == 0:
                    a = 0 + 1
                    message = f"choisi un nombre entre 1 et **{int(choix.content)}**"
                    await ctx.send(message)

            def is_correct(m):
                return m.author == ctx.author and m.content.isdigit()

            try:
                guess = await self.bot.wait_for('message', check=is_correct, timeout=15.0)
            except asyncio.TimeoutError:
                return await ctx.send('écrit plus vite {}.'.format(answer))

            if int(guess.content) > answer:
                await ctx.send('-')
            elif int(guess.content) < answer:
                await ctx.send("+")
            elif int(guess.content) == answer:
                await ctx.send("bien joué trouvé ")
                a = profil.profiles(self, ctx.author, ctx.author.id, ctx, 1)
                return
    @commands.command()
    async def usd(self, ctx):
        await ctx.send('choisi un nombre entre 1 et 10.')

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        answer = random.randint(1, 10)
        try:
            guess = await self.bot.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.send('écrit plus vite  {}.'.format(answer))

        if int(guess.content) == answer:
            await ctx.send('Mouais tu à gagné ')
            a = profil.profiles(self, ctx.author, ctx.author.id, ctx, 10)
        else:
            await ctx.send("HA HA tu est nul c'est {}.".format(answer))

    @commands.command()
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




