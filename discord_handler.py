import discord
from discord.ext import commands
import random


class YLBotClient(discord.Client):
    prefix = ''
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    # async def on_message(self, message):
    #     if message.author == self.user:
    #         return
    #     await message.channel.send(f'Я получил сообщение {message.content}')

class RandomThings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.admin_id = ''  # ID админа, который может всё
        self.mute_role_id = ''  # ID роли мута, которая молчит

    # @commands.command(name='roll_dice')
    # async def roll_dice(self, ctx, count):
    #     res = [random.choice(dashes) for _ in range(int(count))]
    #     await ctx.send(" ".join(res))

    @commands.command(name='randint')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)

    @commands.command(name='muteRole')
    async def set_mute_role(self, ctx, role):
        print(role)
        self.mute_role_id = int(role[3:-1])
        server = ctx.guild.id
        for channel in ctx.guild.text_channels:
            print(channel)
            await channel.set_permissions(ctx.guild.get_role(self.mute_role_id), send_messages=False)
        # print(type(ctx.guild.text_channels[0]))
        # print(dir(discord.guild.Guild))

TOKEN = "NzAxODc5ODU0NTIxNjQ3MTI0.Xp362w.ZUBqA0iw3GKsLSnKRe6KbdX_A_U"
bot = commands.Bot(command_prefix='-')
bot.add_cog(RandomThings(bot))
bot.run(TOKEN)
# client = YLBotClient()
# client.run(TOKEN)
