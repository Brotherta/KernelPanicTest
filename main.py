import os

import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ROLE_PARTICIPANT = os.getenv('ROLE_PARTICIPANT')
ROLE_PARTICIPANT_BOT = os.getenv('ROLE_PARTICIPANT_BOT')

BUFFER_NAME = {}


class KernelPanic(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(command_prefix="!kp", intents=discord.Intents(members=True, guilds=True, messages=True))
        self.remove_command("help")

    async def on_ready(self):
        print(f'{self.user} has connected to Discord !')


    async def on_member_join(self, member):
        guild = member.guild
        if not member.bot:
            role = guild.get_role(ROLE_PARTICIPANT)
            await member.add_roles(role)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True,
                                                    send_messages=True,
                                                    manage_channels=True,
                                                    manage_guild=True)
            }
            chan_name = "{}'s-env".format(member.name)
            await guild.create_category_channel(chan_name, overwrites=overwrites)
            categorie = None
            for cat in guild.categories:
                if cat.name == chan_name:
                    categorie = cat
                    break
            await guild.create_text_channel('general', overwrites=overwrites, category=categorie)

            for chan in categorie.text_channels:
                if chan.name == "general":
                    await chan.send(
                        "Salut <@{}> ! :wave:\nVoici ton channel de test, tu peux créer, supprimer et modifier "
                        "ce que tu veux ici. N'hésite pas à demander aux Admins de l'aide. "
                        "Tu as la permission d'inviter ton bot sur le serveur. ".format(member.id))
                    break

    async def on_message(self, message):
        if message.type == discord.MessageType.new_member and message.author.bot:
            new_bot = message.author
            guild = message.guild
            role = guild.get_role(ROLE_PARTICIPANT_BOT)  # role Bot Concours roles
            await new_bot.add_roles(role)
            async for entry in guild.audit_logs(limit=2):
                if entry.action == discord.AuditLogAction.bot_add:
                    user_name = entry.user.name
                    category = None
                    for cat in guild.categories:
                        if user_name in cat.name:
                            category = cat
                            break
                    await category.set_permissions(new_bot, read_messages=True, send_messages=True)

    async def on_guild_channel_update(self, before, after):
        print(before)
        print("-------------\n\n\n")
        print(after)

    async def on_member_remove(self, member):
        guild = member.guild
        category = None
        for cat in guild.categories:
            if member.name in cat.name:
                category = cat
                break
        for chan in category.channels:
            await chan.delete()
        await category.delete()


if __name__ == '__main__':
    bot = KernelPanic()
    bot.run(TOKEN, reconnect=True)
