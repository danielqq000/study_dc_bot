"""
main.py
Last Update: 5/12/25

Entry point
"""

import sys
import os
import asyncio

# 將 src 目錄加入到 sys.path 以便能夠從 src 中導入模組
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 現在可以導入 src 目錄內的模組了
from src.discord_dev import main

if __name__ == "__main__":
    asyncio.run(main())  # discord_dev.main(), 啟動機器人
