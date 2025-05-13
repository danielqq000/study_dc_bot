"""
activity_tracker.py
Last Update: 5/13/25

追蹤並紀錄各activity,包含加入頻道,使用語音頻道時長,使用反應,發文留言
"""

import discord
from discord import app_commands
from discord.ext import commands
from lib.config import GUILD_ID

import datetime

# data存儲未定案
voice_sessions = {}
user_stats = {}

class UserActivityTracker(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    # 使用語音頻道時長
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        now = datetime.datetime.utcnow()
        user_id = member.id

        if after.channel and not before.channel:
            # 使用者加入頻道
            voice_sessions[user_id] = now
        elif before.channel and not after.channel:
            # 使用者離開頻道
            if user_id in voice_sessions:
                joined_time = voice_sessions.pop(user_id)
                duration = (now - joined_time).total_seconds()
                user_stats.setdefault(user_id, {"seconds": 0, "messages": 0, "reactions": 0})
                user_stats[user_id]["voice_seconds"] += duration

    # 留言統計
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        user_id = message.author.id
        user_stats.setdefault(user_id, {"seconds": 0, "messages": 0, "reactions": 0})
        user_stats[user_id]["messages"] += 1

    # 使用反應
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        user_id = user.id
        user_stats.setdefault(user_id, {"seconds": 0, "messages": 0, "reactions": 0})
        user_stats[user_id]["reactions"] += 1

    # 查詢使用者活動資料
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.command(name="activity", description="查看用戶活動")
    @app_commands.describe(member="要查詢的使用者")
    async def activity(self, interaction: discord.Interaction, member: discord.User):
        print(f"Checking activity, member: {member}")
        print(f"Getting stats...")
        stats = user_stats.get(member.id, {"seconds": 0, "messages": 0, "reactions": 0})
        print(f"stats: {stats}")
        print(f"Getting joined time...")
        joined = member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "Unknown"
        print(f"Getting voice time...")
        voice_minutes = stats['seconds'] / 60
        print(f"Done.")

        embed = discord.Embed(
            title=f"活動統計 - {member.display_name}",
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="加入時間", value=joined, inline=False)
        embed.add_field(name="語音頻道總時長", value=voice_minutes, inline=False)
        embed.add_field(name="留言次數", value=stats['messages'], inline=False)
        embed.add_field(name="反應使用次數", value=stats['reactions'], inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.bot):
    await bot.add_cog(UserActivityTracker(bot))



