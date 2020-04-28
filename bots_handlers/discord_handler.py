import discord
import os
from settings import discord_key
from bots_infrastructure.bot_engine import is_command, get_answer


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
                with open(attachment[0], 'rb') as file:
                    await message.channel.send('', file=file)



client = DSBotClient()
client.run(discord_key)
