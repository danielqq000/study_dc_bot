"""
cogs/exp.py
Last Update: 5/12/25

exp相關指令
"""

import discord
from discord import app_commands
from discord.ext import commands
from lib.config import GUILD_ID
from lib.database import DB_Process

class ExpCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # /xp add {user} {amount}
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="xp_add", description="增加某位使用者的經驗值")
    @app_commands.describe(user="要增加經驗值的用戶", amount="要增加的數值")
    async def xp_add(self, interaction: discord.Interaction, user: discord.User, amount: int):
        try:
            user_info = DB_Process.Get_Data("`user_id`, `leave`", "`user_data`", f"WHERE `user_id` = '{user.name}'")
            # print(f"(xp_add) user_info: {user_info}")
        except Exception as e:
            print(f"(xp_add) - {repr(e)}")
        finally:
            if user_info and user_info[0][1]:
                await interaction.response.send_message(f"使用者 {user.mention} 不是這個群組的成員")
            elif user_info:
                result = DB_Process.Create_Xp(DB_Process, user_info[0][0], amount, "1052552300192866374")
                if result:
                    user_xp_info = DB_Process.Get_Data("`user_id`, SUM(`xp_add`) as `sum`", "`xp_log`", f'WHERE `user_id` = "{user.name}"')
                    await interaction.response.send_message(f"已為 {user.mention} 增加 {amount} 經驗值，目前為 {user_xp_info[0][1]} XP")
                else:
                    await interaction.response.send_message(f"為 {user.mention} 增加 {amount} 經驗值失敗")
            else:
                await interaction.response.send_message(f"無法找到任何關於 {user.mention} 的資訊")

    # /xp remove {user} {amount}
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="xp_remove", description="減少某位使用者的經驗值")
    @app_commands.describe(user="要減少經驗值的用戶", amount="要減少的數值")
    async def xp_remove(self, interaction: discord.Interaction, user: discord.User, amount: int):
        try:
            user_info = DB_Process.Get_Data("`user_id`, `leave`", "`user_data`", f"WHERE `user_id` = '{user.name}'")
            # print(f"(xp_remove) user_info: {user_info}")
        except Exception as e:
            print(f"(xp_remove) - {repr(e)}")
        finally:
            if user_info and user_info[0][1]:
                await interaction.response.send_message(f"使用者 {user.mention} 不是這個群組的成員")
            elif user_info:
                result = DB_Process.Create_Xp(DB_Process, user_info[0][0], 0 - amount, "1052552300192866374")
                if result:
                    user_xp_info = DB_Process.Get_Data("`user_id`, SUM(`xp_add`) as `sum`", "`xp_log`", f'WHERE `user_id` = "{user.name}"')
                    await interaction.response.send_message(f"已為 {user.mention} 減少 {amount} 經驗值，目前為 {user_xp_info[0][1]} XP")
                else:
                    await interaction.response.send_message(f"為 {user.mention} 減少 {amount} 經驗值失敗")
            else:
                await interaction.response.send_message(f"無法找到任何關於 {user.mention} 的資訊")

    # /xp reset {user}
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="xp_reset", description="重置某位使用者的經驗值")
    @app_commands.describe(user="要重置的使用者")
    async def xp_reset(self, interaction: discord.Interaction, user: discord.User):
        try:
            user_info = DB_Process.Get_Data("`user_id`, `leave`", "`user_data`", f"WHERE `user_id` = '{user.name}'")
            user_xp_info_before = DB_Process.Get_Data("`user_id`, SUM(`xp_add`) as `sum`", "`xp_log`", f'WHERE `user_id` = "{user.name}"')
            amount = user_xp_info_before[0][1]
            print(f"(xp_reset) user_xp_info_before: {user_xp_info_before}")
            print(f"(xp_reset) amount: {amount}")
            print(f"(xp_reset) type of amount: {type(amount)}")
        except Exception as e:
            print(f"(xp_reset) - {repr(e)}")
        finally:
            if user_info and user_info[0][1]:
                await interaction.response.send_message(f"使用者 {user.mention} 不是這個群組的成員")
            elif user_info:
                result = DB_Process.Create_Xp(DB_Process, user_info[0][0], 0 - int(amount), "1052552300192866374")
                if result:
                    user_xp_info_after = DB_Process.Get_Data("`user_id`, SUM(`xp_add`) as `sum`", "`xp_log`", f'WHERE `user_id` = "{user.name}"')
                    await interaction.response.send_message(f"已將 {user.mention} 的經驗值從 {amount} 重設為 {user_xp_info_after[0][1]} XP")
                else:
                    await interaction.response.send_message(f"已將 {user.mention} 的經驗值從 {amount} 重設為 {user_xp_info_after[0][1]} XP 失敗")
            else:
                await interaction.response.send_message(f"無法找到任何關於 {user.mention} 的資訊")

    # /xp rank
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="xp_rank", description="查看伺服器的經驗值排行榜")
    async def xp_rank(self, interaction: discord.Interaction):
        try:
            user_xp_info = DB_Process.Get_Data("x.`user_id`, SUM(`xp_add`) as `sum`", "`xp_log` x", f'RIGHT JOIN (SELECT u.user_id FROM user_data u WHERE u.leave = 0) as UN ON UN.user_id = x.user_id\n'f'GROUP BY `user_id`\n'f'ORDER BY `sum` DESC')
            print(f"(xp_rank) user_xp_info: {user_xp_info}")
        except Exception as e:
            print(f"(xp_rank) - {repr(e)}")
        finally:
            i = 0
            if not user_xp_info:
                await interaction.response.send_message("目前尚無經驗值資料。")
                return
            
            embed = discord.Embed(title="經驗值排行榜", color=discord.Color.green())
            
            for user_info in user_xp_info:
                embed.add_field(name=f"{i+1}, {user_info[0]}", value=f"{user_info[1]} XP", inline=False)
                i += 1
            
            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ExpCommands(bot))
