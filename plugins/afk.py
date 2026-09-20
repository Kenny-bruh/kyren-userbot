"""
KyrenUB - AFK (Away From Keyboard) Plugin
=========================================
Set yourself as AFK with an optional reason. Anyone who DMs you
gets an automatic reply with the reason and how long you've been AFK.
AFK state persists across bot restarts.

Commands:
  .afk [reason]              - go AFK (reason optional, defaults to "Busy")
  .afk off                   - manually turn off AFK
  .afk status                - check current AFK state
  .afk                       - toggle AFK on/off

Auto-replies ONLY fire in private chats (DMs) — never in groups,
even if someone @mentions you or replies to your message there.
This keeps your groups quiet while you're away.

Sending ANY message from your account automatically cancels AFK.
"""

def register(app):
    from pyrogram import filters
    from plugins import register_command
    import asyncio, os, json, time, datetime
    from pyrogram.types import ChatPrivileges

    AFK_FILE = "/tmp/kyren_afk_state.json"
    AFK_LOCK = asyncio.Lock()

    # Cooldown: don't reply to the same user in the same chat more than once
    # per COOLDOWN_SECONDS, to avoid spam.
    COOLDOWN_SECONDS = 30
    RECENT_REPLIES = {}  # key: f"{chat_id}:{user_id}" -> last reply timestamp

    def _load_state():
        if os.path.exists(AFK_FILE):
            try:
                with open(AFK_FILE) as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def _save_state(state):
        try:
            with open(AFK_FILE, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"[AFK] Failed to save state: {e}")

    def _clear_state():
        try:
            if os.path.exists(AFK_FILE):
                os.remove(AFK_FILE)
        except Exception:
            pass

    def _fmt_duration(seconds):
        """Human-friendly duration: '3h 12m 5s' or '45s'."""
        seconds = int(seconds)
        if seconds < 60:
            return f"{seconds}s"
        m, s = divmod(seconds, 60)
        if m < 60:
            return f"{m}m {s}s"
        h, m = divmod(m, 60)
        if h < 24:
            return f"{h}h {m}m"
        d, h = divmod(h, 24)
        return f"{d}d {h}h"

    def _build_afk_reply(state, mentioned_by=None):
        """Build the auto-reply message."""
        reason = state.get("reason", "Busy")
        ts = state.get("ts", time.time())
        elapsed = time.time() - ts
        dur = _fmt_duration(elapsed)
        start = state.get("start_str", "?")

        msg = f"💤 **AFK** — `_{reason}_`\n"
        msg += f"⏱️ Away for: `{dur}`\n"
        msg += f"📅 Since: `{start}`"
        if mentioned_by:
            # Don't actually tag the sender — just acknowledge
            msg += f"\n\n_(I'll reply when I'm back)_"
        return msg

    # ─────────── AFK COMMAND ───────────

    @app.on_message(filters.command("afk", prefixes=".") & filters.me)
    async def _afk_cmd(client, message):
        async with AFK_LOCK:
            current = _load_state()
            arg = message.command[1:] if len(message.command) > 1 else []
            sub = arg[0].lower() if arg else ""

            # .afk off  -> explicitly turn off
            if sub == "off":
                if not current:
                    return await message.reply("ℹ️ You're not AFK.")
                _clear_state()
                RECENT_REPLIES.clear()
                dur = _fmt_duration(time.time() - current["ts"])
                await message.reply(f"✅ **Welcome back!** AFK for `{dur}`.")
                return

            # .afk status  -> show current state
            if sub == "status":
                if not current:
                    return await message.reply("ℹ️ You're not AFK.")
                await message.reply(_build_afk_reply(current))
                return

            # .afk on  -> explicit on (same as default)
            if sub == "on":
                arg = arg[1:]

            # Toggle if no args and already AFK
            if not arg and current:
                _clear_state()
                RECENT_REPLIES.clear()
                dur = _fmt_duration(time.time() - current["ts"])
                await message.reply(f"✅ **Welcome back!** AFK for `{dur}`.")
                return

            # Set AFK
            reason = " ".join(arg).strip() if arg else "Busy"
            now = time.time()
            state = {
                "reason": reason,
                "ts": now,
                "start_str": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            _save_state(state)

            # Delete the trigger command to keep chat clean (optional)
            try:
                await message.delete()
            except Exception:
                pass

            # Send a brief confirmation that auto-deletes after 5s
            try:
                confirm = await message.reply(
                    f"💤 You're now AFK.\nReason: `{reason}`\n\n"
                    f"Auto-replies will be sent to anyone who mentions or replies to you. "
                    f"Send any message to cancel.",
                    quote=False,
                )
                await asyncio.sleep(5)
                try:
                    await confirm.delete()
                except Exception:
                    pass
            except Exception:
                pass
    register_command("AFK", "afk", "Set AFK with optional reason. .afk [reason|off|status]", [])

    # ─────────── AUTO-REPLY HANDLER (DMs ONLY) ───────────
    # Only reply to private chats. NEVER reply in groups, even if
    # someone mentions you or replies to your message. This keeps
    # your groups completely quiet while you're AFK.

    @app.on_message(filters.private & ~filters.me & ~filters.bot, group=1)
    async def _afk_pm_reply(client, message):
        state = _load_state()
        if not state:
            return
        if message.from_user and message.from_user.is_bot:
            return
        sender_id = message.from_user.id if message.from_user else 0
        key = f"pm:{sender_id}"
        now = time.time()
        last = RECENT_REPLIES.get(key, 0)
        if now - last < COOLDOWN_SECONDS * 3:  # longer cooldown in PMs
            return
        RECENT_REPLIES[key] = now
        try:
            await message.reply(_build_afk_reply(state, mentioned_by=True))
        except Exception as e:
            print(f"[AFK] PM auto-reply failed: {e}")

    # ─────────── AUTO-CANCEL ON MY MESSAGE ───────────
    # When I send ANY message (manually), AFK is automatically cancelled.

    @app.on_message(filters.me & ~filters.command("afk", prefixes="."), group=2)
    async def _afk_auto_cancel(client, message):
        state = _load_state()
        if not state:
            return
        async with AFK_LOCK:
            _clear_state()
            RECENT_REPLIES.clear()
            dur = _fmt_duration(time.time() - state["ts"])
        # Brief notification (auto-deletes after 4s)
        try:
            note = await message.reply(
                f"✅ **Welcome back!** You were AFK for `{dur}`.",
                quote=False,
            )
            await asyncio.sleep(4)
            try:
                await note.delete()
            except Exception:
                pass
        except Exception:
            pass

    print("[AFK] Registered AFK plugin (commands + auto-reply + auto-cancel)")
