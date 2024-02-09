import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import repeat
import valorant
import profile
import basique
import jeux

from repository.logRepository import add_log
from repository.messageRepository import new_message as new_message_repo
from repository.message_deleteRepository import new_message as new_message_delete_repo
from repository.message_editRepository import new_message as new_message_edit
from repository.utilisateurRepository import get_user_by_idUtilisateur, new_user

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self, command_prefix, description=None, intents=None):
        super().__init__(command_prefix, description=description, intents=intents)

    async def log_event(self, event_type, description):
        # Utilisez le repository pour ajouter des logs de manière asynchrone
        await self.loop.run_in_executor(None, add_log, event_type, description)

    async def on_ready(self):
        print('Le bot est OK !!!!')
        print('------')
        await self.log_event("Bot Status", "Le bot est connecté et prêt.")
        await self.setup_cogs()

    async def on_resumed(self):
        print("Reconnecté au serveur Discord.")
        await self.log_event("Reconnexion", "Le bot a été reconnecté au serveur Discord.")

    async def setup_cogs(self):
        await self.add_cog(repeat.Repeat(self))
        await self.add_cog(valorant.Valorant(self))
        await self.add_cog(profile.Profile(self))
        await self.add_cog(basique.commandeBasique(self))
        await self.add_cog(jeux.Jeux(self))

    async def on_message(self, message):
        if message.author.bot:
            return

        idUtilisateur = message.author.id
        pseudo = message.author.name
        try:
            utilisateur = await self.loop.run_in_executor(None, get_user_by_idUtilisateur, idUtilisateur)
            if not utilisateur:
                await self.loop.run_in_executor(None, new_user, idUtilisateur, pseudo)
                userId = idUtilisateur
            else:
                # Assurez-vous que cette ligne est correcte selon la structure de votre fonction get_user_by_idUtilisateur
                userId = utilisateur['id'] if isinstance(utilisateur, dict) else utilisateur[0]
            await self.loop.run_in_executor(None, new_message_repo, userId, message.content)
        except Exception as e:
            print(f"Erreur lors de l'insertion du message ou de l'utilisateur dans la base de données : {e}")
        await self.process_commands(message)

    async def on_message_delete(self, message):
        if message.author.bot:
            return

        idUtilisateur = message.author.id
        try:
            utilisateur = await self.loop.run_in_executor(None, get_user_by_idUtilisateur, idUtilisateur)
            if utilisateur:
                userId = utilisateur['id'] if isinstance(utilisateur, dict) else utilisateur[0]
                await self.loop.run_in_executor(None, new_message_delete_repo, userId, message.content)
        except Exception as e:
            print(f"Erreur lors de l'insertion du message supprimé dans la base de données : {e}")

    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        idUtilisateur = before.author.id
        try:
            utilisateur = await self.loop.run_in_executor(None, get_user_by_idUtilisateur, idUtilisateur)
            if utilisateur and before.content != after.content:
                userId = utilisateur['id'] if isinstance(utilisateur, dict) else utilisateur[0]
                await self.loop.run_in_executor(None, new_message_edit, userId, before.content, after.content)
        except Exception as e:
            print(f"Erreur lors de l'insertion du message modifié dans la base de données : {e}")

bot = MyBot(command_prefix="^^", description="Bot de Soyer", intents=intents)
bot.run(os.environ.get("TOKEN_DISCORD"))
