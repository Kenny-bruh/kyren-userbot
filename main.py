"""
KyrenUB - Main Entry Point
===========================
Starts the Pyrogram UserBot with a dummy Flask web server
to keep the dyno alive on Render / Heroku.
"""

import patches  # noqa: F401  — MUST be first import

import os
import sys
import time
import asyncio
import threading
from datetime import datetime

from pyrogram import Client
from pyrogram.errors import ApiIdInvalid, AuthKeyDuplicated

from config import Config
from plugins import load_plugins, CMD_LIST

START_TIME = time.time()
app = None


def run_web_server():
    """Minimal Flask server on configured PORT to keep Render dyno alive."""
    try:
        from flask import Flask, jsonify

        web = Flask(__name__)

        @web.route("/")
        def home():
            return jsonify({
                "status": "alive",
                "bot": "KyrenUB",
                "version": Config.BOT_VERSION,
                "uptime": round(time.time() - START_TIME, 2),
                "commands": sum(len(v) for v in CMD_LIST.values()),
                "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            })

        @web.route("/health")
        def health():
            return jsonify({"status": "ok"})

        @web.route("/stats")
        def stats():
            categories = {k: len(v) for k, v in CMD_LIST.items()}
            return jsonify({
                "total_commands": sum(categories.values()),
                "categories": categories,
            })

        port = int(os.getenv("PORT", Config.PORT))
        web.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
    except Exception as e:
        print(f"[WebServer] Failed to start: {e}")


def create_client() -> Client:
    return Client(
        name="KyrenUB",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=Config.STRING_SESSION,
        app_version=f"KyrenUB {Config.BOT_VERSION}",
        device_model="KyrenUB Server",
        system_version=f"Python {sys.version_info.major}.{sys.version_info.minor}",
        sleep_threshold=10,
        max_concurrent_transmissions=5,
    )


async def main():
    global app, START_TIME

    if not Config.validate():
        missing = Config.missing_vars()
        print(f"[KyrenUB] ERROR: Missing required config: {', '.join(missing)}")
        sys.exit(1)

    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    print("[KyrenUB] Web server started in background thread.")

    app = create_client()
    load_plugins(app)
    total_cmds = sum(len(v) for v in CMD_LIST.values())
    print(f"[KyrenUB] Loaded {total_cmds} commands across {len(CMD_LIST)} categories.")

    START_TIME = time.time()
    print("[KyrenUB] Starting client...")

    try:
        await app.start()
    except ApiIdInvalid:
        print("[KyrenUB] ERROR: API_ID or API_HASH is invalid.")
        sys.exit(1)
    except AuthKeyDuplicated:
        print("[KyrenUB] ERROR: Session already in use elsewhere.")
        sys.exit(1)
    except Exception as e:
        print(f"[KyrenUB] ERROR: Failed to start: {e}")
        sys.exit(1)

    me = await app.get_me()
    print(f"[KyrenUB] Logged in as {me.first_name} (@{me.username or 'N/A'}) [ID: {me.id}]")

    if Config.LOG_GROUP:
        try:
            await app.send_message(
                Config.LOG_GROUP,
                f"**KyrenUB v{Config.BOT_VERSION} Started**\n"
                f"👤 **User:** {me.first_name} (@{me.username or 'N/A'})\n"
                f"📋 **Commands:** {total_cmds}\n"
                f"🧩 **Categories:** {len(CMD_LIST)}\n"
                f"🐍 **Python:** {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n"
                f"⏰ **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            )
        except Exception:
            pass

    print("[KyrenUB] Bot is now running. Press Ctrl+C to stop.")
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        if Config.LOG_GROUP:
            try:
                await app.send_message(
                    Config.LOG_GROUP,
                    f"**KyrenUB Stopped**\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                )
            except Exception:
                pass
        await app.stop()
        print("[KyrenUB] Client stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[KyrenUB] Shutting down...")
    except Exception as e:
        print(f"[KyrenUB] Fatal error: {e}")
        sys.exit(1)
