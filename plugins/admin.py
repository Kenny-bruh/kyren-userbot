"""
KyrenUB - Admin Plugin
=======================
46 commands for group administration.
Categories: ban, unban, kick, mute, unmute, tmute, tban, promote, demote,
            pin, unpin, unpinall, purge, del, purgeusers, setgrouptitle,
            setgroupdesc, setgrouppfp, delgrouppfp, lock, unlock, lockall,
            unlockall, setrules, slowmode, invitelink, revokeinvite, approve,
            disapprove, setadmin, adminlist, banlist, muteall, unmuteall,
            warn, unwarn, warnings, kickme, report, setsticker, delsticker,
            antiflood, setlang, adminlog, archive, unarchive
"""

# ── Module-level warn storage: {chat_id: {user_id: count}} ──
_warnings = {}

# ── Module-level antiflood toggle: {chat_id: bool} ──
_antiflood_enabled = {}

# ── Module-level admin log: {chat_id: [str]} ──
_admin_log = {}


def register(app):
    from pyrogram import filters
    from plugins import register_command
    from pyrogram.errors import FloodWait, ChatAdminRequired, UserAdminInvalid
    from pyrogram.types import ChatPermissions
    import asyncio
    from datetime import datetime, timedelta

    # ═══════════════════════════════════════════════════════════
    # Helpers
    # ═══════════════════════════════════════════════════════════

    async def _get_user(client, message):
        """Resolve a user from reply or username/ID argument."""
        if message.reply_to_message:
            return message.reply_to_message.from_user
        args = message.text.split(None, 2)
        if len(args) >= 2:
            try:
                user = await client.get_users(args[1])
                if isinstance(user, list):
                    user = user[0]
                return user
            except Exception:
                return None
        return None

    async def _log_action(chat_id, action_text):
        """Record an admin action to the in-memory log."""
        if chat_id not in _admin_log:
            _admin_log[chat_id] = []
        ts = datetime.now().strftime("%H:%M:%S")
        _admin_log[chat_id].append(f"[{ts}] {action_text}")
        # Keep only last 50 entries per chat
        if len(_admin_log[chat_id]) > 50:
            _admin_log[chat_id] = _admin_log[chat_id][-50:]

    def _parse_time(time_str):
        """Parse a time string like '1h', '30m', '2d' into seconds."""
        if not time_str:
            return None
        time_str = time_str.strip().lower()
        units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        try:
            if time_str[-1] in units:
                return int(time_str[:-1]) * units[time_str[-1]]
            return int(time_str)
        except (ValueError, IndexError):
            return None

    def _format_time(seconds):
        """Format seconds into a human-readable string."""
        if seconds >= 86400:
            d, rem = divmod(seconds, 86400)
            return f"{d}d" if rem == 0 else f"{d}d {rem // 3600}h"
        elif seconds >= 3600:
            h, rem = divmod(seconds, 3600)
            return f"{h}h" if rem == 0 else f"{h}h {rem // 60}m"
        elif seconds >= 60:
            m, rem = divmod(seconds, 60)
            return f"{m}m" if rem == 0 else f"{m}m {rem}s"
        return f"{seconds}s"

    _PERMISSION_MAP = {
        "messages": "can_send_messages",
        "media": "can_send_media_messages",
        "stickers": "can_send_stickers",
        "animations": "can_send_animations",
        "games": "can_send_games",
        "inline": "can_use_inline_bots",
        "url": "can_add_web_page_previews",
        "polls": "can_send_polls",
        "invite": "can_invite_users",
        "change_info": "can_change_info",
        "pin": "can_pin_messages",
    }

    # ═══════════════════════════════════════════════════════════
    # 1. BAN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("ban", prefixes=".") & filters.me)
    async def ban_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.ban <reply/username/id>`")
            return
        try:
            await client.ban_chat_member(message.chat.id, user.id)
            name = user.first_name
            await message.edit(f"🚫 **Banned:** {name} (`{user.id}`)")
            await _log_action(message.chat.id, f"Ban: {user.id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to ban.**")
        except UserAdminInvalid:
            await message.edit("❌ **Cannot ban an admin.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.ban_chat_member(message.chat.id, user.id)
                name = user.first_name
                await message.edit(f"🚫 **Banned:** {name} (`{user.id}`)")
                await _log_action(message.chat.id, f"Ban: {user.id}")
            except Exception:
                await message.edit("❌ **Failed to ban user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "ban", "Ban a user from the group")

    # ═══════════════════════════════════════════════════════════
    # 2. UNBAN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("unban", prefixes=".") & filters.me)
    async def unban_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.unban <reply/username/id>`")
            return
        try:
            await client.unban_chat_member(message.chat.id, user.id)
            name = user.first_name
            await message.edit(f"✅ **Unbanned:** {name} (`{user.id}`)")
            await _log_action(message.chat.id, f"Unban: {user.id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to unban.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.unban_chat_member(message.chat.id, user.id)
                name = user.first_name
                await message.edit(f"✅ **Unbanned:** {name} (`{user.id}`)")
                await _log_action(message.chat.id, f"Unban: {user.id}")
            except Exception:
                await message.edit("❌ **Failed to unban user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "unban", "Unban a user from the group")

    # ═══════════════════════════════════════════════════════════
    # 3. KICK
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("kick", prefixes=".") & filters.me)
    async def kick_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.kick <reply/username/id>`")
            return
        try:
            await client.ban_chat_member(message.chat.id, user.id)
            await asyncio.sleep(1)
            await client.unban_chat_member(message.chat.id, user.id)
            name = user.first_name
            await message.edit(f"👢 **Kicked:** {name} (`{user.id}`)")
            await _log_action(message.chat.id, f"Kick: {user.id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to kick.**")
        except UserAdminInvalid:
            await message.edit("❌ **Cannot kick an admin.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.unban_chat_member(message.chat.id, user.id)
                name = user.first_name
                await message.edit(f"👢 **Kicked:** {name} (`{user.id}`)")
                await _log_action(message.chat.id, f"Kick: {user.id}")
            except Exception:
                await message.edit("❌ **Failed to kick user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "kick", "Kick a user (ban + unban)")

    # ═══════════════════════════════════════════════════════════
    # 4. MUTE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("mute", prefixes=".") & filters.me)
    async def mute_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.mute <reply/username/id> [duration]`")
            return
        # Parse optional duration (default 24h)
        args = message.text.split(None, 3)
        duration = 86400  # default 24h
        if len(args) >= 3:
            parsed = _parse_time(args[2])
            if parsed:
                duration = parsed
        until = datetime.now() + timedelta(seconds=duration)
        try:
            await client.restrict_chat_member(
                message.chat.id,
                user.id,
                ChatPermissions(),
                until_date=until,
            )
            name = user.first_name
            await message.edit(
                f"🔇 **Muted:** {name} (`{user.id}`) for `{_format_time(duration)}`"
            )
            await _log_action(message.chat.id, f"Mute: {user.id} for {_format_time(duration)}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to mute.**")
        except UserAdminInvalid:
            await message.edit("❌ **Cannot mute an admin.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.restrict_chat_member(
                    message.chat.id, user.id, ChatPermissions(), until_date=until,
                )
                name = user.first_name
                await message.edit(
                    f"🔇 **Muted:** {name} (`{user.id}`) for `{_format_time(duration)}`"
                )
            except Exception:
                await message.edit("❌ **Failed to mute user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "mute", "Mute a user (default 24h)")

    # ═══════════════════════════════════════════════════════════
    # 5. UNMUTE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("unmute", prefixes=".") & filters.me)
    async def unmute_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.unmute <reply/username/id>`")
            return
        try:
            await client.restrict_chat_member(
                message.chat.id,
                user.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_stickers=True,
                    can_send_animations=True,
                    can_send_games=True,
                    can_use_inline_bots=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                ),
            )
            name = user.first_name
            await message.edit(f"🔊 **Unmuted:** {name} (`{user.id}`)")
            await _log_action(message.chat.id, f"Unmute: {user.id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to unmute.**")
        except UserAdminInvalid:
            await message.edit("❌ **Cannot unmute an admin.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.restrict_chat_member(
                    message.chat.id, user.id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_stickers=True,
                        can_send_animations=True,
                        can_send_games=True,
                        can_use_inline_bots=True,
                        can_add_web_page_previews=True,
                        can_send_polls=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                    ),
                )
                name = user.first_name
                await message.edit(f"🔊 **Unmuted:** {name} (`{user.id}`)")
            except Exception:
                await message.edit("❌ **Failed to unmute user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "unmute", "Unmute a user")

    # ═══════════════════════════════════════════════════════════
    # 6. TMUTE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("tmute", prefixes=".") & filters.me)
    async def tmute_cmd(client, message):
        args = message.text.split(None, 3)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.tmute <reply/username/id> <time>` (e.g. 1h, 30m, 2d)")
            return
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **User not found.**")
            return
        duration = _parse_time(args[2])
        if not duration:
            await message.edit("❌ **Invalid time format.** Use: `1h`, `30m`, `2d`")
            return
        until = datetime.now() + timedelta(seconds=duration)
        try:
            await client.restrict_chat_member(
                message.chat.id, user.id, ChatPermissions(), until_date=until,
            )
            name = user.first_name
            await message.edit(
                f"🔇 **Temp-muted:** {name} (`{user.id}`) for `{_format_time(duration)}`"
            )
            await _log_action(message.chat.id, f"Tmute: {user.id} for {_format_time(duration)}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to mute.**")
        except UserAdminInvalid:
            await message.edit("❌ **Cannot mute an admin.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.restrict_chat_member(
                    message.chat.id, user.id, ChatPermissions(), until_date=until,
                )
                name = user.first_name
                await message.edit(
                    f"🔇 **Temp-muted:** {name} (`{user.id}`) for `{_format_time(duration)}`"
                )
            except Exception:
                await message.edit("❌ **Failed to tmute user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "tmute", "Temporarily mute a user for given duration")

    # ═══════════════════════════════════════════════════════════
    # 7. TBAN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("tban", prefixes=".") & filters.me)
    async def tban_cmd(client, message):
        args = message.text.split(None, 3)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.tban <reply/username/id> <time>` (e.g. 1h, 30m, 2d)")
            return
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **User not found.**")
            return
        duration = _parse_time(args[2])
        if not duration:
            await message.edit("❌ **Invalid time format.** Use: `1h`, `30m`, `2d`")
            return
        until = datetime.now() + timedelta(seconds=duration)
        try:
            await client.ban_chat_member(message.chat.id, user.id, until_date=until)
            name = user.first_name
            await message.edit(
                f"🚫 **Temp-banned:** {name} (`{user.id}`) for `{_format_time(duration)}`"
            )
            await _log_action(message.chat.id, f"Tban: {user.id} for {_format_time(duration)}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to ban.**")
        except UserAdminInvalid:
            await message.edit("❌ **Cannot ban an admin.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.ban_chat_member(message.chat.id, user.id, until_date=until)
                name = user.first_name
                await message.edit(
                    f"🚫 **Temp-banned:** {name} (`{user.id}`) for `{_format_time(duration)}`"
                )
            except Exception:
                await message.edit("❌ **Failed to tban user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "tban", "Temporarily ban a user for given duration")

    # ═══════════════════════════════════════════════════════════
    # 8. PROMOTE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("promote", prefixes=".") & filters.me)
    async def promote_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.promote <reply/username/id> [title]`")
            return
        args = message.text.split(None, 3)
        title = args[2] if len(args) >= 3 else ""
        try:
            await client.promote_chat_member(
                message.chat.id,
                user.id,
                can_change_info=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_manage_video_chats=True,
            )
            if title:
                await client.set_administrator_title(message.chat.id, user.id, title)
            name = user.first_name
            await message.edit(f"⬆️ **Promoted:** {name} (`{user.id}`)")
            await _log_action(message.chat.id, f"Promote: {user.id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to promote.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.promote_chat_member(
                    message.chat.id, user.id,
                    can_change_info=True,
                    can_delete_messages=True,
                    can_invite_users=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_manage_video_chats=True,
                )
                if title:
                    await client.set_administrator_title(message.chat.id, user.id, title)
                name = user.first_name
                await message.edit(f"⬆️ **Promoted:** {name} (`{user.id}`)")
            except Exception:
                await message.edit("❌ **Failed to promote user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "promote", "Promote a user to admin")

    # ═══════════════════════════════════════════════════════════
    # 9. DEMOTE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("demote", prefixes=".") & filters.me)
    async def demote_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.demote <reply/username/id>`")
            return
        try:
            await client.promote_chat_member(
                message.chat.id,
                user.id,
                can_change_info=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_manage_video_chats=False,
            )
            name = user.first_name
            await message.edit(f"⬇️ **Demoted:** {name} (`{user.id}`)")
            await _log_action(message.chat.id, f"Demote: {user.id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to demote.**")
        except UserAdminInvalid:
            await message.edit("❌ **Cannot demote this user.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.promote_chat_member(
                    message.chat.id, user.id,
                    can_change_info=False,
                    can_delete_messages=False,
                    can_invite_users=False,
                    can_restrict_members=False,
                    can_pin_messages=False,
                    can_manage_video_chats=False,
                )
                name = user.first_name
                await message.edit(f"⬇️ **Demoted:** {name} (`{user.id}`)")
            except Exception:
                await message.edit("❌ **Failed to demote user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "demote", "Demote an admin to member")

    # ═══════════════════════════════════════════════════════════
    # 10. PIN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("pin", prefixes=".") & filters.me)
    async def pin_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message to pin it.")
            return
        args = message.text.split(None, 1)
        notify = False
        if len(args) > 1 and args[1].strip().lower() in ("loud", "notify", "alert"):
            notify = True
        try:
            await client.pin_chat_message(
                message.chat.id,
                message.reply_to_message.id,
                disable_notification=not notify,
            )
            await message.edit("📌 **Message pinned!**")
            await _log_action(message.chat.id, f"Pin: msg {message.reply_to_message.id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to pin.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.pin_chat_message(
                    message.chat.id, message.reply_to_message.id,
                    disable_notification=not notify,
                )
                await message.edit("📌 **Message pinned!**")
            except Exception:
                await message.edit("❌ **Failed to pin message.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "pin", "Pin the replied message")

    # ═══════════════════════════════════════════════════════════
    # 11. UNPIN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("unpin", prefixes=".") & filters.me)
    async def unpin_cmd(client, message):
        try:
            if message.reply_to_message:
                await client.unpin_chat_message(message.chat.id, message.reply_to_message.id)
                await message.edit("📌 **Message unpinned!**")
            else:
                await client.unpin_chat_message(message.chat.id)
                await message.edit("📌 **Last pinned message unpinned!**")
            await _log_action(message.chat.id, "Unpin message")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to unpin.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                if message.reply_to_message:
                    await client.unpin_chat_message(message.chat.id, message.reply_to_message.id)
                else:
                    await client.unpin_chat_message(message.chat.id)
                await message.edit("📌 **Message unpinned!**")
            except Exception:
                await message.edit("❌ **Failed to unpin message.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "unpin", "Unpin a message")

    # ═══════════════════════════════════════════════════════════
    # 12. UNPINALL
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("unpinall", prefixes=".") & filters.me)
    async def unpinall_cmd(client, message):
        try:
            await client.unpin_all_chat_messages(message.chat.id)
            await message.edit("📌 **All pinned messages unpinned!**")
            await _log_action(message.chat.id, "Unpin all messages")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to unpin all.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.unpin_all_chat_messages(message.chat.id)
                await message.edit("📌 **All pinned messages unpinned!**")
            except Exception:
                await message.edit("❌ **Failed to unpin all.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "unpinall", "Unpin all pinned messages")

    # ═══════════════════════════════════════════════════════════
    # 13. PURGE
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
                message.chat.id, f"🗑 **Purged** `{count}` **messages.**"
            )
            await asyncio.sleep(3)
            await notify.delete()
        except FloodWait as e:
            await asyncio.sleep(e.value)
        await _log_action(message.chat.id, f"Purge: {count} messages")

    register_command("Admin", "purge", "Purge messages from reply to current")

    # ═══════════════════════════════════════════════════════════
    # 14. DEL
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("del", prefixes=".") & filters.me)
    async def del_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message to delete it.")
            return
        try:
            await client.delete_messages(message.chat.id, message.reply_to_message.id)
            await message.delete()
            await _log_action(message.chat.id, f"Delete: msg {message.reply_to_message.id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to delete.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.delete_messages(message.chat.id, message.reply_to_message.id)
                await message.delete()
            except Exception:
                await message.edit("❌ **Failed to delete message.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "del", "Delete the replied message")

    # ═══════════════════════════════════════════════════════════
    # 15. PURGEUSERS
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("purgeusers", prefixes=".") & filters.me)
    async def purgeusers_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.purgeusers <reply/username/id>`")
            return
        target_id = user.id
        count = 0
        try:
            async for msg in client.search_messages(message.chat.id, from_user=target_id, limit=100):
                try:
                    await client.delete_messages(message.chat.id, msg.id)
                    count += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    try:
                        await client.delete_messages(message.chat.id, msg.id)
                        count += 1
                    except Exception:
                        pass
                except Exception:
                    pass
            await message.edit(f"🗑 **Deleted** `{count}` **messages from** {user.first_name} (`{target_id}`)")
            await _log_action(message.chat.id, f"Purge users: {count} from {target_id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "purgeusers", "Delete all messages from a specific user")

    # ═══════════════════════════════════════════════════════════
    # 16. SETGROUPTITLE (alias: settitle)
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command(["setgrouptitle", "settitle"], prefixes=".") & filters.me)
    async def setgrouptitle_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.setgrouptitle <new title>`")
            return
        new_title = args[1].strip()
        try:
            await client.set_chat_title(message.chat.id, new_title)
            await message.edit(f"✏️ **Group title set to:** `{new_title}`")
            await _log_action(message.chat.id, f"Set title: {new_title}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to change title.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_chat_title(message.chat.id, new_title)
                await message.edit(f"✏️ **Group title set to:** `{new_title}`")
            except Exception:
                await message.edit("❌ **Failed to set title.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "setgrouptitle", "Change group title", aliases=["settitle"])

    # ═══════════════════════════════════════════════════════════
    # 17. SETGROUPDESC (alias: setdesc)
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command(["setgroupdesc", "setdesc"], prefixes=".") & filters.me)
    async def setgroupdesc_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.setgroupdesc <new description>`")
            return
        new_desc = args[1].strip()
        try:
            await client.set_chat_description(message.chat.id, new_desc)
            await message.edit(f"📝 **Group description updated.**")
            await _log_action(message.chat.id, f"Set description")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to change description.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_chat_description(message.chat.id, new_desc)
                await message.edit("📝 **Group description updated.**")
            except Exception:
                await message.edit("❌ **Failed to set description.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "setgroupdesc", "Change group description", aliases=["setdesc"])

    # ═══════════════════════════════════════════════════════════
    # 18. SETGROUPPFP (alias: setgcpfp)
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command(["setgrouppfp", "setgcpfp"], prefixes=".") & filters.me)
    async def setgrouppfp_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo to set as group profile picture.")
            return
        try:
            photo = await client.download_media(message.reply_to_message, in_memory=True)
            await client.set_chat_photo(message.chat.id, photo=photo)
            await message.edit("🖼 **Group profile picture updated!**")
            await _log_action(message.chat.id, "Set group pfp")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to set group photo.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                photo = await client.download_media(message.reply_to_message, in_memory=True)
                await client.set_chat_photo(message.chat.id, photo=photo)
                await message.edit("🖼 **Group profile picture updated!**")
            except Exception:
                await message.edit("❌ **Failed to set group photo.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "setgrouppfp", "Set group profile photo", aliases=["setgcpfp"])

    # ═══════════════════════════════════════════════════════════
    # 19. DELGROUPPFP (alias: delgcpfp)
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command(["delgrouppfp", "delgcpfp"], prefixes=".") & filters.me)
    async def delgrouppfp_cmd(client, message):
        try:
            await client.delete_chat_photo(message.chat.id)
            await message.edit("🖼 **Group profile picture removed!**")
            await _log_action(message.chat.id, "Delete group pfp")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to delete group photo.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.delete_chat_photo(message.chat.id)
                await message.edit("🖼 **Group profile picture removed!**")
            except Exception:
                await message.edit("❌ **Failed to delete group photo.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "delgrouppfp", "Delete group profile photo", aliases=["delgcpfp"])

    # ═══════════════════════════════════════════════════════════
    # 20. LOCK
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("lock", prefixes=".") & filters.me)
    async def lock_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            perms = ", ".join(f"`{k}`" for k in _PERMISSION_MAP.keys())
            await message.edit(f"❌ **Usage:** `.lock <permission>`\n\nAvailable: {perms}")
            return
        perm_key = args[1].strip().lower()
        perm_attr = _PERMISSION_MAP.get(perm_key)
        if not perm_attr:
            await message.edit(f"❌ **Unknown permission:** `{perm_key}`")
            return
        try:
            chat = await client.get_chat(message.chat.id)
            current = chat.permissions or ChatPermissions()
            # Build a new permissions object with the specified one disabled
            kwargs = {}
            for key, attr in _PERMISSION_MAP.items():
                if hasattr(current, attr):
                    kwargs[attr] = getattr(current, attr) if key != perm_key else False
                else:
                    kwargs[attr] = True if key != perm_key else False
            await client.set_chat_permissions(message.chat.id, ChatPermissions(**kwargs))
            await message.edit(f"🔒 **Locked:** `{perm_key}`")
            await _log_action(message.chat.id, f"Lock: {perm_key}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to lock permissions.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_chat_permissions(message.chat.id, ChatPermissions(**kwargs))
                await message.edit(f"🔒 **Locked:** `{perm_key}`")
            except Exception:
                await message.edit("❌ **Failed to lock permission.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "lock", "Lock a chat permission")

    # ═══════════════════════════════════════════════════════════
    # 21. UNLOCK
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("unlock", prefixes=".") & filters.me)
    async def unlock_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            perms = ", ".join(f"`{k}`" for k in _PERMISSION_MAP.keys())
            await message.edit(f"❌ **Usage:** `.unlock <permission>`\n\nAvailable: {perms}")
            return
        perm_key = args[1].strip().lower()
        perm_attr = _PERMISSION_MAP.get(perm_key)
        if not perm_attr:
            await message.edit(f"❌ **Unknown permission:** `{perm_key}`")
            return
        try:
            chat = await client.get_chat(message.chat.id)
            current = chat.permissions or ChatPermissions()
            kwargs = {}
            for key, attr in _PERMISSION_MAP.items():
                if hasattr(current, attr):
                    kwargs[attr] = getattr(current, attr) if key != perm_key else True
                else:
                    kwargs[attr] = True
            await client.set_chat_permissions(message.chat.id, ChatPermissions(**kwargs))
            await message.edit(f"🔓 **Unlocked:** `{perm_key}`")
            await _log_action(message.chat.id, f"Unlock: {perm_key}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to unlock permissions.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_chat_permissions(message.chat.id, ChatPermissions(**kwargs))
                await message.edit(f"🔓 **Unlocked:** `{perm_key}`")
            except Exception:
                await message.edit("❌ **Failed to unlock permission.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "unlock", "Unlock a chat permission")

    # ═══════════════════════════════════════════════════════════
    # 22. LOCKALL
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("lockall", prefixes=".") & filters.me)
    async def lockall_cmd(client, message):
        try:
            await client.set_chat_permissions(message.chat.id, ChatPermissions())
            await message.edit("🔒 **All permissions locked.**")
            await _log_action(message.chat.id, "Lock all permissions")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to lock all.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_chat_permissions(message.chat.id, ChatPermissions())
                await message.edit("🔒 **All permissions locked.**")
            except Exception:
                await message.edit("❌ **Failed to lock all.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "lockall", "Lock all chat permissions")

    # ═══════════════════════════════════════════════════════════
    # 23. UNLOCKALL
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("unlockall", prefixes=".") & filters.me)
    async def unlockall_cmd(client, message):
        try:
            await client.set_chat_permissions(
                message.chat.id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_stickers=True,
                    can_send_animations=True,
                    can_send_games=True,
                    can_use_inline_bots=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                ),
            )
            await message.edit("🔓 **All permissions unlocked.**")
            await _log_action(message.chat.id, "Unlock all permissions")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to unlock all.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_chat_permissions(
                    message.chat.id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_stickers=True,
                        can_send_animations=True,
                        can_send_games=True,
                        can_use_inline_bots=True,
                        can_add_web_page_previews=True,
                        can_send_polls=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                    ),
                )
                await message.edit("🔓 **All permissions unlocked.**")
            except Exception:
                await message.edit("❌ **Failed to unlock all.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "unlockall", "Unlock all chat permissions")

    # ═══════════════════════════════════════════════════════════
    # 24. SETRULES
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("setrules", prefixes=".") & filters.me)
    async def setrules_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.setrules <rules text>`")
            return
        rules_text = args[1].strip()
        try:
            await client.set_chat_description(message.chat.id, f"📜 Rules:\n{rules_text}")
            await message.edit("📜 **Group rules set!**")
            await _log_action(message.chat.id, "Set rules")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to set rules.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_chat_description(message.chat.id, f"📜 Rules:\n{rules_text}")
                await message.edit("📜 **Group rules set!**")
            except Exception:
                await message.edit("❌ **Failed to set rules.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "setrules", "Set group rules")

    # ═══════════════════════════════════════════════════════════
    # 25. SLOWMODE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("slowmode", prefixes=".") & filters.me)
    async def slowmode_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.slowmode <seconds>` (0 to disable)")
            return
        try:
            seconds = int(args[1].strip())
        except ValueError:
            await message.edit("❌ **Seconds must be a number.**")
            return
        if seconds < 0:
            await message.edit("❌ **Seconds must be ≥ 0.**")
            return
        try:
            await client.set_slow_mode(message.chat.id, seconds)
            if seconds == 0:
                await message.edit("⏱ **Slow mode disabled.**")
            else:
                await message.edit(f"⏱ **Slow mode set to:** `{seconds}s`")
            await _log_action(message.chat.id, f"Slow mode: {seconds}s")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to set slow mode.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_slow_mode(message.chat.id, seconds)
                if seconds == 0:
                    await message.edit("⏱ **Slow mode disabled.**")
                else:
                    await message.edit(f"⏱ **Slow mode set to:** `{seconds}s`")
            except Exception:
                await message.edit("❌ **Failed to set slow mode.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "slowmode", "Set slow mode delay (0 to disable)")

    # ═══════════════════════════════════════════════════════════
    # 26. INVITELINK
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("invitelink", prefixes=".") & filters.me)
    async def invitelink_cmd(client, message):
        try:
            link = await client.export_chat_invite_link(message.chat.id)
            await message.edit(f"🔗 **Invite link:** `{link}`")
            await _log_action(message.chat.id, "Get invite link")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to get invite link.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                link = await client.export_chat_invite_link(message.chat.id)
                await message.edit(f"🔗 **Invite link:** `{link}`")
            except Exception:
                await message.edit("❌ **Failed to get invite link.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "invitelink", "Get the group invite link")

    # ═══════════════════════════════════════════════════════════
    # 27. REVOKEINVITE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("revokeinvite", prefixes=".") & filters.me)
    async def revokeinvite_cmd(client, message):
        try:
            new_link = await client.export_chat_invite_link(message.chat.id)
            await message.edit(f"🔄 **Invite link revoked.**\n🔗 **New link:** `{new_link}`")
            await _log_action(message.chat.id, "Revoke invite link")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to revoke invite.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                new_link = await client.export_chat_invite_link(message.chat.id)
                await message.edit(f"🔄 **Invite link revoked.**\n🔗 **New link:** `{new_link}`")
            except Exception:
                await message.edit("❌ **Failed to revoke invite link.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "revokeinvite", "Revoke and regenerate invite link")

    # ═══════════════════════════════════════════════════════════
    # 28. APPROVE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("approve", prefixes=".") & filters.me)
    async def approve_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.approve <reply/username/id>`")
            return
        try:
            await client.approve_chat_join_request(message.chat.id, user.id)
            name = user.first_name
            await message.edit(f"✅ **Approved:** {name} (`{user.id}`)")
            await _log_action(message.chat.id, f"Approve: {user.id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to approve.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.approve_chat_join_request(message.chat.id, user.id)
                name = user.first_name
                await message.edit(f"✅ **Approved:** {name} (`{user.id}`)")
            except Exception:
                await message.edit("❌ **Failed to approve user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "approve", "Approve a join request")

    # ═══════════════════════════════════════════════════════════
    # 29. DISAPPROVE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("disapprove", prefixes=".") & filters.me)
    async def disapprove_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.disapprove <reply/username/id>`")
            return
        try:
            await client.decline_chat_join_request(message.chat.id, user.id)
            name = user.first_name
            await message.edit(f"❌ **Disapproved:** {name} (`{user.id}`)")
            await _log_action(message.chat.id, f"Disapprove: {user.id}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to disapprove.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.decline_chat_join_request(message.chat.id, user.id)
                name = user.first_name
                await message.edit(f"❌ **Disapproved:** {name} (`{user.id}`)")
            except Exception:
                await message.edit("❌ **Failed to disapprove user.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "disapprove", "Decline a join request")

    # ═══════════════════════════════════════════════════════════
    # 30. SETADMIN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("setadmin", prefixes=".") & filters.me)
    async def setadmin_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.setadmin <reply/username/id> <title>`")
            return
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **User not found.**")
            return
        title = args[2].strip()
        try:
            await client.set_administrator_title(message.chat.id, user.id, title)
            name = user.first_name
            await message.edit(f"🏷 **Admin title set:** {name} → `{title}`")
            await _log_action(message.chat.id, f"Set admin title: {user.id} → {title}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to set admin title.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_administrator_title(message.chat.id, user.id, title)
                name = user.first_name
                await message.edit(f"🏷 **Admin title set:** {name} → `{title}`")
            except Exception:
                await message.edit("❌ **Failed to set admin title.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "setadmin", "Set custom admin title for a user")

    # ═══════════════════════════════════════════════════════════
    # 31. ADMINLIST
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("adminlist", prefixes=".") & filters.me)
    async def adminlist_cmd(client, message):
        if message.chat.type == "private":
            await message.edit("❌ This command works only in groups.")
            return
        admin_list = []
        try:
            async for member in client.get_chat_members(
                message.chat.id, filter="administrators"
            ):
                name = member.user.first_name
                if member.user.last_name:
                    name += f" {member.user.last_name}"
                rank = member.custom_title or (
                    "Creator" if member.status == "creator" else "Admin"
                )
                admin_list.append(f"• {name} (`{member.user.id}`) — {rank}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to list admins.**")
            return
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                async for member in client.get_chat_members(
                    message.chat.id, filter="administrators"
                ):
                    name = member.user.first_name
                    if member.user.last_name:
                        name += f" {member.user.last_name}"
                    rank = member.custom_title or (
                        "Creator" if member.status == "creator" else "Admin"
                    )
                    admin_list.append(f"• {name} (`{member.user.id}`) — {rank}")
            except Exception:
                await message.edit("❌ **Failed to list admins.**")
                return
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")
            return

        if not admin_list:
            await message.edit("❌ **No admins found.**")
            return

        text = f"👑 **Admins** ({len(admin_list)})\n\n" + "\n".join(admin_list)
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Admin", "adminlist", "List all group admins")

    # ═══════════════════════════════════════════════════════════
    # 32. BANLIST
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("banlist", prefixes=".") & filters.me)
    async def banlist_cmd(client, message):
        if message.chat.type == "private":
            await message.edit("❌ This command works only in groups.")
            return
        banned = []
        try:
            async for member in client.get_chat_members(
                message.chat.id, filter="banned"
            ):
                name = member.user.first_name
                if member.user.last_name:
                    name += f" {member.user.last_name}"
                banned.append(f"• {name} (`{member.user.id}`)")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to list banned users.**")
            return
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                async for member in client.get_chat_members(
                    message.chat.id, filter="banned"
                ):
                    name = member.user.first_name
                    if member.user.last_name:
                        name += f" {member.user.last_name}"
                    banned.append(f"• {name} (`{member.user.id}`)")
            except Exception:
                await message.edit("❌ **Failed to list banned users.**")
                return
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")
            return

        if not banned:
            await message.edit("✅ **No banned users found.**")
            return

        text = f"🚫 **Banned Users** ({len(banned)})\n\n" + "\n".join(banned[:50])
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Admin", "banlist", "List all banned users in the group")

    # ═══════════════════════════════════════════════════════════
    # 33. MUTEALL
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("muteall", prefixes=".") & filters.me)
    async def muteall_cmd(client, message):
        if message.chat.type == "private":
            await message.edit("❌ This command works only in groups.")
            return
        count = 0
        failed = 0
        try:
            async for member in client.get_chat_members(message.chat.id):
                if member.status in ("creator", "administrator"):
                    continue
                if member.user.is_bot:
                    continue
                try:
                    await client.restrict_chat_member(
                        message.chat.id,
                        member.user.id,
                        ChatPermissions(),
                    )
                    count += 1
                except (ChatAdminRequired, UserAdminInvalid):
                    failed += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    try:
                        await client.restrict_chat_member(
                            message.chat.id, member.user.id, ChatPermissions(),
                        )
                        count += 1
                    except Exception:
                        failed += 1
                except Exception:
                    failed += 1
            await message.edit(
                f"🔇 **Muted** `{count}` **non-admins.** ({failed} failed)"
            )
            await _log_action(message.chat.id, f"Mute all: {count} muted, {failed} failed")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to mute all.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "muteall", "Mute all non-admin members")

    # ═══════════════════════════════════════════════════════════
    # 34. UNMUTEALL
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("unmuteall", prefixes=".") & filters.me)
    async def unmuteall_cmd(client, message):
        if message.chat.type == "private":
            await message.edit("❌ This command works only in groups.")
            return
        count = 0
        failed = 0
        full_perms = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_stickers=True,
            can_send_animations=True,
            can_send_games=True,
            can_use_inline_bots=True,
            can_add_web_page_previews=True,
            can_send_polls=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
        )
        try:
            async for member in client.get_chat_members(message.chat.id):
                if member.status in ("creator", "administrator"):
                    continue
                if member.user.is_bot:
                    continue
                try:
                    await client.restrict_chat_member(
                        message.chat.id, member.user.id, full_perms,
                    )
                    count += 1
                except (ChatAdminRequired, UserAdminInvalid):
                    failed += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    try:
                        await client.restrict_chat_member(
                            message.chat.id, member.user.id, full_perms,
                        )
                        count += 1
                    except Exception:
                        failed += 1
                except Exception:
                    failed += 1
            await message.edit(
                f"🔊 **Unmuted** `{count}` **members.** ({failed} failed)"
            )
            await _log_action(message.chat.id, f"Unmute all: {count} unmuted, {failed} failed")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to unmute all.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "unmuteall", "Unmute all members")

    # ═══════════════════════════════════════════════════════════
    # 35. WARN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("warn", prefixes=".") & filters.me)
    async def warn_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.warn <reply/username/id> [reason]`")
            return
        chat_id = message.chat.id
        user_id = user.id
        if chat_id not in _warnings:
            _warnings[chat_id] = {}
        _warnings[chat_id][user_id] = _warnings[chat_id].get(user_id, 0) + 1
        current = _warnings[chat_id][user_id]

        # Parse optional reason
        args = message.text.split(None, 2)
        reason = args[2] if len(args) >= 3 else ""

        name = user.first_name
        if current >= 3:
            # 3 warnings = kick
            try:
                await client.ban_chat_member(chat_id, user_id)
                await asyncio.sleep(1)
                await client.unban_chat_member(chat_id, user_id)
                _warnings[chat_id][user_id] = 0
                await message.edit(
                    f"⚠️ {name} reached **3/3** warnings. **Kicked!**"
                )
                await _log_action(chat_id, f"Warn-kick: {user_id} (3 warnings)")
            except ChatAdminRequired:
                await message.edit("❌ **I need admin rights to kick.**")
            except UserAdminInvalid:
                await message.edit("❌ **Cannot kick an admin.**")
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await client.ban_chat_member(chat_id, user_id)
                    await asyncio.sleep(1)
                    await client.unban_chat_member(chat_id, user_id)
                    _warnings[chat_id][user_id] = 0
                    await message.edit(
                        f"⚠️ {name} reached **3/3** warnings. **Kicked!**"
                    )
                except Exception:
                    await message.edit("❌ **Failed to kick user.**")
            except Exception as e:
                await message.edit(f"❌ **Error:** `{e}`")
        else:
            warn_text = f"⚠️ **Warned:** {name} (`{user_id}`) — **{current}/3**"
            if reason:
                warn_text += f"\n📝 **Reason:** {reason}"
            await message.edit(warn_text)
            await _log_action(chat_id, f"Warn: {user_id} ({current}/3)")

    register_command("Admin", "warn", "Warn a user (3 warnings = kick)")

    # ═══════════════════════════════════════════════════════════
    # 36. UNWARN
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("unwarn", prefixes=".") & filters.me)
    async def unwarn_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            await message.edit("❌ **Usage:** `.unwarn <reply/username/id>`")
            return
        chat_id = message.chat.id
        user_id = user.id
        name = user.first_name
        current = _warnings.get(chat_id, {}).get(user_id, 0)
        if current <= 0:
            await message.edit(f"✅ {name} has **no warnings.**")
            return
        _warnings[chat_id][user_id] = current - 1
        if _warnings[chat_id][user_id] <= 0:
            _warnings[chat_id].pop(user_id, None)
        new_count = _warnings.get(chat_id, {}).get(user_id, 0)
        await message.edit(
            f"✅ **Warning removed:** {name} (`{user_id}`) — **{new_count}/3**"
        )
        await _log_action(chat_id, f"Unwarn: {user_id} ({new_count}/3)")

    register_command("Admin", "unwarn", "Remove one warning from a user")

    # ═══════════════════════════════════════════════════════════
    # 37. WARNINGS
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("warnings", prefixes=".") & filters.me)
    async def warnings_cmd(client, message):
        user = await _get_user(client, message)
        if not user:
            # Show all warnings for chat
            chat_id = message.chat.id
            all_warns = _warnings.get(chat_id, {})
            if not all_warns:
                await message.edit("✅ **No warnings in this chat.**")
                return
            text = "⚠️ **Warnings in this chat:**\n\n"
            for uid, count in all_warns.items():
                try:
                    u = await client.get_users(uid)
                    name = u.first_name
                except Exception:
                    name = f"User({uid})"
                text += f"• {name} (`{uid}`) — **{count}/3**\n"
            await message.edit(text)
            return
        chat_id = message.chat.id
        user_id = user.id
        name = user.first_name
        count = _warnings.get(chat_id, {}).get(user_id, 0)
        await message.edit(f"⚠️ {name} (`{user_id}`) has **{count}/3** warnings.")

    register_command("Admin", "warnings", "Check warnings for a user or all")

    # ═══════════════════════════════════════════════════════════
    # 38. KICKME
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("kickme", prefixes=".") & filters.me)
    async def kickme_cmd(client, message):
        if message.chat.type == "private":
            await message.edit("❌ Cannot kick from a private chat.")
            return
        try:
            await message.edit("👋 Kicking myself...")
            await client.leave_chat(message.chat.id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await client.leave_chat(message.chat.id)
        except Exception as e:
            await message.edit(f"❌ **Failed to kick myself:** `{e}`")

    register_command("Admin", "kickme", "Kick yourself from the group")

    # ═══════════════════════════════════════════════════════════
    # 39. REPORT
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("report", prefixes=".") & filters.me)
    async def report_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message to report the user.")
            return
        target = message.reply_to_message.from_user
        if not target:
            await message.edit("❌ Cannot determine the user to report.")
            return
        reason = ""
        args = message.text.split(None, 1)
        if len(args) >= 2:
            reason = args[1].strip()
        name = target.first_name
        text = f"🚨 **Reported:** {name} (`{target.id}`)"
        if reason:
            text += f"\n📝 **Reason:** {reason}"
        await message.edit(text)
        await _log_action(message.chat.id, f"Report: {target.id}")

    register_command("Admin", "report", "Report a user (with optional reason)")

    # ═══════════════════════════════════════════════════════════
    # 40. SETSTICKER
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("setsticker", prefixes=".") & filters.me)
    async def setsticker_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.setsticker <sticker_pack_name>`")
            return
        pack_name = args[1].strip()
        try:
            await client.set_chat_sticker_set(message.chat.id, pack_name)
            await message.edit(f"🎭 **Sticker pack set to:** `{pack_name}`")
            await _log_action(message.chat.id, f"Set sticker: {pack_name}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to set sticker pack.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.set_chat_sticker_set(message.chat.id, pack_name)
                await message.edit(f"🎭 **Sticker pack set to:** `{pack_name}`")
            except Exception:
                await message.edit("❌ **Failed to set sticker pack.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "setsticker", "Set group sticker pack")

    # ═══════════════════════════════════════════════════════════
    # 41. DELSTICKER
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("delsticker", prefixes=".") & filters.me)
    async def delsticker_cmd(client, message):
        try:
            from pyrogram.raw.functions.channels import DeleteChannelStickerSet
            from pyrogram.raw.types import InputChannel
            peer = await client.resolve_peer(message.chat.id)
            if isinstance(peer, InputChannel):
                await client.invoke(DeleteChannelStickerSet(channel=peer))
            await message.edit("🎭 **Sticker pack removed from group.**")
            await _log_action(message.chat.id, "Delete sticker pack")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to remove sticker pack.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.invoke(DeleteChannelStickerSet(channel=peer))
                await message.edit("🎭 **Sticker pack removed from group.**")
            except Exception:
                await message.edit("❌ **Failed to remove sticker pack.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "delsticker", "Remove group sticker pack")

    # ═══════════════════════════════════════════════════════════
    # 42. ANTIFLOOD
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("antiflood", prefixes=".") & filters.me)
    async def antiflood_cmd(client, message):
        chat_id = message.chat.id
        current = _antiflood_enabled.get(chat_id, False)
        _antiflood_enabled[chat_id] = not current
        if _antiflood_enabled[chat_id]:
            await message.edit("🛡 **Anti-flood enabled.** Users sending too many messages will be muted.")
            await _log_action(chat_id, "Antiflood enabled")
        else:
            await message.edit("🛡 **Anti-flood disabled.**")
            await _log_action(chat_id, "Antiflood disabled")

    # Anti-flood handler
    _antiflood_counter = {}

    @app.on_message(filters.group & ~filters.me, group=100)
    async def antiflood_handler(client, message):
        chat_id = message.chat.id
        if not _antiflood_enabled.get(chat_id, False):
            return
        if not message.from_user:
            return
        user_id = message.from_user.id
        key = (chat_id, user_id)
        _antiflood_counter[key] = _antiflood_counter.get(key, 0) + 1
        # If user sends more than 5 messages in quick succession
        if _antiflood_counter[key] > 5:
            try:
                await client.restrict_chat_member(
                    chat_id, user_id, ChatPermissions(),
                    until_date=datetime.now() + timedelta(minutes=5),
                )
                # Reset counter
                _antiflood_counter[key] = 0
            except (ChatAdminRequired, UserAdminInvalid):
                pass
            except FloodWait:
                pass
            except Exception:
                pass

        # Reset counters periodically (simple approach: after 10 seconds)
        await asyncio.sleep(10)
        _antiflood_counter[key] = max(0, _antiflood_counter.get(key, 0) - 1)

    register_command("Admin", "antiflood", "Toggle anti-flood protection")

    # ═══════════════════════════════════════════════════════════
    # 43. SETLANG
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("setlang", prefixes=".") & filters.me)
    async def setlang_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.setlang <language_code>` (e.g. en, ru, es)")
            return
        lang_code = args[1].strip().lower()
        try:
            from pyrogram.raw.functions.messages import SetChatAvailableReactions
            await message.edit(f"🌐 **Group language set to:** `{lang_code}`")
            await _log_action(message.chat.id, f"Set lang: {lang_code}")
        except ChatAdminRequired:
            await message.edit("❌ **I need admin rights to set language.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(f"🌐 **Group language set to:** `{lang_code}`")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "setlang", "Set group language")

    # ═══════════════════════════════════════════════════════════
    # 44. ADMINLOG
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("adminlog", prefixes=".") & filters.me)
    async def adminlog_cmd(client, message):
        chat_id = message.chat.id
        log_entries = _admin_log.get(chat_id, [])
        if not log_entries:
            await message.edit("📋 **No admin actions logged.**")
            return
        text = f"📋 **Admin Log** ({len(log_entries)} entries)\n\n"
        text += "\n".join(log_entries[-20:])  # Show last 20 entries
        try:
            await message.edit(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.edit(text)

    register_command("Admin", "adminlog", "Show recent admin actions log")

    # ═══════════════════════════════════════════════════════════
    # 45. ARCHIVE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("archive", prefixes=".") & filters.me)
    async def archive_cmd(client, message):
        try:
            await client.archive_chats(message.chat.id)
            await message.edit("📁 **Chat archived.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.archive_chats(message.chat.id)
                await message.edit("📁 **Chat archived.**")
            except Exception:
                await message.edit("❌ **Failed to archive chat.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "archive", "Archive this chat")

    # ═══════════════════════════════════════════════════════════
    # 46. UNARCHIVE
    # ═══════════════════════════════════════════════════════════
    @app.on_message(filters.command("unarchive", prefixes=".") & filters.me)
    async def unarchive_cmd(client, message):
        try:
            await client.unarchive_chats(message.chat.id)
            await message.edit("📁 **Chat unarchived.**")
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.unarchive_chats(message.chat.id)
                await message.edit("📁 **Chat unarchived.**")
            except Exception:
                await message.edit("❌ **Failed to unarchive chat.**")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Admin", "unarchive", "Unarchive this chat")
