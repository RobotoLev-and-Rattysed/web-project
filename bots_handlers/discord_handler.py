import discord
import os
from settings import discord_key
from bots_infrastructure.bot_engine import is_command, get_answer
from data import db_session

db_session.global_init()

class DSBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user or not is_command(message.content):
            return
        answer = get_answer(message.content, 'discord')
        if answer.text or answer.attachments:
            text = answer.text
            await message.channel.send(f'{text}')
            if not answer.attachments:
                return
            for attachment in answer.attachments.values():
                try:
                    await message.channel.send('', file=discord.File(attachment[0]))
                except FileNotFoundError:
                    await message.channel.send('', file=discord.File(attachment[0][1:]))


client = DSBotClient()
client.run(discord_key)
