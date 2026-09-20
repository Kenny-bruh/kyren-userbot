"""
KyrenUB - Spam Plugin
======================
23 commands for spamming, flooding, and animated text effects.
Uses Config.SPAM_LIMIT, Config.SPAM_DELAY, Config.FLOOD_LIMIT.
Handles FloodWait gracefully. Animations edit same message with asyncio.sleep.
"""


def register(app):
    from pyrogram import filters
    from pyrogram.errors import FloodWait
    from plugins import register_command
    from config import Config
    import asyncio
    import random

    # ═══════════════════════════════════════════════════════════════
    #  SPAM COMMANDS (13)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("spam", prefixes=".") & filters.me)
    async def spam_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.spam <count> <text>`")
            return
        try:
            count = int(args[1])
        except ValueError:
            await message.edit("❌ Count must be a number.")
            return
        if count < 1:
            await message.edit("❌ Count must be ≥ 1.")
            return
        if count > Config.SPAM_LIMIT:
            await message.edit(f"❌ Max limit is `{Config.SPAM_LIMIT}`.")
            return
        text = args[2]
        await message.delete()
        for _ in range(count):
            try:
                await client.send_message(message.chat.id, text)
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await client.send_message(message.chat.id, text)
            await asyncio.sleep(Config.SPAM_DELAY)

    register_command("Spam", "spam", "Spam text N times (max SPAM_LIMIT)", [])

    @app.on_message(filters.command(["stkspam", "sspam"], prefixes=".") & filters.me)
    async def stkspam_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.sticker:
            await message.edit("❌ Reply to a sticker to spam it.")
            return
        args = message.text.split(None, 1)
        try:
            count = int(args[1]) if len(args) > 1 else 5
        except ValueError:
            count = 5
        if count > Config.SPAM_LIMIT:
            await message.edit(f"❌ Max limit is `{Config.SPAM_LIMIT}`.")
            return
        sticker_id = message.reply_to_message.sticker.file_id
        await message.delete()
        for _ in range(count):
            try:
                await client.send_sticker(message.chat.id, sticker_id)
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await client.send_sticker(message.chat.id, sticker_id)
            await asyncio.sleep(Config.SPAM_DELAY)

    register_command("Spam", "stkspam", "Spam a sticker N times", ["sspam"])

    @app.on_message(filters.command(["txtspam", "tspam"], prefixes=".") & filters.me)
    async def txtspam_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.txtspam <count> <text>`")
            return
        try:
            count = int(args[1])
        except ValueError:
            await message.edit("❌ Count must be a number.")
            return
        if count < 1 or count > Config.SPAM_LIMIT:
            await message.edit(f"❌ Count must be 1-{Config.SPAM_LIMIT}.")
            return
        text = args[2]
        await message.delete()
        for _ in range(count):
            try:
                await client.send_message(message.chat.id, f"```{text}```")
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await client.send_message(message.chat.id, f"```{text}```")
            await asyncio.sleep(Config.SPAM_DELAY)

    register_command("Spam", "txtspam", "Spam text in monospace N times", ["tspam"])

    @app.on_message(filters.command("flood", prefixes=".") & filters.me)
    async def flood_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.flood <count> <text>`")
            return
        try:
            count = int(args[1])
        except ValueError:
            await message.edit("❌ Count must be a number.")
            return
        if count < 1 or count > Config.FLOOD_LIMIT:
            await message.edit(f"❌ Count must be 1-{Config.FLOOD_LIMIT}.")
            return
        text = args[2]
        await message.delete()
        for i in range(count):
            try:
                await client.send_message(message.chat.id, f"{text} {i+1}")
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await client.send_message(message.chat.id, f"{text} {i+1}")
            await asyncio.sleep(Config.SPAM_DELAY * 0.5)

    register_command("Spam", "flood", "Flood chat with numbered messages", [])

    @app.on_message(filters.command("bigspam", prefixes=".") & filters.me)
    async def bigspam_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.bigspam <count> <text>`")
            return
        try:
            count = int(args[1])
        except ValueError:
            await message.edit("❌ Count must be a number.")
            return
        limit = Config.SPAM_LIMIT * 10
        if count < 1 or count > limit:
            await message.edit(f"❌ Count must be 1-{limit}.")
            return
        text = args[2]
        await message.delete()
        for _ in range(count):
            try:
                await client.send_message(message.chat.id, text)
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await client.send_message(message.chat.id, text)
            await asyncio.sleep(Config.SPAM_DELAY * 0.5)

    register_command("Spam", "bigspam", "Spam with higher limit (SPAM_LIMIT×10)", [])

    @app.on_message(filters.command("picspam", prefixes=".") & filters.me)
    async def picspam_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo to spam it.")
            return
        args = message.text.split(None, 1)
        try:
            count = int(args[1]) if len(args) > 1 else 5
        except ValueError:
            count = 5
        if count > Config.SPAM_LIMIT:
            await message.edit(f"❌ Max limit is `{Config.SPAM_LIMIT}`.")
            return
        photo_id = message.reply_to_message.photo.file_id
        await message.delete()
        for _ in range(count):
            try:
                await client.send_photo(message.chat.id, photo_id)
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await client.send_photo(message.chat.id, photo_id)
            await asyncio.sleep(Config.SPAM_DELAY)

    register_command("Spam", "picspam", "Spam a photo N times", [])

    @app.on_message(filters.command("vidspam", prefixes=".") & filters.me)
    async def vidspam_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.video:
            await message.edit("❌ Reply to a video to spam it.")
            return
        args = message.text.split(None, 1)
        try:
            count = int(args[1]) if len(args) > 1 else 3
        except ValueError:
            count = 3
        if count > Config.SPAM_LIMIT:
            await message.edit(f"❌ Max limit is `{Config.SPAM_LIMIT}`.")
            return
        video_id = message.reply_to_message.video.file_id
        await message.delete()
        for _ in range(count):
            try:
                await client.send_video(message.chat.id, video_id)
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await client.send_video(message.chat.id, video_id)
            await asyncio.sleep(Config.SPAM_DELAY * 2)

    register_command("Spam", "vidspam", "Spam a video N times", [])

    @app.on_message(filters.command("msgspam", prefixes=".") & filters.me)
    async def msgspam_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message to spam it.")
            return
        args = message.text.split(None, 1)
        try:
            count = int(args[1]) if len(args) > 1 else 5
        except ValueError:
            count = 5
        if count > Config.SPAM_LIMIT:
            await message.edit(f"❌ Max limit is `{Config.SPAM_LIMIT}`.")
            return
        r = message.reply_to_message
        await message.delete()
        for _ in range(count):
            try:
                await r.copy(message.chat.id)
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await r.copy(message.chat.id)
            await asyncio.sleep(Config.SPAM_DELAY)

    register_command("Spam", "msgspam", "Spam a replied message N times", [])

    @app.on_message(filters.command("emojis", prefixes=".") & filters.me)
    async def emojis_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.emojis <count> <emoji>`")
            return
        try:
            count = int(args[1])
        except ValueError:
            await message.edit("❌ Count must be a number.")
            return
        if count > 100:
            await message.edit("❌ Max 100 emojis.")
            return
        emoji = args[2].strip()
        await message.delete()
        text = emoji * count
        try:
            await client.send_message(message.chat.id, text)
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await client.send_message(message.chat.id, text)

    register_command("Spam", "emojis", "Send emoji repeated N times", [])

    @app.on_message(filters.command("letterspam", prefixes=".") & filters.me)
    async def letterspam_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.letterspam <count> <letter>`")
            return
        try:
            count = int(args[1])
        except ValueError:
            await message.edit("❌ Count must be a number.")
            return
        if count > Config.SPAM_LIMIT:
            await message.edit(f"❌ Max limit is `{Config.SPAM_LIMIT}`.")
            return
        letter = args[2][0] if args[2] else "a"
        await message.delete()
        for _ in range(count):
            try:
                await client.send_message(message.chat.id, letter)
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await client.send_message(message.chat.id, letter)
            await asyncio.sleep(Config.SPAM_DELAY * 0.3)

    register_command("Spam", "letterspam", "Spam a single letter N times", [])

    @app.on_message(filters.command("numberspam", prefixes=".") & filters.me)
    async def numberspam_cmd(client, message):
        args = message.text.split(None, 1)
        try:
            count = int(args[1]) if len(args) > 1 else 10
        except ValueError:
            count = 10
        if count > Config.SPAM_LIMIT:
            await message.edit(f"❌ Max limit is `{Config.SPAM_LIMIT}`.")
            return
        await message.delete()
        for i in range(1, count + 1):
            try:
                await client.send_message(message.chat.id, str(i))
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await client.send_message(message.chat.id, str(i))
            await asyncio.sleep(Config.SPAM_DELAY * 0.3)

    register_command("Spam", "numberspam", "Spam numbers 1 to N", [])

    @app.on_message(filters.command("countdownspam", prefixes=".") & filters.me)
    async def countdownspam_cmd(client, message):
        args = message.text.split(None, 1)
        try:
            count = int(args[1]) if len(args) > 1 else 10
        except ValueError:
            count = 10
        if count > 50:
            await message.edit("❌ Max 50.")
            return
        await message.delete()
        for i in range(count, 0, -1):
            try:
                msg = await client.send_message(message.chat.id, f"💥 **{i}**")
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                msg = await client.send_message(message.chat.id, f"💥 **{i}**")
            await asyncio.sleep(1)
            try:
                await msg.delete()
            except Exception:
                pass

    register_command("Spam", "countdownspam", "Animated countdown spam", [])

    @app.on_message(filters.command("bomb", prefixes=".") & filters.me)
    async def bomb_cmd(client, message):
        args = message.text.split(None, 1)
        try:
            count = int(args[1]) if len(args) > 1 else 5
        except ValueError:
            count = 5
        if count > 30:
            await message.edit("❌ Max 30.")
            return
        await message.delete()
        for i in range(count, 0, -1):
            try:
                msg = await client.send_message(message.chat.id, f"💣 **{i}**")
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                msg = await client.send_message(message.chat.id, f"💣 **{i}**")
            await asyncio.sleep(0.5)
            try:
                await msg.delete()
            except Exception:
                pass
        try:
            await client.send_message(message.chat.id, "💥 **BOOM!**")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await client.send_message(message.chat.id, "💥 **BOOM!**")

    register_command("Spam", "bomb", "Bomb animation with countdown", [])

    # ═══════════════════════════════════════════════════════════════
    #  ANIMATION COMMANDS (10) — edit same message with asyncio.sleep
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("matrix", prefixes=".") & filters.me)
    async def matrix_cmd(client, message):
        msg = await message.edit("🟢")
        frames = [
            "🟢⬛⬛⬛⬛\n⬛⬛⬛⬛⬛\n⬛⬛⬛⬛⬛",
            "🟢🟢⬛⬛⬛\n⬛🟢⬛⬛⬛\n⬛⬛⬛⬛⬛",
            "🟢🟢🟢⬛⬛\n⬛🟢🟢⬛⬛\n⬛⬛🟢⬛⬛",
            "🟢🟢🟢🟢⬛\n⬛🟢🟢🟢⬛\n⬛⬛🟢🟢⬛",
            "🟢🟢🟢🟢🟢\n⬛🟢🟢🟢🟢\n⬛⬛🟢🟢🟢",
            "⬛🟢🟢🟢🟢\n⬛⬛🟢🟢🟢\n⬛⬛⬛🟢🟢",
            "⬛⬛🟢🟢🟢\n⬛⬛⬛🟢🟢\n⬛⬛⬛⬛🟢",
            "⬛⬛⬛🟢🟢\n⬛⬛⬛⬛🟢\n⬛⬛⬛⬛⬛",
        ]
        for frame in frames:
            try:
                await msg.edit(frame)
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await msg.edit(frame)
            await asyncio.sleep(0.4)
        try:
            await msg.edit("🟢 **Matrix** 🟢")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await msg.edit("🟢 **Matrix** 🟢")

    register_command("Spam", "matrix", "Matrix rain animation", [])

    @app.on_message(filters.command("rain", prefixes=".") & filters.me)
    async def rain_cmd(client, message):
        msg = await message.edit("🌧")
        frames = [
            "💧     \n  💧   \n    💧 ",
            "  💧   \n    💧 \n💧     ",
            "    💧 \n💧     \n  💧   ",
            "💧     \n  💧   \n    💧 ",
            "  💧   \n    💧 \n💧     ",
        ]
        for _ in range(3):
            for frame in frames:
                try:
                    await msg.edit(frame)
                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)
                    await msg.edit(frame)
                await asyncio.sleep(0.5)
        try:
            await msg.edit("🌧 **Rain** 🌧")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await msg.edit("🌧 **Rain** 🌧")

    register_command("Spam", "rain", "Rain animation", [])

    @app.on_message(filters.command("wave", prefixes=".") & filters.me)
    async def wave_cmd(client, message):
        args = message.text.split(None, 1)
        text = args[1] if len(args) > 1 else "KyrenUB"
        msg = await message.edit("🌊")
        for i in range(len(text) * 2):
            pos = i % len(text)
            display = list(text)
            display[pos] = f"**{display[pos]}**"
            try:
                await msg.edit("".join(display))
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await msg.edit("".join(display))
            await asyncio.sleep(0.3)
        try:
            await msg.edit(f"🌊 **{text}** 🌊")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await msg.edit(f"🌊 **{text}** 🌊")

    register_command("Spam", "wave", "Wave animation on text", [])

    @app.on_message(filters.command("scroll", prefixes=".") & filters.me)
    async def scroll_cmd(client, message):
        args = message.text.split(None, 1)
        text = args[1] if len(args) > 1 else "KyrenUB"
        msg = await message.edit("📜")
        padded = " " * 10 + text + " " * 10
        for i in range(len(padded) - 10):
            display = padded[i:i+10]
            try:
                await msg.edit(f"📜 `{display}`")
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await msg.edit(f"📜 `{display}`")
            await asyncio.sleep(0.3)
        try:
            await msg.edit(f"📜 **{text}**")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await msg.edit(f"📜 **{text}**")

    register_command("Spam", "scroll", "Scrolling text animation", [])

    @app.on_message(filters.command("progress", prefixes=".") & filters.me)
    async def progress_cmd(client, message):
        msg = await message.edit("⏳ 0%")
        total = 10
        for i in range(1, total + 1):
            filled = "█" * i
            empty = "░" * (total - i)
            pct = int((i / total) * 100)
            bar = f"`[{filled}{empty}]` {pct}%"
            try:
                await msg.edit(f"⏳ {bar}")
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await msg.edit(f"⏳ {bar}")
            await asyncio.sleep(0.5)
        try:
            await msg.edit("✅ **Complete!**")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await msg.edit("✅ **Complete!**")

    register_command("Spam", "progress", "Progress bar animation", [])

    @app.on_message(filters.command("heartbeat", prefixes=".") & filters.me)
    async def heartbeat_cmd(client, message):
        msg = await message.edit("❤️")
        frames = ["❤️", "🧡", "💛", "💚", "💙", "💜", "💙", "💚", "💛", "🧡"]
        for _ in range(3):
            for frame in frames:
                try:
                    await msg.edit(frame)
                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)
                    await msg.edit(frame)
                await asyncio.sleep(0.3)
        try:
            await msg.edit("❤️ **Heartbeat** ❤️")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await msg.edit("❤️ **Heartbeat** ❤️")

    register_command("Spam", "heartbeat", "Heartbeat animation", [])

    @app.on_message(filters.command("explosion", prefixes=".") & filters.me)
    async def explosion_cmd(client, message):
        msg = await message.edit("🔥")
        frames = ["🟡", "🟠", "🔴", "💥", "⬛", "🌫", "✨"]
        for frame in frames:
            try:
                await msg.edit(frame)
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await msg.edit(frame)
            await asyncio.sleep(0.5)
        try:
            await msg.edit("💥 **BOOM!** 💥")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await msg.edit("💥 **BOOM!** 💥")

    register_command("Spam", "explosion", "Explosion animation", [])

    @app.on_message(filters.command("rocket", prefixes=".") & filters.me)
    async def rocket_cmd(client, message):
        msg = await message.edit("🚀")
        frames = [
            "⬛⬛⬛⬛\n⬛⬛⬛⬛\n⬛⬛⬛⬛\n⬛⬛🚀⬛",
            "⬛⬛⬛⬛\n⬛⬛⬛⬛\n⬛⬛🚀⬛\n⬛⬛🔥⬛",
            "⬛⬛⬛⬛\n⬛⬛🚀⬛\n⬛⬛🔥⬛\n⬛⬛⬛⬛",
            "⬛⬛🚀⬛\n⬛⬛🔥⬛\n⬛⬛⬛⬛\n⬛⬛⬛⬛",
            "⬛🚀⬛⬛\n⬛🔥⬛⬛\n⬛⬛⬛⬛\n⬛⬛⬛⬛",
            "🚀⬛⬛⬛\n🔥⬛⬛⬛\n⬛⬛⬛⬛\n⬛⬛⬛⬛",
        ]
        for _ in range(2):
            for frame in frames:
                try:
                    await msg.edit(frame)
                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)
                    await msg.edit(frame)
                await asyncio.sleep(0.4)
        try:
            await msg.edit("🚀 **Launched!** 🚀")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await msg.edit("🚀 **Launched!** 🚀")

    register_command("Spam", "rocket", "Rocket launch animation", [])

    @app.on_message(filters.command("snake", prefixes=".") & filters.me)
    async def snake_cmd(client, message):
        msg = await message.edit("🐍")
        frames = [
            "⬛⬛⬛⬛⬛\n⬛🐍⬛⬛⬛\n⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛\n⬛⬛🐍⬛⬛\n⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛\n⬛⬛⬛🐍⬛\n⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛\n⬛⬛⬛⬛🐍\n⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛\n⬛⬛⬛🐍⬛\n⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛\n⬛⬛🐍⬛⬛\n⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛\n⬛🐍⬛⬛⬛\n⬛⬛⬛⬛⬛",
            "⬛⬛⬛⬛⬛\n🐍⬛⬛⬛⬛\n⬛⬛⬛⬛⬛",
        ]
        for _ in range(2):
            for frame in frames:
                try:
                    await msg.edit(frame)
                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)
                    await msg.edit(frame)
                await asyncio.sleep(0.3)
        try:
            await msg.edit("🐍 **Snake** 🐍")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await msg.edit("🐍 **Snake** 🐍")

    register_command("Spam", "snake", "Snake animation", [])

    @app.on_message(filters.command("loading", prefixes=".") & filters.me)
    async def loading_cmd(client, message):
        msg = await message.edit("⏳")
        frames = ["⏳", "⏳.", "⏳..", "⏳...", "⏳....", "⏳....."]
        for _ in range(3):
            for frame in frames:
                try:
                    await msg.edit(frame)
                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)
                    await msg.edit(frame)
                await asyncio.sleep(0.4)
        try:
            await msg.edit("✅ **Loaded!**")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await msg.edit("✅ **Loaded!**")

    register_command("Spam", "loading", "Loading dots animation", [])
