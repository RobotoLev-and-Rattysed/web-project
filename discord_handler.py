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


class MainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.admin_id = 0  # ID админа, который может всё
        self.moderation_role_id = 0  # ID роли модера, который может мутить
        self.mute_role_id = ''  # ID роли мута, которая молчит

    def has_role(self, member, role_id):
        for role in member.roles:
            if role.id == role_id:
                return True
        return False

    def is_admin(self, member):
        return member.id == self.admin_id or member.guild_permissions.administrator

    def is_moderator(self, member):
        return self.is_admin(member) or self.has_role(member, self.moderation_role_id)

    @commands.command(name='randint')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)

    @commands.command(name='muteRole')
    async def set_mute_role(self, ctx, role):
        if not self.is_moderator(ctx.author):
            return await self.perms_error(ctx)
        self.mute_role_id = int(role[3:-1])
        server = ctx.guild.id
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(ctx.guild.get_role(self.mute_role_id), send_messages=False)
        await ctx.message.channel.send('Mute Role has been updated succesfuly!')
        # print(type(ctx.guild.text_channels[0]))
        # print(dir(discord.guild.Guild))

    async def perms_error(self, ctx):
        await ctx.message.channel.send(f"{ctx.author.mention}, you don't have enought permissions to do that.")


TOKEN = "NzAxODc5ODU0NTIxNjQ3MTI0.Xp362w.ZUBqA0iw3GKsLSnKRe6KbdX_A_U"
bot = commands.Bot(command_prefix='-')
bot.add_cog(MainCommands(bot))
bot.run(TOKEN)
# client = YLBotClient()
# client.run(TOKEN)
