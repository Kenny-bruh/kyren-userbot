# ⚡ KyrenUB — The Ultimate Pyrogram UserBot

![KyrenUB](https://img.shields.io/badge/KyrenUB-2.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12%2B-green?style=for-the-badge)
![Commands](https://img.shields.io/badge/Commands-850%2B-orange?style=for-the-badge)

**A feature-packed Pyrogram UserBot with 850+ commands across 17 categories — including VPS file bridge, GoFile uploader, AI chat/image, TTS, yt-dlp downloader, Docker manager, and persistent notes.**

---

## 🚀 Deploy to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Step-by-Step

1. **Fork this repo** to your GitHub account
2. **Get API credentials** from [https://my.telegram.org/apps](https://my.telegram.org/apps)
3. **Generate a String Session**: `pip install -r requirements.txt && python generate_session.py`
4. **Deploy on Render**: Create a Web Service, connect your repo, set env vars:

| Variable | Required | Description |
|----------|----------|-------------|
| `API_ID` | ✅ | Telegram API ID |
| `API_HASH` | ✅ | Telegram API Hash |
| `STRING_SESSION` | ✅ | Pyrogram string session |
| `PREFIX` | ❌ | Command prefix (default: `.`) |
| `LOG_GROUP` | ❌ | Chat ID for logs |

---

## 🖥️ Local Setup

```bash
git clone https://github.com/YOU/KyrenUB.git && cd KyrenUB
pip install -r requirements.txt
python generate_session.py
cp .env.sample .env  # Edit with your credentials
python main.py
```

---

## 📁 Project Structure

```
KyrenUB/
├── main.py              # Entry point + Flask web server
├── config.py            # Environment handler
├── patches.py           # Python 3.12+ monkey patches
├── generate_session.py  # Session generator
├── plugins/
│   ├── __init__.py      # Dynamic plugin loader
│   ├── core.py          # 34 commands - alive, ping, help, id, info...
│   ├── admin.py         # 46 commands - ban, mute, promote, lock...
│   ├── fun.py           # 120 commands - games, quotes, generators
│   ├── naughty.py       # 83 commands - roasts, flirts, spicy
│   ├── tools.py         # 119 commands - encoders, hash, QR...
│   ├── text.py          # 134 commands - fonts, encryption, decoration
│   ├── spam.py          # 23 commands - spam variants, animations
│   ├── media.py         # 57 commands - image ops, stickers, downloads
│   ├── system.py        # 56 commands - shell, eval, exec, git...
│   ├── dev.py           # 121 commands - API testing, format converters, hashes
│   ├── vps.py           # 37 commands - .pull/.push/.ls/.cat/.tail/.grep/.find/.zip
│   ├── gofile.py        # 4 commands  - .gofile upload + history + direct link
│   ├── tts.py           # 4 commands  - .tts/.stt voice messages
│   ├── downloader.py    # 11 commands - .ytdl/.insta/.tiktok/.twitter/.facebook
│   ├── ai.py            # 11 commands - .ai/.aimage/.summarize/.translate/.ocr/.wiki
│   ├── docker.py        # 3 commands  - .docker ps/logs/restart/exec/stats
│   ├── notes.py         # 7 commands  - .note/.clip/.todo/.remind persistent
│   └── chatdump.py      # 4 commands  - .dump/.dumpall/.exportmedia
├── .env.sample
├── requirements.txt
├── render.yml
└── README.md
```

---

## 🐍 Python 3.12+ Compatibility

`patches.py` is imported first and patches: `cgi`, `audioop`, `imghdr` (removed in 3.13), and `asyncio.get_event_loop` deprecation.

---

## ⚠️ Disclaimer

For educational purposes only. Use responsibly and at your own risk. Telegram may ban accounts violating their ToS.

---

<div align="center">**KyrenUB** — Made with ⚡</div>
