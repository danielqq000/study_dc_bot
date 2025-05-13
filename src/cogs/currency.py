"""
cogs/currency.py
Last Update: 5/12/25

currency相關指令
"""

import discord
from discord import app_commands
from discord.ext import commands
from lib.config import GUILD_ID

# data存儲未定案
user_exp_data = {}

class currencyCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # /currency add {user} {amount}
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="currency_add", description="增加某位使用者的貨幣")
    @app_commands.describe(user="要增加貨幣的使用者", amount="增加的數量")
    async def currency_add(self, interaction: discord.Interaction, user: discord.User, amount: int):
        user_currency_data[user.id] = user_currency_data.get(user.id, 0) + amount
        await interaction.response.send_message(f"已為 {user.mention} 增加 {amount} 金幣，目前為 {user_currency_data[user.id]}")

    # /currency remove {user} {amount}
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="currency_remove", description="減少某位使用者的貨幣")
    @app_commands.describe(user="要減少貨幣的使用者", amount="減少的數量")
    async def currency_remove(self, interaction: discord.Interaction, user: discord.User, amount: int):
        current = user_currency_data.get(user.id, 0)
        user_currency_data[user.id] = max(0, current - amount)
        await interaction.response.send_message(f"已為 {user.mention} 減少 {amount} 金幣，目前為 {user_currency_data[user.id]}")

    # /currency reset {user}
    @app_commands.guilds(discord.Object(GUILD_ID))
    @app_commands.command(name="currency_reset", description="重設某位使用者的貨幣為 0")
    @app_commands.describe(user="要重設的使用者")
    async def currency_reset(self, interaction: discord.Interaction, user: discord.User):
        before = user_currency_data.get(user.id, 0)
        user_currency_data[user.id] = 0
        await interaction.response.send_message(f"已將 {user.mention} 的金幣從 {before} 重設為 0")

    # /currency rank
    @app_commands.guilds(discord.Object(GUILD_ID))
    @app_commands.command(name="currency_rank", description="查看貨幣排行榜")
    async def currency_rank(self, interaction: discord.Interaction):
        if not user_currency_data:
            await interaction.response.send_message("目前尚無任何貨幣資料")
            return

        sorted_data = sorted(user_currency_data.items(), key=lambda x: x[1], reverse=True)
        embed = discord.Embed(title="貨幣排行榜", color=discord.Color.gold())

        for i, (user_id, amount) in enumerate(sorted_data[:10], start=1):
            user = await self.bot.fetch_user(user_id)
            embed.add_field(name=f"{i}. {user.display_name}", value=f"{amount} 金幣", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(currencyCommands(bot))
