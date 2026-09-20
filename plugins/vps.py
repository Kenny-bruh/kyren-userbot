"""
KyrenUB - VPS File Bridge Plugin
================================
Commands for moving files between the VPS server and Telegram,
plus filesystem operations: ls, cat, tail, head, grep, find, mv,
cp, rm, mkdir, touch, tree, wc, du, file, chmod, pull, push.

These let you treat the Render/VPS filesystem like a remote shell
straight from Telegram — extremely handy for log inspection, config
tweaks, and pulling logs/screenshots back into chat.
"""

def register(app):
    from pyrogram import filters
    from plugins import register_command
    import asyncio, os, sys, json, re, time, stat, shutil
    import subprocess, hashlib, mimetypes, datetime

    # Track a per-user "current directory" so .ls / .cat feel like a shell
    CWD = {"path": os.getcwd()}

    def _resolve(path: str) -> str:
        if not path:
            return CWD["path"]
        if path.startswith("~"):
            path = os.path.expanduser(path)
        if not os.path.isabs(path):
            path = os.path.join(CWD["path"], path)
        return os.path.normpath(path)

    def _human_size(n: int) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
            if n < 1024:
                return f"{n:.1f}{unit}"
            n /= 1024
        return f"{n:.1f}EB"

    # ─────────── PULL / PUSH (Telegram <-> VPS) ───────────

    @app.on_message(filters.command("pull", prefixes=".") & filters.me)
    async def _pull_cmd(client, message):
        """Pull a file FROM the VPS filesystem and send it to Telegram chat."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.pull <remote_path>`\nExample: `.pull /var/log/syslog`")
        path = _resolve(message.command[1])
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        if os.path.isdir(path):
            return await message.reply("❌ That's a directory. Use `.zip <path>` first or `.ls` to browse.")
        try:
            size = os.path.getsize(path)
            if size > 2 * 1024 * 1024 * 1024:  # 2GB Telegram hard limit
                return await message.reply(f"❌ File too large: {_human_size(size)} (Telegram limit: 2GB)")
            await message.reply(f"⬆️ Pulling `{path}` ({_human_size(size)})...")
            await client.send_document(
                chat_id=message.chat.id,
                document=path,
                caption=f"📦 `{path}`\nSize: {_human_size(size)}\nPulled: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            )
        except Exception as e:
            await message.reply(f"❌ Pull error: `{e}`")
    register_command("VPS", "pull", "Pull a file from VPS to Telegram", [])

    @app.on_message(filters.command("push", prefixes=".") & filters.me)
    async def _push_cmd(client, message):
        """Push a file FROM Telegram TO the VPS filesystem (reply to a file)."""
        if not message.reply_to_message:
            return await message.reply("Reply to a file with `.push <remote_path>` to upload it to the VPS.")
        if not message.reply_to_message.document and not message.reply_to_message.video \
                and not message.reply_to_message.audio and not message.reply_to_message.photo:
            return await message.reply("Reply must be to a file/photo/video/audio.")
        if len(message.command) < 2:
            return await message.reply("Usage: `.push <remote_path>` (reply to a file)\nExample: `.push /tmp/upload.bin`")
        remote_path = _resolve(message.command[1])
        # If target is a directory, use the original filename
        if os.path.isdir(remote_path):
            orig = (message.reply_to_message.document or message.reply_to_message.video
                    or message.reply_to_message.audio)
            fname = orig.file_name if orig and getattr(orig, "file_name", None) else "file.bin"
            remote_path = os.path.join(remote_path, fname)
        try:
            os.makedirs(os.path.dirname(remote_path) or ".", exist_ok=True)
            await message.reply(f"⬇️ Pushing to `{remote_path}`...")
            tmp = await message.reply_to_message.download(in_memory=False)
            shutil.move(tmp, remote_path)
            size = os.path.getsize(remote_path)
            await message.reply(
                f"✅ Pushed to `{remote_path}`\nSize: {_human_size(size)}"
            )
        except Exception as e:
            await message.reply(f"❌ Push error: `{e}`")
    register_command("VPS", "push", "Push a file from Telegram to VPS", [])

    # ─────────── FILESYSTEM BROWSING ───────────

    @app.on_message(filters.command("ls", prefixes=".") & filters.me)
    async def _ls_cmd(client, message):
        path = _resolve(message.command[1] if len(message.command) > 1 else ".")
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        if not os.path.isdir(path):
            return await message.reply(f"❌ Not a directory: `{path}`")
        try:
            entries = sorted(os.listdir(path))
            lines = []
            for name in entries[:80]:
                full = os.path.join(path, name)
                try:
                    st = os.stat(full)
                    tag = "d" if stat.S_ISDIR(st.st_mode) else "-"
                    size = _human_size(st.st_size) if not stat.S_ISDIR(st.st_mode) else "<DIR>"
                    mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%b %d %H:%M")
                    lines.append(f"{tag} {size:>9}  {mtime}  {name}")
                except OSError:
                    lines.append(f"? {'?':>9}  {'?':>12}  {name}")
            header = f"📂 `{path}` ({len(entries)} entries)\n```\n"
            await message.reply(header + "\n".join(lines) + "\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "ls", "List directory contents", ["dir"])

    @app.on_message(filters.command("cat", prefixes=".") & filters.me)
    async def _cat_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.cat <path>`")
        path = _resolve(message.command[1])
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        if os.path.isdir(path):
            return await message.reply("❌ That's a directory.")
        try:
            size = os.path.getsize(path)
            max_read = 3500  # keep us under TG 4096 limit
            with open(path, "r", errors="ignore") as f:
                content = f.read(max_read + 200)
            truncated = "… (truncated)" if len(content) > max_read else ""
            await message.reply(f"📄 `{path}` ({_human_size(size)})\n```\n{content[:max_read]}{truncated}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "cat", "Read a file's contents", ["read"])

    @app.on_message(filters.command("tail", prefixes=".") & filters.me)
    async def _tail_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.tail <path> [lines]` (default 20 lines)")
        path = _resolve(message.command[1])
        n = int(message.command[2]) if len(message.command) > 2 and message.command[2].isdigit() else 20
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        try:
            out = subprocess.run(["tail", "-n", str(n), path],
                                 capture_output=True, text=True, timeout=10)
            text = (out.stdout or out.stderr)[:3500]
            await message.reply(f"📄 tail -n {n} `{path}`\n```\n{text}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "tail", "Last N lines of a file (great for logs)", [])

    @app.on_message(filters.command("head2", prefixes=".") & filters.me)
    async def _head2_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.head2 <path> [lines]`")
        path = _resolve(message.command[1])
        n = int(message.command[2]) if len(message.command) > 2 and message.command[2].isdigit() else 20
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        try:
            out = subprocess.run(["head", "-n", str(n), path],
                                 capture_output=True, text=True, timeout=10)
            text = (out.stdout or out.stderr)[:3500]
            await message.reply(f"📄 head -n {n} `{path}`\n```\n{text}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "head2", "First N lines of a file", [])

    @app.on_message(filters.command("grep", prefixes=".") & filters.me)
    async def _grep_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.grep <pattern> <path>`\nExample: `.grep ERROR /var/log/syslog`")
        pattern = message.command[1]
        path = _resolve(message.command[2])
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        try:
            out = subprocess.run(["grep", "-n", "-E", pattern, path],
                                 capture_output=True, text=True, timeout=10)
            text = (out.stdout or "(no matches)")[:3500]
            await message.reply(f"🔍 grep `{pattern}` in `{path}`\n```\n{text}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "grep", "Search inside a file", ["search_file"])

    @app.on_message(filters.command("find", prefixes=".") & filters.me)
    async def _find_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.find <name> [dir]` (default dir = .)")
        name = message.command[1]
        directory = _resolve(message.command[2]) if len(message.command) > 2 else CWD["path"]
        if not os.path.isdir(directory):
            return await message.reply(f"❌ Not a directory: `{directory}`")
        try:
            out = subprocess.run(["find", directory, "-name", name, "-type", "f"],
                                 capture_output=True, text=True, timeout=15)
            text = (out.stdout or "(none)").strip()
            if not text:
                return await message.reply("No matches.")
            files = text.split("\n")
            shown = "\n".join(files[:40])
            extra = f"\n… (+{len(files) - 40} more)" if len(files) > 40 else ""
            await message.reply(f"🔍 Found {len(files)} file(s):\n```\n{shown}{extra}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "find", "Find files by name", [])

    @app.on_message(filters.command("tree", prefixes=".") & filters.me)
    async def _tree_cmd(client, message):
        directory = _resolve(message.command[1]) if len(message.command) > 1 else CWD["path"]
        if not os.path.isdir(directory):
            return await message.reply(f"❌ Not a directory: `{directory}`")
        try:
            out = subprocess.run(["find", directory, "-maxdepth", "3",
                                  "-not", "-path", "*/\\.*"],
                                 capture_output=True, text=True, timeout=10)
            lines = out.stdout.strip().split("\n")[:60]
            # build a simple tree
            result = []
            for line in lines:
                depth = line.replace(directory, "").count("/")
                result.append("  " * depth + "├─ " + os.path.basename(line))
            await message.reply(f"🌳 `{directory}`\n```\n" + "\n".join(result) + "\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "tree", "Show directory tree (depth 3)", [])

    @app.on_message(filters.command("wc", prefixes=".") & filters.me)
    async def _wc_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.wc <path>`")
        path = _resolve(message.command[1])
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        try:
            with open(path, "r", errors="ignore") as f:
                content = f.read()
            lines = content.count("\n")
            words = len(content.split())
            chars = len(content)
            await message.reply(
                f"📊 `{path}`\nLines: {lines}\nWords: {words}\nChars: {chars}\nSize: {_human_size(os.path.getsize(path))}"
            )
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "wc", "Word/line/char count", [])

    @app.on_message(filters.command("du", prefixes=".") & filters.me)
    async def _du_cmd(client, message):
        directory = _resolve(message.command[1]) if len(message.command) > 1 else CWD["path"]
        if not os.path.exists(directory):
            return await message.reply(f"❌ Not found: `{directory}`")
        try:
            out = subprocess.run(["du", "-sh", directory],
                                 capture_output=True, text=True, timeout=15)
            await message.reply(f"```\n{out.stdout.strip()}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "du", "Disk usage of a path", [])

    @app.on_message(filters.command("file", prefixes=".") & filters.me)
    async def _file_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.file <path>`")
        path = _resolve(message.command[1])
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        try:
            st = os.stat(path)
            mtype = mimetypes.guess_type(path)[0] or "unknown"
            kind = "directory" if stat.S_ISDIR(st.st_mode) else "file"
            perms = stat.filemode(st.st_mode)
            mtime = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            await message.reply(
                f"📄 `{path}`\n"
                f"Type: {kind} ({mtype})\n"
                f"Size: {_human_size(st.st_size)}\n"
                f"Perms: `{perms}`\n"
                f"Modified: {mtime}\n"
                f"Inode: {st.st_ino}"
            )
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "file", "File info (type/size/perms)", [])

    # ─────────── FILE OPS ───────────

    @app.on_message(filters.command("mv", prefixes=".") & filters.me)
    async def _mv_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.mv <src> <dst>`")
        src = _resolve(message.command[1])
        dst = _resolve(message.command[2])
        try:
            shutil.move(src, dst)
            await message.reply(f"✅ Moved `{src}` → `{dst}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "mv", "Move/rename a file", ["rename"])

    @app.on_message(filters.command("cp", prefixes=".") & filters.me)
    async def _cp_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.cp <src> <dst>`")
        src = _resolve(message.command[1])
        dst = _resolve(message.command[2])
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            await message.reply(f"✅ Copied `{src}` → `{dst}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "cp", "Copy a file or directory", ["copy"])

    @app.on_message(filters.command("rm", prefixes=".") & filters.me)
    async def _rm_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.rm <path>` (⚠️ permanent!)")
        path = _resolve(message.command[1])
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            await message.reply(f"🗑️ Deleted `{path}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "rm", "Delete a file or directory (⚠️ permanent)", ["del"])

    @app.on_message(filters.command("mkdir", prefixes=".") & filters.me)
    async def _mkdir_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.mkdir <path>`")
        path = _resolve(message.command[1])
        try:
            os.makedirs(path, exist_ok=True)
            await message.reply(f"✅ Created `{path}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "mkdir", "Create a directory", ["md"])

    @app.on_message(filters.command("touch", prefixes=".") & filters.me)
    async def _touch_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.touch <path>`")
        path = _resolve(message.command[1])
        try:
            with open(path, "a"):
                os.utime(path, None)
            await message.reply(f"✅ Touched `{path}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "touch", "Create empty file / update mtime", [])

    @app.on_message(filters.command("chmod", prefixes=".") & filters.me)
    async def _chmod_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.chmod <mode> <path>`\nExample: `.chmod 755 script.sh`")
        mode = message.command[1]
        path = _resolve(message.command[2])
        try:
            os.chmod(path, int(mode, 8))
            await message.reply(f"✅ chmod {mode} `{path}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "chmod", "Change file permissions", [])

    @app.on_message(filters.command("pwd", prefixes=".") & filters.me)
    async def _pwd_cmd(client, message):
        await message.reply(f"📂 CWD: `{CWD['path']}`")
    register_command("VPS", "pwd", "Show current working directory", [])

    @app.on_message(filters.command("cd", prefixes=".") & filters.me)
    async def _cd_cmd(client, message):
        if len(message.command) < 2:
            CWD["path"] = os.path.expanduser("~")
            return await message.reply(f"📂 CWD: `{CWD['path']}`")
        path = _resolve(message.command[1])
        if not os.path.isdir(path):
            return await message.reply(f"❌ Not a directory: `{path}`")
        CWD["path"] = path
        await message.reply(f"📂 CWD: `{CWD['path']}`")
    register_command("VPS", "cd", "Change working directory", [])

    # ─────────── ARCHIVE OPS ───────────

    @app.on_message(filters.command("zip", prefixes=".") & filters.me)
    async def _zip_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.zip <path>` (creates path.zip)")
        path = _resolve(message.command[1])
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        try:
            out = subprocess.run(["zip", "-r", "-q", f"{path}.zip", path],
                                 capture_output=True, text=True, timeout=60)
            size = os.path.getsize(f"{path}.zip")
            await message.reply(f"✅ Created `{path}.zip` ({_human_size(size)})")
        except FileNotFoundError:
            # fallback to python zipfile
            import zipfile
            with zipfile.ZipFile(f"{path}.zip", "w", zipfile.ZIP_DEFLATED) as zf:
                if os.path.isdir(path):
                    for root, _, files in os.walk(path):
                        for fn in files:
                            fp = os.path.join(root, fn)
                            zf.write(fp, os.path.relpath(fp, path))
                else:
                    zf.write(path, os.path.basename(path))
            size = os.path.getsize(f"{path}.zip")
            await message.reply(f"✅ Created `{path}.zip` ({_human_size(size)})")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "zip", "Zip a file or directory", [])

    @app.on_message(filters.command("unzip", prefixes=".") & filters.me)
    async def _unzip_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.unzip <archive.zip> [dest]`")
        path = _resolve(message.command[1])
        dest = _resolve(message.command[2]) if len(message.command) > 2 else os.path.dirname(path) or "."
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        try:
            import zipfile
            with zipfile.ZipFile(path) as zf:
                zf.extractall(dest)
                names = zf.namelist()
            await message.reply(f"✅ Extracted {len(names)} file(s) to `{dest}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "unzip", "Unzip a .zip archive", ["extract"])

    @app.on_message(filters.command("tar", prefixes=".") & filters.me)
    async def _tar_cmd(client, message):
        """Usage: .tar c <path>  OR  .tar x <archive.tar.gz>"""
        if len(message.command) < 3:
            return await message.reply("Usage: `.tar c <path>` (create) or `.tar x <archive>` (extract)")
        action = message.command[1]
        path = _resolve(message.command[2])
        try:
            if action == "c":
                archive = f"{path}.tar.gz"
                subprocess.run(["tar", "-czf", archive, path],
                               capture_output=True, text=True, timeout=120, check=True)
                size = os.path.getsize(archive)
                await message.reply(f"✅ Created `{archive}` ({_human_size(size)})")
            elif action == "x":
                subprocess.run(["tar", "-xzf", path],
                               capture_output=True, text=True, timeout=120, check=True)
                await message.reply(f"✅ Extracted `{path}`")
            else:
                await message.reply("Action must be `c` (create) or `x` (extract)")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "tar", "Create or extract .tar.gz", [])

    # ─────────── LOG TAIL FOLLOW (one-shot, N seconds) ───────────

    @app.on_message(filters.command("follow", prefixes=".") & filters.me)
    async def _follow_cmd(client, message):
        """Follow a log file for N seconds (default 5s) and dump new lines."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.follow <path> [seconds]`")
        path = _resolve(message.command[1])
        secs = int(message.command[2]) if len(message.command) > 2 and message.command[2].isdigit() else 5
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        try:
            out = subprocess.run(["timeout", str(secs), "tail", "-f", path],
                                 capture_output=True, text=True, timeout=secs + 2)
            text = (out.stdout or "(no output)")[:3500]
            await message.reply(f"📄 followed `{path}` for {secs}s\n```\n{text}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "follow", "Follow a log file for N seconds", ["tailf"])

    # ─────────── PROCESS / SYSTEM ───────────

    @app.on_message(filters.command("ps", prefixes=".") & filters.me)
    async def _ps_cmd(client, message):
        try:
            out = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10)
            lines = out.stdout.split("\n")
            await message.reply(f"```\n" + "\n".join(lines[:30]) + "\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "ps", "Show running processes", [])

    @app.on_message(filters.command("kill", prefixes=".") & filters.me)
    async def _kill_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.kill <pid>`")
        pid = message.command[1]
        try:
            subprocess.run(["kill", pid], check=True)
            await message.reply(f"☠️ Sent SIGTERM to PID {pid}")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "kill", "Kill a process by PID", [])

    @app.on_message(filters.command("killall", prefixes=".") & filters.me)
    async def _killall_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.killall <name>`")
        name = message.command[1]
        try:
            subprocess.run(["killall", name], check=True)
            await message.reply(f"☠️ Killed all `{name}` processes")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "killall", "Kill all processes by name", [])

    @app.on_message(filters.command("disk", prefixes=".") & filters.me)
    async def _disk_cmd(client, message):
        try:
            out = subprocess.run(["df", "-h"], capture_output=True, text=True, timeout=10)
            await message.reply(f"```\n{out.stdout}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "disk", "Show disk usage (df -h)", ["df"])

    @app.on_message(filters.command("free", prefixes=".") & filters.me)
    async def _free_cmd(client, message):
        try:
            out = subprocess.run(["free", "-h"], capture_output=True, text=True, timeout=10)
            await message.reply(f"```\n{out.stdout}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "free", "Show memory usage (free -h)", ["mem"])

    @app.on_message(filters.command("whoami", prefixes=".") & filters.me)
    async def _whoami_cmd(client, message):
        try:
            out = subprocess.run(["whoami"], capture_output=True, text=True, timeout=5)
            await message.reply(f"👤 `{out.stdout.strip()}` (uid={os.getuid()}, gid={os.getgid()})")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "whoami", "Show current user", [])

    @app.on_message(filters.command("hostname", prefixes=".") & filters.me)
    async def _hostname_cmd(client, message):
        try:
            import socket
            await message.reply(f"🖥️ Hostname: `{socket.gethostname()}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "hostname", "Show server hostname", [])

    # ─────────── ENV / SECRETS ───────────

    @app.on_message(filters.command("env", prefixes=".") & filters.me)
    async def _env_cmd(client, message):
        """List environment variables (filtered to hide secrets)."""
        try:
            safe = {}
            for k, v in os.environ.items():
                if any(s in k.upper() for s in ["SECRET", "TOKEN", "PASSWORD", "KEY", "API", "SESSION"]):
                    safe[k] = "***REDACTED***"
                else:
                    safe[k] = v
            text = "\n".join(f"{k}={v}" for k, v in sorted(safe.items()))
            await message.reply(f"```\n{text[:3500]}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "env", "List environment variables (secrets redacted)", [])

    @app.on_message(filters.command("write", prefixes=".") & filters.me)
    async def _write_cmd(client, message):
        """Write text to a file. Usage: .write <path> <content>  (or reply to a message)"""
        if len(message.command) < 2:
            return await message.reply("Usage: `.write <path> <content>` or reply with `.write <path>`")
        path = _resolve(message.command[1])
        if message.reply_to_message and message.reply_to_message.text:
            content = message.reply_to_message.text
        else:
            args = message.command[2:]
            content = " ".join(args)
        if not content:
            return await message.reply("No content to write.")
        try:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            await message.reply(f"✅ Wrote {len(content)} chars to `{path}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "write", "Write text to a file", ["save_file"])

    @app.on_message(filters.command("append", prefixes=".") & filters.me)
    async def _append_cmd(client, message):
        """Append text to a file. Usage: .append <path> <content> (or reply)"""
        if len(message.command) < 2:
            return await message.reply("Usage: `.append <path> <content>`")
        path = _resolve(message.command[1])
        if message.reply_to_message and message.reply_to_message.text:
            content = message.reply_to_message.text + "\n"
        else:
            content = " ".join(message.command[2:]) + "\n"
        try:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "a") as f:
                f.write(content)
            await message.reply(f"✅ Appended {len(content)} chars to `{path}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "append", "Append text to a file", [])

    @app.on_message(filters.command("hashfile", prefixes=".") & filters.me)
    async def _hashfile_cmd(client, message):
        """Compute SHA256/MD5 of a file."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.hashfile <path> [algo]` (default sha256)")
        path = _resolve(message.command[1])
        algo = message.command[2] if len(message.command) > 2 else "sha256"
        if not os.path.exists(path):
            return await message.reply(f"❌ Not found: `{path}`")
        try:
            h = hashlib.new(algo)
            with open(path, "rb") as f:
                while True:
                    chunk = f.read(65536)
                    if not chunk:
                        break
                    h.update(chunk)
            await message.reply(f"{algo}({path}):\n`{h.hexdigest()}`")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "hashfile", "Hash a file (sha256/md5/etc.)", [])

    @app.on_message(filters.command("diff", prefixes=".") & filters.me)
    async def _diff_cmd(client, message):
        """Diff two files."""
        if len(message.command) < 3:
            return await message.reply("Usage: `.diff <file1> <file2>`")
        a = _resolve(message.command[1])
        b = _resolve(message.command[2])
        try:
            out = subprocess.run(["diff", a, b], capture_output=True, text=True, timeout=10)
            text = (out.stdout or "(identical)")[:3500]
            await message.reply(f"```\n{text}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "diff", "Diff two files", [])

    @app.on_message(filters.command("history_log", prefixes=".") & filters.me)
    async def _history_log_cmd(client, message):
        """Show last N lines from a log file with line numbers."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.history_log <path> [n]`")
        path = _resolve(message.command[1])
        n = int(message.command[2]) if len(message.command) > 2 and message.command[2].isdigit() else 50
        try:
            out = subprocess.run(["tail", "-n", str(n), path],
                                 capture_output=True, text=True, timeout=10)
            lines = out.stdout.split("\n")
            numbered = "\n".join(f"{i+1:4d}  {l}" for i, l in enumerate(lines) if l)
            await message.reply(f"```\n{numbered[:3500]}\n```")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("VPS", "history_log", "Show last N log lines with numbers", [])

    print("[VPS] Registered VPS/file bridge commands")
