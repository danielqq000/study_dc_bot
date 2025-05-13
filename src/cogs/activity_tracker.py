"""
activity_tracker.py
Last Update: 5/12/25

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
    async def activity(self, ctx, member: discord.Member = None):
        print("In activity")
        member = member or ctx.author
        print(f"In activity, member: {member}")
        stats = user_stats.get(member.id, {"Voice_seconds": 0, "messages": 0, "reactions": 0})
        joined = member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "Unknown"
        voice_minutes = stats["voice seconds"] / 60

        await ctx.send(
            f"活動統計 for {member.display_name}:\n"
            f"加入時間: {joined}\n"
            f"語音頻道總時長: {voice_minutes:.1f}\n"
            f"留言次數: {stats['messages']}\n"
            f"反應使用次數: {stats['reactions']}\n"
        )

async def setup(bot: commands.bot):
    await bot.add_cog(UserActivityTracker(bot))



