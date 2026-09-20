"""
KyrenUB - Persistent Notes & Snippets Plugin
=============================================
Save/load text snippets, notes, todos, and clipboard items that persist
across bot restarts. Stored as JSON in /tmp/kyren_notes_store.json
(on Render this survives within a single dyno session).

Commands:
  .note save <name> (reply)     - save replied text as a named note
  .note get <name>              - retrieve a note
  .note list                    - list all notes
  .note del <name>              - delete a note
  .note search <query>          - search note names

  .snip <name>                  - same as .note get (quick alias)
  .clip <text>                  - save to clipboard (last 10 items)
  .clip                         - show last clipboard item
  .clips                        - list all clipboard items

  .todo <text>                  - add todo item
  .todos                        - list todos
  .todo done <id>               - mark todo done
  .todo del <id>                - delete todo
"""

def register(app):
    from pyrogram import filters
    from plugins import register_command
    import os, json, time

    STORE_FILE = "/tmp/kyren_notes_store.json"

    def _load():
        if os.path.exists(STORE_FILE):
            try:
                with open(STORE_FILE) as f:
                    return json.load(f)
            except Exception:
                pass
        return {"notes": {}, "clipboard": [], "todos": []}

    def _save(data):
        with open(STORE_FILE, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ─────────── NOTES ───────────

    @app.on_message(filters.command("note", prefixes=".") & filters.me)
    async def _note_cmd(client, message):
        store = _load()
        if len(message.command) < 2:
            return await message.reply(
                "📝 **Notes commands:**\n"
                "`.note save <name>` (reply to msg)\n"
                "`.note get <name>`\n"
                "`.note list`\n"
                "`.note del <name>`\n"
                "`.note search <query>`"
            )
        action = message.command[1]
        if action == "save":
            if len(message.command) < 3 or not message.reply_to_message:
                return await message.reply("Reply to a message with `.note save <name>`")
            name = message.command[2]
            content = message.reply_to_message.text or message.reply_to_message.caption or "(no text)"
            store["notes"][name] = {
                "content": content,
                "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
                "chat": message.chat.id,
            }
            _save(store)
            await message.reply(f"✅ Note `{name}` saved ({len(content)} chars)")
        elif action == "get":
            if len(message.command) < 3:
                return await message.reply("Usage: `.note get <name>`")
            name = message.command[2]
            if name not in store["notes"]:
                return await message.reply(f"❌ Note `{name}` not found")
            n = store["notes"][name]
            await message.reply(f"📝 **{name}**\n_(saved {n['ts']})_\n\n{n['content'][:3500]}")
        elif action == "list":
            if not store["notes"]:
                return await message.reply("No notes saved yet.")
            lines = [f"• `{n}` - {len(d['content'])} chars ({d['ts']})" for n, d in store["notes"].items()]
            await message.reply("📝 **Notes:**\n" + "\n".join(lines))
        elif action == "del":
            if len(message.command) < 3:
                return await message.reply("Usage: `.note del <name>`")
            name = message.command[2]
            if name in store["notes"]:
                del store["notes"][name]
                _save(store)
                await message.reply(f"🗑️ Deleted note `{name}`")
            else:
                await message.reply("Not found")
        elif action == "search":
            if len(message.command) < 3:
                return await message.reply("Usage: `.note search <query>`")
            q = message.command[2].lower()
            matches = [n for n in store["notes"] if q in n.lower()]
            if not matches:
                return await message.reply("No matches.")
            await message.reply("🔍 Matches:\n" + "\n".join(f"• `{n}`" for n in matches))
        else:
            await message.reply("Unknown action. Try `.note` for help.")
    register_command("Notes", "note", "Persistent notes (save/get/list/del/search)", ["notes"])

    # ─────────── QUICK SNIPPET ───────────

    @app.on_message(filters.command("snip", prefixes=".") & filters.me)
    async def _snip_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.snip <name>` (retrieves a saved note)")
        store = _load()
        name = message.command[1]
        if name not in store["notes"]:
            return await message.reply(f"❌ Note `{name}` not found")
        n = store["notes"][name]
        await message.reply(n["content"][:3500])
    register_command("Notes", "snip", "Quick-retrieve a saved note", [])

    # ─────────── CLIPBOARD ───────────

    @app.on_message(filters.command("clip", prefixes=".") & filters.me)
    async def _clip_cmd(client, message):
        store = _load()
        if len(message.command) == 1:
            # Show last clipboard item
            if not store["clipboard"]:
                return await message.reply("Clipboard empty. Use `.clip <text>` to add.")
            last = store["clipboard"][0]
            await message.reply(f"📋 Last clip ({last['ts']}):\n\n{last['text'][:3500]}")
        else:
            text = " ".join(message.command[1:])
            store["clipboard"].insert(0, {
                "text": text,
                "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
            })
            store["clipboard"] = store["clipboard"][:10]  # keep last 10
            _save(store)
            await message.reply(f"📋 Clipped ({len(text)} chars)")
    register_command("Notes", "clip", "Save/show clipboard items", ["copy"])

    @app.on_message(filters.command("clips", prefixes=".") & filters.me)
    async def _clips_cmd(client, message):
        store = _load()
        if not store["clipboard"]:
            return await message.reply("Clipboard empty.")
        lines = [f"{i+1}. _{c['ts']}_ - {c['text'][:80]}..." for i, c in enumerate(store["clipboard"])]
        await message.reply("📋 **Clipboard history:**\n" + "\n".join(lines))
    register_command("Notes", "clips", "List clipboard history", [])

    # ─────────── TODOS ───────────

    @app.on_message(filters.command("todo", prefixes=".") & filters.me)
    async def _todo_cmd(client, message):
        store = _load()
        if "todos" not in store:
            store["todos"] = []
        if len(message.command) < 2:
            # add a todo from message text
            return await message.reply(
                "✅ **Todo commands:**\n"
                "`.todo <text>` - add item\n"
                "`.todos` - list items\n"
                "`.todo done <id>` - mark done\n"
                "`.todo del <id>` - delete item\n"
                "`.todo clear` - clear all"
            )
        action = message.command[1]
        if action == "done":
            if len(message.command) < 3 or not message.command[2].isdigit():
                return await message.reply("Usage: `.todo done <id>`")
            idx = int(message.command[2]) - 1
            if 0 <= idx < len(store["todos"]):
                store["todos"][idx]["done"] = True
                _save(store)
                await message.reply(f"✅ Marked #{idx+1} done")
            else:
                await message.reply("Invalid id")
        elif action == "del":
            if len(message.command) < 3 or not message.command[2].isdigit():
                return await message.reply("Usage: `.todo del <id>`")
            idx = int(message.command[2]) - 1
            if 0 <= idx < len(store["todos"]):
                store["todos"].pop(idx)
                _save(store)
                await message.reply(f"🗑️ Deleted #{idx+1}")
        elif action == "clear":
            store["todos"] = []
            _save(store)
            await message.reply("🧹 Cleared all todos")
        else:
            # Treat whole thing as new todo text
            text = " ".join(message.command[1:])
            store["todos"].append({
                "text": text,
                "done": False,
                "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
            })
            _save(store)
            await message.reply(f"➕ Added todo #{len(store['todos'])}: {text[:200]}")
    register_command("Notes", "todo", "Persistent todo list (add/done/del/clear)", [])

    @app.on_message(filters.command("todos", prefixes=".") & filters.me)
    async def _todos_cmd(client, message):
        store = _load()
        todos = store.get("todos", [])
        if not todos:
            return await message.reply("No todos. Use `.todo <text>` to add.")
        lines = []
        for i, t in enumerate(todos, 1):
            mark = "✅" if t.get("done") else "⬜"
            lines.append(f"{mark} {i}. {t['text'][:200]}\n     _{t['ts']}_")
        await message.reply("📝 **Todos:**\n\n" + "\n".join(lines))
    register_command("Notes", "todos", "List all todos", [])

    # ─────────── REMINDERS (basic in-memory) ───────────

    REMINDERS = []

    @app.on_message(filters.command("remind", prefixes=".") & filters.me)
    async def _remind_cmd(client, message):
        """
        .remind <time> <text>
        time: 30s, 5m, 1h, 2h30m
        """
        if len(message.command) < 3:
            return await message.reply("Usage: `.remind <time> <text>`\nExamples: `.remind 30m call mom`, `.remind 2h deploy`")
        time_str = message.command[1]
        text = " ".join(message.command[2:])
        # Parse time
        import re
        m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", time_str)
        if not m or not any(m.groups()):
            return await message.reply("Invalid time. Use format like `30s`, `5m`, `1h`, `2h30m`")
        h, mn, s = m.groups()
        total = (int(h or 0) * 3600) + (int(mn or 0) * 60) + int(s or 0)
        if total < 1:
            return await message.reply("Time must be at least 1 second.")

        await message.reply(f"⏰ Reminder set for {total}s: {text[:200]}")

        async def _fire():
            await asyncio.sleep(total)
            try:
                await client.send_message(
                    message.chat.id,
                    f"⏰ **Reminder** ({time_str} ago):\n\n{text}\n\n_(set by {message.from_user.first_name if message.from_user else 'you'})_",
                    reply_to_message_id=message.id,
                )
            except Exception:
                pass

        import asyncio
        asyncio.create_task(_fire())
    register_command("Notes", "remind", "Set a reminder (.remind <time> <text>)", ["reminder"])

    print("[Notes] Registered notes/clipboard/todo/reminder commands")
