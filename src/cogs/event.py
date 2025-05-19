import discord
from discord.ext import commands
from lib.database import DB_Process
from datetime import datetime, date

class Bot_event(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author == self.bot.user:
    #         return
        
    #     if message.content == "Hello":
    #         await message.channel.send(f"Hello, {message.author}")
    #     elif message.content == "commandtest":
    #         print("In commandtest")
    #         myresult = DB_Process.Get_Data("user_id, reaction", "user_data")
    #         print(myresult)
    #         await message.channel.send(myresult)
            
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            print(f"Who join the guild?\n ID: {member.id}\n Name: {member.name}")
            
            member_info = DB_Process.Get_Data("user_id", "user_data", f"WHERE `user_id` = '{member.name}'")
            
        except Exception as e:
            print(f"(on_member_join) - {repr(e)}")
        finally:
            
            if member_info:
                print(f"Find some information for Guild Member: {member.name}")
                DB_Process.Update_User_Info(member.name, "leave", False, "user_data")
                DB_Process.Update_User_Info(member.name, "joined_time", datetime.utcnow(), "user_data")
                print(f"(on_member_join) Finished Updating Info")
            else:
                print(f"Can't get any user information")
                DB_Process.Create_NewMember(member.name)
                print(f"Create a member sucessfully")
            
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            print(f"Who has left the guild: {member.name}")
            DB_Process.Update_User_Info(member.name, "leave", True, "user_data")
        except Exception as e:
            print(f"(on_member_remove) - {repr(e)}")
    
        
async def setup(bot):
    await bot.add_cog(Bot_event(bot))