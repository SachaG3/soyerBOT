import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

import profile.profile as profile
import basique
from game import jeux, valorant
from repository.listGuildRepository import get_guild, add_guild
from repository.utilisateurs_guildsRepository import new_utilisateur_guild, add_user_to_guild_if_not_exists
from spam import repeat

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
        await self.loop.run_in_executor(None, add_log, event_type, description)

    async def on_ready(self):
        print('Le bot est OK !!!!')
        print('------')
        await self.log_event("Bot Status", "Le bot est connecté et prêt.")
        await self.setup_cogs()

    async def on_resumed(self):
        await self.log_event("Bot Status", "Le bot a été reconnecté au serveur Discord.")

    async def on_guild_join(self, guild):
        await self.log_event("Bot Status", f"Le bot a rejoint le serveur : {guild.name}")

    async def on_guild_remove(self, guild):
        await self.log_event("Bot Status", f"Le bot a quitté le serveur : {guild.name}")

    async def on_command_error(self, ctx, error):
        await self.log_event("Commande Error",f"Erreur lors de l'exécution de la commande : {ctx.command}.\nErreur : {error}")

    async def on_guild_channel_create(self, channel):
        await self.log_event("Channel Status", f"Un canal a été créé: {channel}")

    async def on_guild_channel_delete(self, channel):
        await self.log_event("Channel Status", f"Un canal a été supprimé: {channel}")

    async def on_guild_channel_update(self, before, after):
        await self.log_event("Channel Status", f"Un canal a été mis à jour: {before} --> {after}")

    async def on_guild_role_create(self, role):
        await self.log_event("Role Status", f"Un rôle a été créé: {role}")

    async def on_guild_role_delete(self, role):
        await self.log_event("Role Status", f"Un rôle a été supprimé: {role}")

    async def on_guild_role_update(self, before, after):
        await self.log_event("Role Status", f"Un rôle a été mis à jour: {before} --> {after}")

    async def on_member_ban(self, guild, utilisateur):
        await self.log_event("Ban Status", f"{utilisateur} a été banni du serveur: {guild}")

    async def on_member_unban(self, guild, utilisateur):
        await self.log_event("Ban Status", f"{utilisateur} a été réintégré sur le serveur: {guild}")

    async def on_member_join(self, membre):
        user_id = membre.id
        guild_id = membre.guild.id

        try:
            user_in_db = await self.loop.run_in_executor(None, get_user_by_idUtilisateur, user_id)
            if not user_in_db:
                await self.log_event("Ajout utilisateur", f"Ajout d'un nouvel utilisateur: {user_id}")
                await self.loop.run_in_executor(None, new_user, user_id, membre.name)
            else:
                await self.log_event("Ajout utilisateur",f"L'utilisateur {user_id} existe déjà dans la base de données.")

            guild_in_db = await self.loop.run_in_executor(None, get_guild, guild_id)
            if not guild_in_db:
                await self.log_event("Ajout guilde", f"Ajout d'une nouvelle guilde: {guild_id}")
                await self.loop.run_in_executor(None, add_guild, guild_id, membre.guild.name)
            else:
                await self.log_event("Ajout guilde", f"La guilde {guild_id} existe déjà dans la base de données.")

            await self.log_event("Ajout utilisateur à guilde",f"Ajout de l'utilisateur {user_id} à la guilde {guild_id}.")
            await self.loop.run_in_executor(None, new_utilisateur_guild, user_id, guild_id)
        except Exception as e:
            await self.log_event("Erreur",f"Une erreur est survenue lors de l'ajout de l'utilisateur à la guilde : {e}")

    async def setup_cogs(self):
        await self.add_cog(repeat.Repeat(self))
        await self.add_cog(valorant.Valorant(self))
        await self.add_cog(profile.Profile(self))
        await self.add_cog(basique.commandeBasique(self))
        await self.add_cog(jeux.Jeux(self))

    async def on_message(self, message):

        idUtilisateur = message.author.id
        guild_id = message.guild.id
        guild_name = message.guild.name
        guild = get_guild(guild_id)
        pseudo = message.author.name
        try:
            utilisateur = await self.loop.run_in_executor(None, get_user_by_idUtilisateur, idUtilisateur)
            if not utilisateur:
                await self.loop.run_in_executor(None, new_user, idUtilisateur, pseudo)
                userId = utilisateur['id'] if isinstance(utilisateur, dict) else utilisateur[0]
            else:
                userId = utilisateur['id'] if isinstance(utilisateur, dict) else utilisateur[0]
            await self.loop.run_in_executor(None, new_message_repo, userId, message.content)

        except Exception as e:
            a = f"Erreur lors de l'insertion du message ou de l'utilisateur dans la base de données : {e}"
            await self.log_event("Bot error", a)
        if not guild:
            add_guild(guild_id, guild_name)
        add_user_to_guild_if_not_exists(userId, guild_id)
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
            a = f"Erreur lors de l'insertion du message supprimé dans la base de données : {e}"
            await self.log_event("Bot error", a)

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
            a = f"Erreur lors de l'insertion du message modifié dans la base de données : {e}"
            await self.log_event("Bot error", a)


bot = MyBot(command_prefix="^^", description="Bot de Soyer", intents=intents)
bot.run(os.environ.get("TOKEN_DISCORD"))
