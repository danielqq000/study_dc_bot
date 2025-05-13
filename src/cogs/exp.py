"""
cogs/exp.py
Last Update: 5/12/25

exp相關指令
"""

import discord
from discord import app_commands
from discord.ext import commands
from lib.config import GUILD_ID

# data存儲未定案
user_exp_data = {}

class ExpCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # /xp add {user} {amount}
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="xp_add", description="增加某位使用者的經驗值")
    @app_commands.describe(user="要增加經驗值的用戶", amount="要增加的數值")
    async def xp_add(self, interaction: discord.Interaction, user: discord.User, amount: int):
        user_exp_data[user.id] = user_exp_data.get(user.id, 0) + amount
        await interaction.response.send_message(f"已為 {user.mention} 增加 {amount} 經驗值，目前為 {user_exp_data[user.id]} XP")

    # /xp remove {user} {amount}
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="xp_remove", description="減少某位使用者的經驗值")
    @app_commands.describe(user="要減少經驗值的用戶", amount="要減少的數值")
    async def xp_remove(self, interaction: discord.Interaction, user: discord.User, amount: int):
        current = user_exp_data.get(user.id, 0)
        user_exp_data[user.id] = max(0, current - amount)
        await interaction.response.send_message(f"已為 {user.mention} 減少 {amount} 經驗值，目前為 {user_exp_data[user.id]} XP")

    # /xp reset {user}
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="xp_reset", description="重置某位使用者的經驗值")
    @app_commands.describe(user="要重置的使用者")
    async def xp_reset(self, interaction: discord.Interaction, user: discord.User):
        before = user_exp_data.get(user.id, 0)
        user_exp_data[user.id] = 0
        await interaction.response.send_message(f"已將 {user.mention} 的經驗值從 {before} 重設為 0 XP")

    # /xp rank
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="xp_rank", description="查看伺服器的經驗值排行榜")
    async def xp_rank(self, interaction: discord.Interaction):
        if not user_exp_data:
            await interaction.response.send_message("目前尚無經驗值資料。")
            return

        sorted_users = sorted(user_exp_data.items(), key=lambda x: x[1], reverse=True)
        embed = discord.Embed(title="經驗值排行榜", color=discord.Color.green())

        for i, (user_id, xp) in enumerate(sorted_users[:10], start=1):
            user = await self.bot.fetch_user(user_id)
            embed.add_field(name=f"{i}. {user.display_name}", value=f"{xp} XP", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ExpCommands(bot))
