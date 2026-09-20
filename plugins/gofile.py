"""
KyrenUB - GoFile Uploader Plugin
================================
Permanent command for uploading files (replied-to or from URL) to GoFile
and returning the public download link in the original chat AND in
Saved Messages — no code changes needed next time.

Uses GoFile's public API:
  1. GET https://api.gofile.io/servers  -> pick a server
  2. POST https://{server}.gofile.io/contents/uploadfile  -> get download page URL
"""

def register(app):
    from pyrogram import filters
    from plugins import register_command
    import asyncio, os, json, time, urllib.parse, urllib.request
    import urllib.error

    GOFILE_API = "https://api.gofile.io"
    HISTORY_FILE = "/tmp/kyren_gofile_history.json"

    def _load_history():
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE) as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_history(entry):
        hist = _load_history()
        hist.insert(0, entry)
        hist = hist[:50]  # keep last 50
        with open(HISTORY_FILE, "w") as f:
            json.dump(hist, f, indent=2)

    def _get_server():
        """Pick a random GoFile server."""
        req = urllib.request.Request(f"{GOFILE_API}/servers", headers={"User-Agent": "KyrenUB/2.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        servers = data.get("data", {}).get("servers", [])
        if not servers:
            raise RuntimeError("No GoFile servers available")
        return servers[0]["name"]

    def _upload_file(local_path):
        """Upload a local file to GoFile, return the download page URL."""
        server = _get_server()
        url = f"https://{server}.gofile.io/contents/uploadfile"

        # Build multipart/form-data
        boundary = "----KyrenUBBoundary" + str(int(time.time() * 1000))
        filename = os.path.basename(local_path)
        with open(local_path, "rb") as f:
            file_data = f.read()

        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "User-Agent": "KyrenUB/2.0",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=300) as r:
            resp = json.loads(r.read())
        if resp.get("status") != "ok":
            raise RuntimeError(f"GoFile error: {resp}")
        page = resp["data"].get("downloadPage")
        code = resp["data"].get("code")
        return page, code

    def _download_url(url, dest="/tmp/kyren_dl.bin"):
        """Download a URL to a local file."""
        req = urllib.request.Request(url, headers={"User-Agent": "KyrenUB/2.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            with open(dest, "wb") as f:
                while True:
                    chunk = r.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
        return dest

    # ─────────── MAIN GOFILE COMMAND ───────────

    @app.on_message(filters.command("gofile", prefixes=".") & filters.me)
    async def _gofile_cmd(client, message):
        """
        Upload to GoFile:
          .gofile (reply to file)            -> upload replied file
          .gofile <url>                      -> download URL then upload
          .gofile <vps_path>                 -> upload file from VPS filesystem
        Returns the download link in this chat AND in Saved Messages.
        """
        arg = message.command[1] if len(message.command) > 1 else None
        replied = message.reply_to_message

        if not arg and not replied:
            return await message.reply(
                "Usage:\n"
                "• `.gofile` (reply to a file)\n"
                "• `.gofile <url>` (download URL first)\n"
                "• `.gofile <vps_path>` (upload file from server)"
            )

        local_path = None
        source = ""
        try:
            if arg and (arg.startswith("http://") or arg.startswith("https://")):
                await message.reply("⬇️ Downloading from URL...")
                fname = arg.split("/")[-1].split("?")[0] or "download.bin"
                local_path = f"/tmp/kyren_gofile_{int(time.time())}_{fname}"
                _download_url(arg, local_path)
                source = f"URL: {arg}"
            elif arg:
                if not os.path.exists(arg):
                    return await message.reply(f"❌ VPS file not found: `{arg}`")
                local_path = arg
                source = f"VPS: `{arg}`"
            elif replied and (replied.document or replied.video or replied.audio or replied.photo):
                await message.reply("⬇️ Downloading from Telegram...")
                local_path = await replied.download(in_memory=False)
                source = "Telegram message"
            else:
                return await message.reply("Reply to a file, give a URL, or a VPS path.")

            size = os.path.getsize(local_path)
            await message.reply(f"⬆️ Uploading `{os.path.basename(local_path)}` ({size/1024/1024:.2f} MB) to GoFile...")

            page_url, code = await asyncio.get_event_loop().run_in_executor(
                None, _upload_file, local_path
            )

            entry = {
                "filename": os.path.basename(local_path),
                "size": size,
                "page": page_url,
                "code": code,
                "source": source,
                "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            _save_history(entry)

            text = (
                f"📤 **GoFile Upload Complete**\n\n"
                f"📄 File: `{entry['filename']}`\n"
                f"📦 Size: `{size/1024/1024:.2f} MB`\n"
                f"🔗 Link: {page_url}\n"
                f"🔑 Code: `{code}`\n"
                f"📅 {entry['ts']}"
            )

            # Reply in current chat
            await message.reply(text)

            # Also send to Saved Messages for persistence
            try:
                await client.send_message("me", text)
            except Exception:
                pass

        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")[:500]
            await message.reply(f"❌ GoFile HTTP {e.code}: {err_body}")
        except Exception as e:
            await message.reply(f"❌ GoFile error: `{e}`")
        finally:
            # Clean up downloaded temp file (but not VPS-sourced files)
            if local_path and arg and arg.startswith("http"):
                try:
                    os.remove(local_path)
                except Exception:
                    pass
            elif local_path and replied:
                try:
                    os.remove(local_path)
                except Exception:
                    pass
    register_command("GoFile", "gofile", "Upload file/URL/VPS file to GoFile (link sent to chat + Saved Messages)", [])

    # ─────────── GOFILE HISTORY ───────────

    @app.on_message(filters.command("gofilehistory", prefixes=".") & filters.me)
    async def _gofilehistory_cmd(client, message):
        """Show your last 10 GoFile uploads."""
        hist = _load_history()
        if not hist:
            return await message.reply("No GoFile uploads yet.")
        lines = []
        for i, e in enumerate(hist[:10], 1):
            lines.append(
                f"{i}. **{e['filename']}** ({e['size']/1024/1024:.2f} MB)\n"
                f"   🔗 {e['page']}\n"
                f"   📅 {e['ts']}"
            )
        await message.reply("📤 **Recent GoFile Uploads**\n\n" + "\n\n".join(lines))
    register_command("GoFile", "gofilehistory", "Show last 10 GoFile uploads", ["gofilehist"])

    # ─────────── GOFILE DIRECT LINK ───────────

    @app.on_message(filters.command("gofilelink", prefixes=".") & filters.me)
    async def _gofilelink_cmd(client, message):
        """Get a fresh direct-download link for a GoFile content code."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.gofilelink <code>` or `.gofilelink <page_url>`")
        arg = message.command[1]
        code = arg.split("/")[-1] if "/" in arg else arg
        try:
            req = urllib.request.Request(
                f"{GOFILE_API}/contents/{code}",
                headers={"User-Agent": "KyrenUB/2.0"},
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
            if data.get("status") != "ok":
                return await message.reply(f"❌ {data}")
            contents = data["data"].get("contents", {})
            if not contents:
                return await message.reply("❌ No files in that GoFile content.")
            lines = []
            for fid, finfo in list(contents.items())[:5]:
                lines.append(
                    f"📄 **{finfo.get('name')}** ({finfo.get('size', 0)/1024/1024:.2f} MB)\n"
                    f"   🔗 {finfo.get('link')}\n"
                    f"   ⏰ Direct: {finfo.get('directLink', 'N/A')}"
                )
            await message.reply("\n\n".join(lines))
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("GoFile", "gofilelink", "Get direct link for a GoFile code", [])

    # ─────────── GOFILE ACCOUNT ───────────

    @app.on_message(filters.command("gofileaccount", prefixes=".") & filters.me)
    async def _gofileaccount_cmd(client, message):
        """Create a guest GoFile account and store the token (for managing uploads)."""
        try:
            req = urllib.request.Request(
                f"{GOFILE_API}/accounts",
                headers={"User-Agent": "KyrenUB/2.0"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
            if data.get("status") != "ok":
                return await message.reply(f"❌ {data}")
            tok = data["data"].get("token")
            with open("/tmp/kyren_gofile_token.txt", "w") as f:
                f.write(tok)
            await message.reply(
                f"✅ Created guest GoFile account\n"
                f"🔑 Token: `{tok}`\n"
                f"💾 Saved to `/tmp/kyren_gofile_token.txt`\n\n"
                f"Use this token to manage uploads at https://gofile.io/myProfile"
            )
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("GoFile", "gofileaccount", "Create a guest GoFile account token", [])

    print("[GoFile] Registered GoFile uploader commands")
