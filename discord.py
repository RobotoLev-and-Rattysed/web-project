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


TOKEN = "NjkzMTEwODgyNzYyMjI3NzU0.Xn4UNQ.jm2fqMpAa2XeGC34oSgLMlqEWUs"
client = YLBotClient()
client.run(TOKEN)
