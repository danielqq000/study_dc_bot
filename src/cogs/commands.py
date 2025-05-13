"""
cogs/commands.py
Last Update: 5/12/25

基礎指令
"""

import discord
from discord.ext import commands
from discord import app_commands
from lib.config import GUILD_ID

from lib.database import mycursor

class Bot_commands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    # 查看等級排行, 用embed形式回覆
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="rank", description="查看你的等級和排行")
    async def rank(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        # fake data for now
        rank = 5
        level = 10
        exp = 1200
        next_level_exp = 1500

        # 輸出文字
        embed = discord.Embed(title=f"{interaction.user.display_name} 的等級資料", color=discord.Color.blue())
        embed.add_field(name="等級", value=f"Lv. {level}", inline=True)
        embed.add_field(name="經驗值", value=f"{exp}/ {next_level_exp}", inline=True)
        embed.add_field(name="伺服器排行", value=f"#{rank}", inline=False)
        await interaction.response.send_message(embed=embed)
        
    # 查看金幣數量
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="coin", description="查看你的金幣數量")
    async def coin(self, interaciton: discord.Interaction):
        print(f"coin: ")
        user_id = interaciton.user.id

        # fake data for now
        coin = 2357
        await interaciton.response.send_message(f"你目前擁有 {coins} 金幣")



async def setup(bot):
    await bot.add_cog(Bot_commands(bot))
