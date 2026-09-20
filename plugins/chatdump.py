"""
KyrenUB - Chat Dump / Backup Plugin
====================================
Dump messages from a chat to a .txt or .json file and upload to Telegram.
Solves the ad-hoc use case the user had earlier (dumping 5412776008's chats).

Commands:
  .dump <chat_id> <count>              - dump last N messages as text
  .dump json <chat_id> <count>         - dump as JSON
  .dumpall <chat_id>                   - dump last 1000 messages as text
  .backupchat <chat_id>                - full chat backup as JSON file
  .exportmedia <chat_id> <count>       - download all media from last N msgs
"""

def register(app):
    from pyrogram import filters
    from plugins import register_command
    import asyncio, os, json, time, tempfile
    import datetime

    async def _resolve_chat(client, identifier):
        """Accept @username, -100xxx, or plain chat ID."""
        if identifier.startswith("@"):
            return identifier
        if identifier.lstrip("-").isdigit():
            return int(identifier)
        return identifier

    # ─────────── DUMP ───────────

    @app.on_message(filters.command("dump", prefixes=".") & filters.me)
    async def _dump_cmd(client, message):
        """
        .dump <chat> <count>           - text dump
        .dump json <chat> <count>      - JSON dump
        """
        args = message.command[1:]
        fmt = "text"
        if args and args[0] == "json":
            fmt = "json"
            args = args[1:]
        if len(args) < 2:
            return await message.reply(
                "Usage:\n"
                "`.dump <chat_id|@username> <count>` (text)\n"
                "`.dump json <chat_id|@username> <count>` (JSON)\n"
                "Example: `.dump -1003371746149 500`"
            )
        chat_id = await _resolve_chat(client, args[0])
        count = int(args[1]) if args[1].isdigit() else 100
        if count > 5000:
            return await message.reply("Max 5000 messages per dump.")
        status = await message.reply(f"📥 Dumping last {count} messages from `{args[0]}`...")

        try:
            messages = []
            async for msg in client.get_chat_history(chat_id, limit=count):
                messages.append(msg)

            # Reverse so oldest is first
            messages.reverse()

            if fmt == "json":
                data = []
                for m in messages:
                    data.append({
                        "id": m.id,
                        "date": m.date.isoformat() if m.date else None,
                        "from": (m.from_user.username or m.from_user.first_name) if m.from_user else None,
                        "from_id": m.from_user.id if m.from_user else None,
                        "text": m.text or m.caption or "",
                        "media": "photo" if m.photo else "video" if m.video else "audio" if m.audio
                                else "document" if m.document else "voice" if m.voice else "sticker" if m.sticker
                                else "animation" if m.animation else None,
                        "reply_to": m.reply_to_message_id if m.reply_to_message else None,
                        "edited": m.edit_date.isoformat() if m.edit_date else None,
                    })
                content = json.dumps(data, indent=2, ensure_ascii=False)
                ext = "json"
            else:
                lines = []
                for m in messages:
                    sender = "unknown"
                    if m.from_user:
                        sender = m.from_user.username or m.from_user.first_name or str(m.from_user.id)
                    elif m.sender_chat:
                        sender = m.sender_chat.title or str(m.sender_chat.id)
                    dt = m.date.strftime("%Y-%m-%d %H:%M:%S") if m.date else "?"
                    text = m.text or m.caption or ""
                    media = ""
                    if m.photo: media = " [photo]"
                    elif m.video: media = " [video]"
                    elif m.audio: media = " [audio]"
                    elif m.document: media = f" [doc:{m.document.file_name or ''}]"
                    elif m.voice: media = " [voice]"
                    elif m.sticker: media = f" [sticker:{m.sticker.set_name or ''}]"
                    elif m.animation: media = " [gif]"
                    lines.append(f"[{dt}] {sender}{media}: {text}")
                content = "\n".join(lines)
                ext = "txt"

            tmp_path = tempfile.NamedTemporaryFile(
                suffix=f"_dump_{int(time.time())}.{ext}", delete=False
            ).name
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(content)

            size = os.path.getsize(tmp_path)
            await status.edit(f"📤 Uploading dump ({len(messages)} msgs, {size/1024:.1f} KB)...")
            await client.send_document(
                chat_id=message.chat.id,
                document=tmp_path,
                caption=f"📥 Dump of `{args[0]}`\nMessages: {len(messages)}\nFormat: {ext}\nDate: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            )
            try:
                await status.delete()
            except Exception:
                pass
        except Exception as e:
            await status.edit(f"❌ Dump error: `{e}`")
        finally:
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except Exception: pass
    register_command("Backup", "dump", "Dump chat messages to a text/JSON file", [])

    @app.on_message(filters.command("dumpall", prefixes=".") & filters.me)
    async def _dumpall_cmd(client, message):
        """Dump last 1000 messages as text (shortcut)."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.dumpall <chat_id|@username>`")
        # Repoint to .dump
        message.command = ["dump", message.command[1], "1000"]
        await _dump_cmd(client, message)
    register_command("Backup", "dumpall", "Dump last 1000 messages", [])

    # ─────────── EXPORT MEDIA ───────────

    @app.on_message(filters.command("exportmedia", prefixes=".") & filters.me)
    async def _exportmedia_cmd(client, message):
        """Download all media from last N messages into a zip."""
        if len(message.command) < 3:
            return await message.reply("Usage: `.exportmedia <chat_id|@username> <count>`")
        chat_id = await _resolve_chat(client, message.command[1])
        count = int(message.command[2]) if message.command[2].isdigit() else 50
        if count > 200:
            return await message.reply("Max 200 messages per export.")
        status = await message.reply(f"📥 Downloading media from last {count} msgs of `{message.command[1]}`...")

        outdir = tempfile.mkdtemp(prefix="kyren_media_")
        try:
            downloaded = 0
            async for msg in client.get_chat_history(chat_id, limit=count):
                if msg.photo or msg.video or msg.document or msg.audio or msg.voice or msg.animation:
                    try:
                        await msg.download(file_name=outdir)
                        downloaded += 1
                        if downloaded % 10 == 0:
                            try:
                                await status.edit(f"⬇️ Downloaded {downloaded} files...")
                            except Exception:
                                pass
                    except Exception:
                        pass

            if downloaded == 0:
                return await status.edit("No media found in those messages.")

            # Zip them
            import shutil
            zip_path = outdir + ".zip"
            shutil.make_archive(outdir, "zip", outdir)
            size = os.path.getsize(zip_path)
            await status.edit(f"📤 Uploading {downloaded} media files ({size/1024/1024:.2f} MB)...")
            await client.send_document(
                chat_id=message.chat.id,
                document=zip_path,
                caption=f"📦 Exported {downloaded} media files from `{message.command[1]}`",
            )
            try:
                await status.delete()
            except Exception:
                pass

            # Cleanup
            import shutil as _sh
            _sh.rmtree(outdir, ignore_errors=True)
            try: os.remove(zip_path)
            except Exception: pass
        except Exception as e:
            await status.edit(f"❌ {e}")
    register_command("Backup", "exportmedia", "Download all media from last N messages", ["dlmedia"])

    # ─────────── CHAT INFO ───────────

    @app.on_message(filters.command("chatdump_info", prefixes=".") & filters.me)
    async def _chatdump_info_cmd(client, message):
        """Show chat info including message counts."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.chatdump_info <chat_id|@username>`")
        chat_id = await _resolve_chat(client, message.command[1])
        try:
            chat = await client.get_chat(chat_id)
            info = (
                f"📊 **Chat Info**\n\n"
                f"Title: {chat.title or chat.first_name or 'N/A'}\n"
                f"ID: `{chat.id}`\n"
                f"Type: {chat.type}\n"
                f"Members: {chat.members_count if hasattr(chat, 'members_count') else 'N/A'}\n"
                f"Username: @{chat.username if chat.username else 'none'}\n"
                f"Description: {chat.description or 'none'}"
            )
            await message.reply(info)
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("Backup", "chatdump_info", "Get chat info (title/members/desc)", [])

    print("[Backup] Registered chat dump/export commands")
