import discord
from discord.ext import commands
from lib.database import mycursor

class Bot_event(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if message.content == "Hello":
            await message.channel.send(f"Hello, {message.author}")
        elif message.content == "listuser":
            mycursor.execute("SELECT CUS_ID FROM CUSTOMER")
            myresult = mycursor.fetchall()
            await message.channel.send(myresult)
        
async def setup(bot):
    await bot.add_cog(Bot_event(bot))