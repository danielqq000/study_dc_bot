import discord
from discord.ext import commands

from lib.database import mycursor

class Bot_commands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def rank(self, ctx):
        await ctx.send(f"id: {ctx.author.id}\nchannel id: {ctx.channel.id}")


async def setup(bot):
    await bot.add_cog(Bot_commands(bot))