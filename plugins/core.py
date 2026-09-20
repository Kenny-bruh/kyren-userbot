"""
KyrenUB - Core Plugin
======================
34 commands that form the backbone of the UserBot.
Categories: alive, ping, help, uptime, repeat, echo, me, id, info,
            chatinfo, stats, ver, setprefix, purge, delme, search,
            pin, unpin, leave, join, copy, forward, save, quoted,
            admins, members, profile, setname, setbio, setpfp,
            delpfp, caption, log, broadcast
"""


def register(app):
    from pyrogram import filters
    from pyrogram.errors import FloodWait
    from pyrogram.types import (
        InlineKeyboardMarkup,
        InlineKeyboardButton,
    )
    from plugins import register_command, CMD_LIST
    from config import Config
    import time
    import sys
    import asyncio
    import os
    from datetime import datetime, timedelta

    # ── Plugin load time (used as bot start proxy for uptime) ──
    _start = time.time()

    # ── Session-scoped prefix storage ──────────────────────────
    _custom_prefix = [Config.PREFIX]

    # ── Category emoji map for help ────────────────────────────
    _CAT_EMOJI = {
        "Core": "🔧",
        "Admin": "👑",
        "Fun": "🎮",
        "Naughty": "😈",
        "Tools": "🛠",
        "Text": "✏️",
        "Spam": "💥",
        "Media": "🎬",
        "System": "⚙️",
    }

    # ── Helpers ────────────────────────────────────────────────
    def _uptime():
        sec = int(time.time() - _start)
        d, rem = divmod(sec, 86400)
        h, rem = divmod(rem, 3600)
        m, s = divmod(rem, 60)
        return f"{d}d {h}h {m}m {s}s"

    def _pyver():
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def _total_cmds():
        return sum(len(v) for v in CMD_LIST.values())

    # ═══════════════════════════════════════════════════════════
    # 1. ALIVE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("alive", prefixes=".") & filters.me)
    async def alive_cmd(client, message):
        start = time.time()
        ping_ms = round((time.time() - start) * 1000)
        # Send and edit for a more accurate ping
        msg = await message.edit("⚡...")
        ping_ms = round((time.time() - start) * 1000)
        text = (
            f"⚡ **KyrenUB is Alive!**\n\n"
            f"📊 **Ping:** `{ping_ms} ms`\n"
            f"⏱ **Uptime:** `{_uptime()}`\n"
            f"📋 **Commands:** `{_total_cmds()}`\n"
            f"🐍 **Python:** `{_pyver()}`\n"
            f"📦 **Version:** `{Config.BOT_VERSION}`\n"
            f"👤 **Owner:** {Config.OWNER_USERNAME.lstrip('@')}"
        )
        try:
            await msg.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await msg.edit(text)

    register_command("Core", "alive", "Show bot status with uptime and stats")

    # ═══════════════════════════════════════════════════════════
    # 2. PING
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("ping", prefixes=".") & filters.me)
    async def ping_cmd(client, message):
        start = time.time()
        msg = await message.edit("🏓 Pong!")
        end = time.time()
        ms = round((end - start) * 1000)
        try:
            await msg.edit(f"🏓 **Pong!** `{ms} ms`")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await msg.edit(f"🏓 **Pong!** `{ms} ms`")

    register_command("Core", "ping", "Measure response time in ms")

    # ═══════════════════════════════════════════════════════════
    # 3. HELP
    # ═══════════════════════════════════════════════════════════
    def _chunk_text(text, limit=4000):
        parts = []
        while len(text) > limit:
            cut = text.rfind("\n", 0, limit)
            if cut == -1:
                cut = limit
            parts.append(text[:cut])
            text = text[cut:].lstrip("\n")
        if text:
            parts.append(text)
        return parts or [""]

    @app.on_message(filters.command("help", prefixes=".") & filters.me)
    async def help_cmd(client, message):
        if not CMD_LIST:
            await message.edit("❌ No commands registered yet.")
            return

        pfx = _custom_prefix[0]
        args = message.text.split(None, 1)
        query = args[1].strip().lower() if len(args) > 1 else None

        if query:
            cat = next((c for c in CMD_LIST if c.lower() == query), None)
            if not cat:
                await message.edit(
                    f"❌ Category `{query}` not found.\n"
                    f"Use `{pfx}help` to list all categories."
                )
                return
            text = f"{_CAT_EMOJI.get(cat, '📁')} **{cat}** — `{len(CMD_LIST[cat])}` commands\n\n"
            for cmd in CMD_LIST[cat]:
                aliases = f" ({', '.join(cmd['aliases'])})" if cmd.get("aliases") else ""
                text += f"• `{pfx}{cmd['name']}`{aliases} — {cmd['help']}\n"
            chunks = _chunk_text(text)
            try:
                await message.edit(chunks[0])
                for extra in chunks[1:]:
                    await message.reply(extra)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await message.edit(chunks[0])
            except Exception as e:
                await message.edit(f"❌ Help failed: `{e}`")
            return

        text = f"📖 **KyrenUB Help** — `{_total_cmds()}` commands\n"
        text += f"📌 **Prefix:** `{pfx}`  |  Use `{pfx}help <category>`\n\n"
        for cat in sorted(CMD_LIST.keys()):
            emoji = _CAT_EMOJI.get(cat, "📁")
            text += f"{emoji} **{cat}** — `{len(CMD_LIST[cat])}` commands\n"
        chunks = _chunk_text(text)
        try:
            await message.edit(chunks[0])
            for extra in chunks[1:]:
                await message.reply(extra)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(chunks[0])
        except Exception as e:
            await message.edit(f"❌ Help failed: `{e}`")

    register_command("Core", "help", "Show all commands categorized with emojis")

    # ═══════════════════════════════════════════════════════════
    # 4. UPTIME
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("uptime", prefixes=".") & filters.me)
    async def uptime_cmd(client, message):
        await message.edit(f"⏱ **Uptime:** `{_uptime()}`")

    register_command("Core", "uptime", "Show bot uptime in human readable format")

    # ═══════════════════════════════════════════════════════════
    # 5. REPEAT (alias: rp)
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command(["repeat", "rp"], prefixes=".") & filters.me)
    async def repeat_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.repeat <count> <text>`")
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
                await asyncio.sleep(e.value)
                await client.send_message(message.chat.id, text)
            await asyncio.sleep(Config.SPAM_DELAY)

    register_command("Core", "repeat", "Repeat text N times (max SPAM_LIMIT)", aliases=["rp"])

    # ═══════════════════════════════════════════════════════════
    # 6. ECHO
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("echo", prefixes=".") & filters.me)
    async def echo_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) > 1:
            text = args[1]
        elif message.reply_to_message:
            text = message.reply_to_message.text or message.reply_to_message.caption or ""
        else:
            await message.edit("❌ **Usage:** `.echo <text>` or reply to a message.")
            return
        await message.delete()
        try:
            await client.send_message(message.chat.id, text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.send_message(message.chat.id, text)

    register_command("Core", "echo", "Echo text or replied message")

    # ═══════════════════════════════════════════════════════════
    # 7. ME
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("me", prefixes=".") & filters.me)
    async def me_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.me <action>`")
            return
        action = args[1]
        me = await client.get_me()
        name = me.first_name
        await message.delete()
        try:
            await client.send_message(message.chat.id, f"_{name} {action}_")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.send_message(message.chat.id, f"_{name} {action}_")

    register_command("Core", "me", "Send /me action in italics")

    # ═══════════════════════════════════════════════════════════
    # 8. ID
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("id", prefixes=".") & filters.me)
    async def id_cmd(client, message):
        text = f"💬 **Chat ID:** `{message.chat.id}`"
        if message.reply_to_message:
            replied = message.reply_to_message.from_user
            if replied:
                text += f"\n👤 **Replied User ID:** `{replied.id}`"
            if message.reply_to_message.forward_from:
                text += f"\n↗️ **Forward From ID:** `{message.reply_to_message.forward_from.id}`"
        else:
            text += f"\n👤 **Your ID:** `{message.from_user.id}`"
        if message.chat.type != "private":
            text += f"\n👥 **Chat Type:** `{message.chat.type}`"
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Core", "id", "Show chat ID, user ID, replied user ID")

    # ═══════════════════════════════════════════════════════════
    # 9. INFO
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("info", prefixes=".") & filters.me)
    async def info_cmd(client, message):
        if message.reply_to_message and message.reply_to_message.from_user:
            user = message.reply_to_message.from_user
        else:
            args = message.text.split(None, 1)
            if len(args) > 1:
                try:
                    user = await client.get_users(args[1])
                except Exception:
                    await message.edit("❌ User not found.")
                    return
            else:
                user = await client.get_me()

        if isinstance(user, list):
            user = user[0]

        status_map = {
            "online": "🟢 Online",
            "offline": "🔴 Offline",
            "recently": "🟡 Recently",
            "last_week": "⚪ Last Week",
            "last_month": "⚪ Last Month",
        }
        status = status_map.get(str(user.status), "⚪ Unknown") if user.status else "⚪ Unknown"

        text = (
            f"👤 **User Info**\n\n"
            f"📛 **Name:** {user.first_name}"
            + (f" {user.last_name}" if user.last_name else "")
            + "\n"
        )
        if user.username:
            text += f"🌐 **Username:** @{user.username}\n"
        text += (
            f"🆔 **ID:** `{user.id}`\n"
            f"📡 **DC:** `{user.dc_id or 'N/A'}`\n"
            f"🟢 **Status:** {status}\n"
            f"🤖 **Bot:** `{user.is_bot}`\n"
            f"⛔ **Restricted:** `{user.is_scam or False}`\n"
            f"✅ **Verified:** `{user.is_verified or False}`\n"
            f"🏷 **Mutual:** `{user.is_mutual_contact or False}`\n"
        )
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Core", "info", "Detailed user info (name, username, id, dc, status)")

    # ═══════════════════════════════════════════════════════════
    # 10. CHATINFO
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("chatinfo", prefixes=".") & filters.me)
    async def chatinfo_cmd(client, message):
        chat = message.chat
        try:
            full_chat = await client.get_chat(chat.id)
        except Exception as e:
            await message.edit(f"❌ Failed to get chat info: {e}")
            return

        text = f"💬 **Chat Info**\n\n"
        text += f"📛 **Title:** {full_chat.title or 'N/A'}\n"
        if full_chat.username:
            text += f"🌐 **Username:** @{full_chat.username}\n"
        text += f"🆔 **ID:** `{full_chat.id}`\n"
        text += f"🏷 **Type:** `{full_chat.type.value}`\n"
        if full_chat.members_count:
            text += f"👥 **Members:** `{full_chat.members_count}`\n"
        if full_chat.description:
            desc = full_chat.description[:200]
            text += f"📝 **Description:** {desc}\n"
        if full_chat.dc_id:
            text += f"📡 **DC:** `{full_chat.dc_id}`\n"
        if full_chat.pinned_message:
            text += f"📌 **Pinned:** Message ID `{full_chat.pinned_message.id}`\n"
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Core", "chatinfo", "Chat title, members, type, description")

    # ═══════════════════════════════════════════════════════════
    # 11. STATS
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("stats", prefixes=".") & filters.me)
    async def stats_cmd(client, message):
        if not CMD_LIST:
            await message.edit("❌ No stats available.")
            return
        total = _total_cmds()
        text = f"📊 **KyrenUB Stats**\n\n"
        text += f"📋 **Total Commands:** `{total}`\n"
        text += f"🧩 **Categories:** `{len(CMD_LIST)}`\n"
        text += f"⏱ **Uptime:** `{_uptime()}`\n"
        text += f"🐍 **Python:** `{_pyver()}`\n\n"
        for cat in sorted(CMD_LIST.keys()):
            emoji = _CAT_EMOJI.get(cat, "📁")
            text += f"{emoji} **{cat}:** `{len(CMD_LIST[cat])}` commands\n"
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Core", "stats", "Bot stats with category breakdown")

    # ═══════════════════════════════════════════════════════════
    # 12. VER (alias: version)
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command(["ver", "version"], prefixes=".") & filters.me)
    async def ver_cmd(client, message):
        text = (
            f"📦 **KyrenUB v{Config.BOT_VERSION}**\n"
            f"🐍 **Python:** {_pyver()}\n"
            f"📋 **Commands:** `{_total_cmds()}`\n"
            f"🔗 **Repo:** {Config.BOT_REPO}"
        )
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Core", "ver", "Show bot version and Python version", aliases=["version"])

    # ═══════════════════════════════════════════════════════════
    # 13. SETPREFIX
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("setprefix", prefixes=".") & filters.me)
    async def setprefix_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit(
                f"❌ **Usage:** `.setprefix <prefix>`\n"
                f"📌 **Current:** `{_custom_prefix[0]}`"
            )
            return
        new_prefix = args[1].strip()
        old_prefix = _custom_prefix[0]
        _custom_prefix[0] = new_prefix
        # Update Pyrogram's command prefixes for this client
        # Since we can't easily change global prefixes at runtime,
        # store it and inform the user it applies to next restart
        try:
            await message.edit(
                f"✅ **Prefix changed:** `{old_prefix}` → `{new_prefix}`\n"
                f"⚠️ Note: This affects custom prefix tracking only. "
                f"Restart required for full effect."
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(
                f"✅ **Prefix changed:** `{old_prefix}` → `{new_prefix}`\n"
                f"⚠️ Note: This affects custom prefix tracking only. "
                f"Restart required for full effect."
            )

    register_command("Core", "setprefix", "Change command prefix for the session")

    # ═══════════════════════════════════════════════════════════
    # 14. PURGE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("purge", prefixes=".") & filters.me)
    async def purge_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message to start purging from.")
            return
        start_id = message.reply_to_message.id
        end_id = message.id
        count = 0
        for msg_id in range(start_id, end_id + 1):
            try:
                await client.delete_messages(message.chat.id, msg_id)
                count += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await client.delete_messages(message.chat.id, msg_id)
                    count += 1
                except Exception:
                    pass
            except Exception:
                pass
        try:
            notify = await client.send_message(
                message.chat.id,
                f"🗑 **Purged** `{count}` **messages.**"
            )
            await asyncio.sleep(3)
            await notify.delete()
        except FloodWait as e:
            await asyncio.sleep(e.value)

    register_command("Core", "purge", "Delete messages from reply to current")

    # ═══════════════════════════════════════════════════════════
    # 15. DELME
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("delme", prefixes=".") & filters.me)
    async def delme_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message to delete it.")
            return
        try:
            await client.delete_messages(
                message.chat.id,
                message.reply_to_message.id
            )
            await message.delete()
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.delete_messages(
                message.chat.id,
                message.reply_to_message.id
            )
            await message.delete()
        except Exception as e:
            await message.edit(f"❌ Failed to delete: {e}")

    register_command("Core", "delme", "Delete the replied message")

    # ═══════════════════════════════════════════════════════════
    # 16. SEARCH
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("search", prefixes=".") & filters.me)
    async def search_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.search <query>`")
            return
        query = args[1]
        results = []
        try:
            async for msg in client.search_messages(message.chat.id, query, limit=10):
                if msg.text:
                    snippet = msg.text[:80].replace("\n", " ")
                    results.append(f"• [`{msg.id}`] {snippet}...")
                elif msg.caption:
                    snippet = msg.caption[:80].replace("\n", " ")
                    results.append(f"• [`{msg.id}`] {snippet}...")
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            await message.edit(f"❌ Search failed: {e}")
            return

        if not results:
            await message.edit(f"🔍 No results for: `{query}`")
            return

        text = f"🔍 **Search results for:** `{query}`\n\n" + "\n".join(results)
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Core", "search", "Search messages in chat")

    # ═══════════════════════════════════════════════════════════
    # 17. PIN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("pin", prefixes=".") & filters.me)
    async def pin_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message to pin it.")
            return
        try:
            await client.pin_chat_message(
                message.chat.id,
                message.reply_to_message.id,
                disable_notification=True,
            )
            await message.edit("📌 **Message pinned!**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.pin_chat_message(
                message.chat.id,
                message.reply_to_message.id,
                disable_notification=True,
            )
            await message.edit("📌 **Message pinned!**")
        except Exception as e:
            await message.edit(f"❌ Failed to pin: {e}")

    register_command("Core", "pin", "Pin replied message")

    # ═══════════════════════════════════════════════════════════
    # 18. UNPIN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("unpin", prefixes=".") & filters.me)
    async def unpin_cmd(client, message):
        if message.reply_to_message:
            msg_id = message.reply_to_message.id
        else:
            msg_id = None  # Unpin all if no reply
        try:
            if msg_id:
                await client.unpin_chat_message(message.chat.id, msg_id)
                await message.edit("📌 **Message unpinned!**")
            else:
                await client.unpin_all_chat_messages(message.chat.id)
                await message.edit("📌 **All messages unpinned!**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if msg_id:
                await client.unpin_chat_message(message.chat.id, msg_id)
                await message.edit("📌 **Message unpinned!**")
            else:
                await client.unpin_all_chat_messages(message.chat.id)
                await message.edit("📌 **All messages unpinned!**")
        except Exception as e:
            await message.edit(f"❌ Failed to unpin: {e}")

    register_command("Core", "unpin", "Unpin message")

    # ═══════════════════════════════════════════════════════════
    # 19. LEAVE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("leave", prefixes=".") & filters.me)
    async def leave_cmd(client, message):
        if message.chat.type == "private":
            await message.edit("❌ Can't leave a private chat.")
            return
        try:
            await message.edit("👋 Leaving chat...")
            await client.leave_chat(message.chat.id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.leave_chat(message.chat.id)
        except Exception as e:
            await message.edit(f"❌ Failed to leave: {e}")

    register_command("Core", "leave", "Leave current chat")

    # ═══════════════════════════════════════════════════════════
    # 20. JOIN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("join", prefixes=".") & filters.me)
    async def join_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.join <username or invite link>`")
            return
        target = args[1].strip()
        try:
            await client.join_chat(target)
            await message.edit(f"✅ **Joined:** `{target}`")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.join_chat(target)
            await message.edit(f"✅ **Joined:** `{target}`")
        except Exception as e:
            await message.edit(f"❌ Failed to join: {e}")

    register_command("Core", "join", "Join via username or invite link")

    # ═══════════════════════════════════════════════════════════
    # 21. COPY
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("copy", prefixes=".") & filters.me)
    async def copy_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message to copy it.")
            return
        args = message.text.split(None, 1)
        if len(args) < 2:
            target_chat = message.chat.id
        else:
            try:
                target_chat = int(args[1])
            except ValueError:
                target_chat = args[1]
        try:
            await message.reply_to_message.copy(target_chat)
            await message.edit("✅ **Message copied!**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(target_chat)
            await message.edit("✅ **Message copied!**")
        except Exception as e:
            await message.edit(f"❌ Failed to copy: {e}")

    register_command("Core", "copy", "Copy message to another chat")

    # ═══════════════════════════════════════════════════════════
    # 22. FORWARD
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("forward", prefixes=".") & filters.me)
    async def forward_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message to forward it.")
            return
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.forward <chat_id or username>`")
            return
        target = args[1].strip()
        try:
            target_chat = int(target)
        except ValueError:
            target_chat = target
        try:
            await message.reply_to_message.forward(target_chat)
            await message.edit("✅ **Message forwarded!**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.forward(target_chat)
            await message.edit("✅ **Message forwarded!**")
        except Exception as e:
            await message.edit(f"❌ Failed to forward: {e}")

    register_command("Core", "forward", "Forward message to another chat")

    # ═══════════════════════════════════════════════════════════
    # 23. SAVE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("save", prefixes=".") & filters.me)
    async def save_cmd(client, message):
        if not message.reply_to_message:
            args = message.text.split(None, 1)
            if len(args) < 2:
                await message.edit("❌ Reply to a message or provide text to save.")
                return
            try:
                await client.send_message("me", args[1])
                await message.edit("✅ **Saved to Saved Messages!**")
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await client.send_message("me", args[1])
                await message.edit("✅ **Saved to Saved Messages!**")
            except Exception as e:
                await message.edit(f"❌ Failed to save: {e}")
        else:
            try:
                await message.reply_to_message.copy("me")
                await message.edit("✅ **Saved to Saved Messages!**")
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await message.reply_to_message.copy("me")
                await message.edit("✅ **Saved to Saved Messages!**")
            except Exception as e:
                await message.edit(f"❌ Failed to save: {e}")

    register_command("Core", "save", "Save to Saved Messages")

    # ═══════════════════════════════════════════════════════════
    # 24. QUOTED
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("quoted", prefixes=".") & filters.me)
    async def quoted_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message to get its quote info.")
            return
        r = message.reply_to_message
        text = f"💬 **Quoted Message Info**\n\n"
        text += f"🆔 **Message ID:** `{r.id}`\n"
        if r.from_user:
            name = r.from_user.first_name
            if r.from_user.last_name:
                name += f" {r.from_user.last_name}"
            text += f"👤 **From:** {name} (`{r.from_user.id}`)\n"
            if r.from_user.username:
                text += f"🌐 **Username:** @{r.from_user.username}\n"
        if r.date:
            text += f"📅 **Date:** `{r.date.strftime('%Y-%m-%d %H:%M:%S')}`\n"
        if r.forward_from:
            text += f"↗️ **Forwarded from:** `{r.forward_from.id}`\n"
        if r.forward_from_chat:
            text += f"↗️ **Forwarded from chat:** `{r.forward_from_chat.title}` (`{r.forward_from_chat.id}`)\n"
        if r.reply_to_message:
            text += f"↩️ **Replies to:** `{r.reply_to_message.id}`\n"
        if r.text:
            snippet = r.text[:100].replace("\n", " ")
            text += f"📝 **Text:** {snippet}\n"
        elif r.caption:
            snippet = r.caption[:100].replace("\n", " ")
            text += f"📝 **Caption:** {snippet}\n"
        if r.media:
            text += f"📎 **Media:** `{type(r.media).__name__}`\n"
        if r.views:
            text += f"👁 **Views:** `{r.views}`\n"
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Core", "quoted", "Info about the replied-to message")

    # ═══════════════════════════════════════════════════════════
    # 25. ADMINS
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("admins", prefixes=".") & filters.me)
    async def admins_cmd(client, message):
        if message.chat.type == "private":
            await message.edit("❌ This command works only in groups/channels.")
            return
        admin_list = []
        try:
            async for admin in client.get_chat_members(message.chat.id, filter="administrators"):
                name = admin.user.first_name
                if admin.user.last_name:
                    name += f" {admin.user.last_name}"
                rank = admin.custom_title or ("Creator" if admin.status == "creator" else "Admin")
                admin_list.append(f"• {name} (`{admin.user.id}`) — {rank}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            async for admin in client.get_chat_members(message.chat.id, filter="administrators"):
                name = admin.user.first_name
                if admin.user.last_name:
                    name += f" {admin.user.last_name}"
                rank = admin.custom_title or ("Creator" if admin.status == "creator" else "Admin")
                admin_list.append(f"• {name} (`{admin.user.id}`) — {rank}")
        except Exception as e:
            await message.edit(f"❌ Failed to fetch admins: {e}")
            return

        if not admin_list:
            await message.edit("❌ No admins found.")
            return

        text = f"👑 **Admins** ({len(admin_list)})\n\n" + "\n".join(admin_list)
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Core", "admins", "List group admins")

    # ═══════════════════════════════════════════════════════════
    # 26. MEMBERS
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("members", prefixes=".") & filters.me)
    async def members_cmd(client, message):
        try:
            chat = await client.get_chat(message.chat.id)
            count = chat.members_count or "N/A"
            text = f"👥 **Members:** `{count}`"
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            chat = await client.get_chat(message.chat.id)
            count = chat.members_count or "N/A"
            text = f"👥 **Members:** `{count}`"
            await message.edit(text)
        except Exception as e:
            await message.edit(f"❌ Failed to get member count: {e}")

    register_command("Core", "members", "Show member count")

    # ═══════════════════════════════════════════════════════════
    # 27. PROFILE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("profile", prefixes=".") & filters.me)
    async def profile_cmd(client, message):
        if message.reply_to_message and message.reply_to_message.from_user:
            user = message.reply_to_message.from_user
        else:
            user = await client.get_me()

        text = f"👤 **Profile**\n\n"
        text += f"📛 **Name:** {user.first_name}"
        if user.last_name:
            text += f" {user.last_name}"
        text += "\n"
        if user.username:
            text += f"🌐 **Username:** @{user.username}\n"
        text += f"🆔 **ID:** `{user.id}`\n"
        if user.bio:
            text += f"📝 **Bio:** {user.bio}\n"
        if user.dc_id:
            text += f"📡 **DC:** `{user.dc_id}`\n"
        if user.photo:
            text += f"🖼 **Photo:** Has profile photo\n"
        else:
            text += f"🖼 **Photo:** No profile photo\n"
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Core", "profile", "Show your profile info")

    # ═══════════════════════════════════════════════════════════
    # 28. SETNAME
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("setname", prefixes=".") & filters.me)
    async def setname_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.setname <first name>`")
            return
        first_name = args[1].strip()
        try:
            await client.update_profile(first_name=first_name)
            await message.edit(f"✅ **First name set to:** `{first_name}`")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.update_profile(first_name=first_name)
            await message.edit(f"✅ **First name set to:** `{first_name}`")
        except Exception as e:
            await message.edit(f"❌ Failed to set name: {e}")

    register_command("Core", "setname", "Set first name")

    # ═══════════════════════════════════════════════════════════
    # 29. SETBIO
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("setbio", prefixes=".") & filters.me)
    async def setbio_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.setbio <bio text>`")
            return
        bio = args[1].strip()
        try:
            await client.update_profile(bio=bio)
            await message.edit(f"✅ **Bio set to:** `{bio}`")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.update_profile(bio=bio)
            await message.edit(f"✅ **Bio set to:** `{bio}`")
        except Exception as e:
            await message.edit(f"❌ Failed to set bio: {e}")

    register_command("Core", "setbio", "Set bio/about")

    # ═══════════════════════════════════════════════════════════
    # 30. SETPFP
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("setpfp", prefixes=".") & filters.me)
    async def setpfp_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo to set as profile picture.")
            return
        try:
            photo = await message.reply_to_message.download()
            await client.set_profile_photo(photo=photo)
            os.remove(photo)
            await message.edit("✅ **Profile photo updated!**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.set_profile_photo(photo=photo)
            os.remove(photo)
            await message.edit("✅ **Profile photo updated!**")
        except Exception as e:
            await message.edit(f"❌ Failed to set profile photo: {e}")

    register_command("Core", "setpfp", "Set profile photo from replied photo")

    # ═══════════════════════════════════════════════════════════
    # 31. DELPFP
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("delpfp", prefixes=".") & filters.me)
    async def delpfp_cmd(client, message):
        args = message.text.split(None, 1)
        count = 1
        if len(args) > 1:
            try:
                count = int(args[1])
            except ValueError:
                await message.edit("❌ Count must be a number.")
                return
        try:
            photos = []
            async for photo in client.get_profile_photos("me"):
                photos.append(photo)
                if len(photos) >= count:
                    break
            if not photos:
                await message.edit("❌ No profile photos found.")
                return
            photo_ids = [p.id for p in photos[:count]]
            await client.delete_profile_photos(photo_ids)
            await message.edit(f"✅ **Deleted** `{len(photo_ids)}` **profile photo(s).**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            photo_ids = [p.id for p in photos[:count]]
            await client.delete_profile_photos(photo_ids)
            await message.edit(f"✅ **Deleted** `{len(photo_ids)}` **profile photo(s).**")
        except Exception as e:
            await message.edit(f"❌ Failed to delete profile photos: {e}")

    register_command("Core", "delpfp", "Delete profile photos")

    # ═══════════════════════════════════════════════════════════
    # 32. CAPTION
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("caption", prefixes=".") & filters.me)
    async def caption_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a media message to change its caption.")
            return
        if not message.reply_to_message.media:
            await message.edit("❌ Replied message has no media.")
            return
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.caption <new caption>`")
            return
        new_caption = args[1]
        try:
            await message.reply_to_message.copy(
                message.chat.id,
                caption=new_caption,
            )
            await message.reply_to_message.delete()
            await message.delete()
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(
                message.chat.id,
                caption=new_caption,
            )
            await message.reply_to_message.delete()
            await message.delete()
        except Exception as e:
            await message.edit(f"❌ Failed to change caption: {e}")

    register_command("Core", "caption", "Change caption of replied media")

    # ═══════════════════════════════════════════════════════════
    # 33. LOG
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("log", prefixes=".") & filters.me)
    async def log_cmd(client, message):
        if not Config.LOG_GROUP:
            await message.edit("❌ LOG_GROUP is not configured.")
            return
        args = message.text.split(None, 1)
        if message.reply_to_message:
            try:
                await message.reply_to_message.copy(Config.LOG_GROUP)
                await message.edit("✅ **Message logged to LOG_GROUP.**")
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await message.reply_to_message.copy(Config.LOG_GROUP)
                await message.edit("✅ **Message logged to LOG_GROUP.**")
            except Exception as e:
                await message.edit(f"❌ Failed to log: {e}")
        elif len(args) > 1:
            try:
                await client.send_message(Config.LOG_GROUP, args[1])
                await message.edit("✅ **Logged to LOG_GROUP.**")
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await client.send_message(Config.LOG_GROUP, args[1])
                await message.edit("✅ **Logged to LOG_GROUP.**")
            except Exception as e:
                await message.edit(f"❌ Failed to log: {e}")
        else:
            await message.edit("❌ **Usage:** `.log <text>` or reply to a message.")

    register_command("Core", "log", "Send message to LOG_GROUP")

    # ═══════════════════════════════════════════════════════════
    # 34. BROADCAST (sudo only)
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("broadcast", prefixes=".") & filters.me)
    async def broadcast_cmd(client, message):
        me = await client.get_me()
        if Config.SUDO_USERS and me.id not in Config.SUDO_USERS:
            await message.edit("❌ **Sudo only command.**")
            return

        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.broadcast <message>`")
            return
        broadcast_text = args[1]
        sent = 0
        failed = 0
        await message.edit("📢 **Broadcasting...**")

        # Collect all dialogs (groups/channels)
        dialogs = []
        try:
            async for dialog in client.get_dialogs():
                if dialog.chat.type in ("group", "supergroup"):
                    dialogs.append(dialog.chat.id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            async for dialog in client.get_dialogs():
                if dialog.chat.type in ("group", "supergroup"):
                    dialogs.append(dialog.chat.id)
        except Exception as e:
            await message.edit(f"❌ Failed to get dialogs: {e}")
            return

        for chat_id in dialogs:
            try:
                await client.send_message(chat_id, broadcast_text)
                sent += 1
                await asyncio.sleep(Config.SPAM_DELAY)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await client.send_message(chat_id, broadcast_text)
                    sent += 1
                except Exception:
                    failed += 1
            except Exception:
                failed += 1

        try:
            await message.edit(
                f"📢 **Broadcast Complete**\n\n"
                f"✅ **Sent:** `{sent}`\n"
                f"❌ **Failed:** `{failed}`\n"
                f"📊 **Total:** `{sent + failed}`"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(
                f"📢 **Broadcast Complete**\n\n"
                f"✅ **Sent:** `{sent}`\n"
                f"❌ **Failed:** `{failed}`\n"
                f"📊 **Total:** `{sent + failed}`"
            )

    register_command("Core", "broadcast", "Send to all groups (sudo only)")
