"""
discord_dev.py
Last Update: 5/12/25

BOT主程式
"""

import asyncio
import os

# 鎖定src base_path
base_path = os.path.dirname(__file__)

# 導入Discord.py模組
import discord
from discord import Object
from discord.ext import commands

from lib.database import mycursor
import lib.config as config

# client是跟discord連接，intents是要求機器人的權限
intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.reactions = True
intents.voice_states = True

# 機器人指令prefix
bot = commands.Bot(command_prefix = "$", intents = intents)

# 當機器人完成啟動
@bot.event
async def on_ready():
    print(f"目前登入身份 --> {bot.user}")
    try:
        guild = Object(id=config.GUILD_ID)
        print(f"指定測試伺服器: {guild}")
    except:
        print(f"沒有指定測試伺服器")
    synced = await bot.tree.sync(guild=guild)
    print(f"已同步 {len(synced)} 個指令")


# 載入指令程式檔
@bot.command()
async def load(ctx, extension_name):
    print(f"load called")
    extension = find_extension(extension_name)
    if not extension:
        await ctx.send(f"Load {extension_name} failed: not found.")
        return

    try:
        await bot.load_extension(extension)
    except Exception as e:
        await ctx.send(f"Load {extension_name} failed: {e}")
    else:
        await ctx.send(f"Load {extension_name} done.")

# 卸載指令程式檔
@bot.command()
async def unload(ctx, extension_name):
    print(f"unload called")
    extension = find_extension(extension_name)
    if not extension:
        await ctx.send(f"Unload {extension_name} failed: not found.")
        return

    try:
        await bot.unload_extension(extension)
    except Exception as e:
        await ctx.send(f"Unload {extension_name} failed: {e}")
    else:
        await ctx.send(f"Unload {extension_name} done.")

# 更新指令程式檔
@bot.command()
async def reload(ctx, extension_name):
    print(f"reload called")
    extension = find_extension(extension_name)
    if not extension:
        await ctx.send(f"Reload {extension_name} failed: not found.")
        return

    try:
        await bot.reload_extension(extension)
    except Exception as e:
        await ctx.send(f"Reload {extension_name} failed: {e}")
    else:
        await ctx.send(f"Reload {extension_name} done.")

# 遞歸加載 cogs 並顯示提示訊息
async def load_extensions():
    print("🔄 開始載入 Cogs...\n")
    for root, _, files in os.walk(os.path.join(base_path, 'cogs')):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                # Construct the extension path, adjust it to the module structure (remove base_path and replace '/' with '.')
                ext = os.path.join(root, file).replace(base_path, '').replace('/', '.').replace('\\', '.').replace('.py', "")
                # Remove leading dot (.) if present
                if ext.startswith('.'):
                    ext = ext[1:]

                try:
                    print(f"嘗試載入: {ext} ...")
                    await bot.load_extension(ext)
                    print(f"✅ 成功載入: {ext}")
                except Exception as e:
                    print(f"❌ 載入失敗: {ext} -> {e}")
    print("\n✅ 所有 Cogs 載入完成\n")
def find_extension(name):
    # 如果包含路径，則優先查找指定路徑下的文件
    if '.' in name:
        possible_path = name.replace('.', '/') + '.py'
        for root, _, files in os.walk('src/cogs'):
            for file in files:
                if os.path.join(root, file).endswith(possible_path):
                    return os.path.join(root, file).replace('./', '').replace('/', '.').replace('\\', '.').replace('.py', "")
    else:
        # 如果不包含路徑，查找第一个相符的文件
        for root, _, files in os.walk('./cogs'):
            for file in files:
                if file == f"{name}.py":
                    return os.path.join(root, file).replace('./', '').replace('/', '.').replace('\\', '.').replace('.py', "")
    return None
# main
async def main():
    await load_extensions()
    await bot.start(config.BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
