# DiscordBot

一個多功能的 Discord 機器人，具備以下功能模組：

- 使用者語音頻道時長追蹤
- 表情反應紀錄
- 留言/發文分析
- 加入伺服器時間查詢
- 可擴充指令與事件監聽架構

## 📁 專案結構

```
DiscordBot/
├── Discord/  
│   ├── cogs/                 ⟶ 放置各類機器人功能模組  
│   │   ├── activity_tracker.py     ⟶ 語音/活動追蹤功能  
│   │   ├── commands.py             ⟶ 指令相關邏輯  
│   │   ├── event.py                ⟶ 事件監聽邏輯  
│   ├── discord_dev.py        ⟶ 主機器人入口  
│   ├── lib/                 
│   │   ├── config.py               ⟶ 配置管理（Token、設定值等）  
│   │   ├── database.py             ⟶ 資料庫連線與操作封裝  
│   ├── log/                        ⟶ 預留 log 存放目錄  
│   └── requirement.txt            ⟶ Python 相當契套套件清單  
├── SQL/  
│   └── create_table.sql     ⟶ 建立資料表的 SQL 腳本
```

## 📦 安裝方式

1. 建立處理環境（建議）：

```bash
python3 -m venv .venv  
source .venv/bin/activate
```

2. 安裝相當契套套件：

```bash
pip install -r requirement.txt
```

3. 設定環境變數或 config.py：

請複製config_example.py並建立local的config.py。

```bash
cd Discord/lib
cp config_example.py config.py
```

請於 lib/config.py 設定你的 Discord Bot Token、資料庫位置等必要參數。

## 🥪 執行方式

```bash
python3 discord_dev.py
```

或指定主程式位置：

```bash
cd Discord  
python3 discord_dev.py
```

## 🗃 資料庫初始化

如果你未建立資料表，請於 SQL/ 執行：

```bash
sqlite3 mybot.db < create_table.sql
```

你也可以修改成適用於 PostgreSQL 或 MySQL 等資料庫。

## 🔧 機器人功能與指令

- !activity @user → 查詢使用者語音頻道時長、訊息次數、反應次數、加入時間
- 更多指令請參考 cogs/ 目錄中的 command 說明與事件

## 📜 LICENSE

MIT License


