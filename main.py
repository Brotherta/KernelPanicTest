import os
import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

logger = logging.getLogger('LSDStats')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='KernelPanicTest.log',
    encoding='utf-8',
    mode='w'
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
))
logger.addHandler(handler)


class KernelPanic(commands.AutoShardedBot):

    def __init__(self):
        super().__init__(command_prefix="!kp", intents=discord.Intents(members=True, guilds=True))
        self.remove_command("help")

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        await self.process_commands(message)

    async def on_member_join(self, member):
        guild = member.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True,
                                                send_messages=True,
                                                manage_channels=True)
        }
        guild_name = "{}'s-env".format(member.name)

        await guild.create_category_channel(guild_name, overwrites=overwrites)
        categorie = None
        for cat in guild.categories:
            if cat.name == guild_name:
                categorie=cat
                break
        await guild.create_text_channel('general', overwrites=overwrites, category=categorie)

        for chan in categorie.text_channels:
            if chan.name == "general":
                await chan.send("Salut <@{}> ! :wave:\nVoici ton channel de test, tu peux créer, supprimer et modifier "
                                "ce que tu veux ici. N'hésite pas à demander aux Admins de l'aide."
                                "\nTu trouveras plus d'informations ici :point_right: "
                                "https://discord.com/channels/687978521796411441/810083294543740938".format(member.id))
                break



if __name__ == '__main__':
    bot = KernelPanic()
    bot.run(TOKEN, reconnect=True)




















