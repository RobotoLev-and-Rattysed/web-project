import discord


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        await message.channel.send(f'Я получил сообщение {message.content}')


TOKEN = "NzAxODc5ODU0NTIxNjQ3MTI0.Xp362w.ZUBqA0iw3GKsLSnKRe6KbdX_A_U"
client = YLBotClient()
client.run(TOKEN)
