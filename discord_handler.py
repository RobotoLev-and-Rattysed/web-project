import discord
import requests


class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if any([word in message.content.lower()
                for word in {'кот', 'cat', 'кошк', 'коша', 'кис', 'кыс'}]):
            request = requests.get('https://api.thecatapi.com/v1/images/search')
            url = request.json()[0]['url']
            await message.channel.send(url)
        elif any([word in message.content.lower()
                  for word in {'пес', 'пёс', 'собак', 'собач', 'щен', 'dog'}]):
            request = requests.get('https://dog.ceo/api/breeds/image/random')
            url = request.json()['message']
            await message.channel.send(url)


TOKEN = "NzAxODc5ODU0NTIxNjQ3MTI0.Xp362w.ZUBqA0iw3GKsLSnKRe6KbdX_A_U"
client = YLBotClient()
client.run(TOKEN)
