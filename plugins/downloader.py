"""
KyrenUB - Media Downloader Plugin
=================================
Download videos/audio from YouTube, Instagram, TikTok, Twitter/X, Facebook,
and any direct URL using yt-dlp. Auto-uploads the file back to Telegram.
Falls back to a plain HTTP download if yt-dlp isn't installed.
"""

def register(app):
    from pyrogram import filters
    from plugins import register_command
    import asyncio, os, time, subprocess, tempfile, urllib.request
    import urllib.error, json

    MAX_SIZE = 500 * 1024 * 1024  # 500 MB hard cap to keep Render from OOMing

    def _human(n):
        for u in ["B", "KB", "MB", "GB"]:
            if n < 1024:
                return f"{n:.1f}{u}"
            n /= 1024
        return f"{n:.1f}TB"

    def _check_ytdlp():
        try:
            subprocess.run(["yt-dlp", "--version"], capture_output=True, timeout=5)
            return True
        except Exception:
            return False

    async def _download_and_send(message, url, mode="auto"):
        """
        mode: 'video' | 'audio' | 'auto'
        Downloads via yt-dlp; falls back to plain HTTP for direct URLs.
        Sends the file back to Telegram.
        """
        status = await message.reply(f"⬇️ Downloading `{url[:80]}` ...")

        if not _check_ytdlp():
            # Plain HTTP fallback for direct file URLs
            try:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix="_kyren_dl").name
                req = urllib.request.Request(url, headers={"User-Agent": "KyrenUB/2.0"})
                with urllib.request.urlopen(req, timeout=120) as r:
                    total = int(r.headers.get("Content-Length", 0))
                    with open(tmp, "wb") as f:
                        downloaded = 0
                        while True:
                            chunk = r.read(65536)
                            if not chunk:
                                break
                            f.write(chunk)
                            downloaded += len(chunk)
                            if downloaded > MAX_SIZE:
                                f.close()
                                os.remove(tmp)
                                return await status.edit(f"❌ File too large (> {_human(MAX_SIZE)})")
                size = os.path.getsize(tmp)
                await status.edit(f"⬆️ Uploading to Telegram ({_human(size)})...")
                await message.reply_document(
                    document=tmp,
                    caption=f"📥 Downloaded from {url[:200]}",
                )
                try: await status.delete()
                except Exception: pass
            except Exception as e:
                await status.edit(f"❌ Download error: `{e}`\nInstall yt-dlp for site support: `pip install yt-dlp`")
            return

        # yt-dlp path
        outdir = tempfile.mkdtemp(prefix="kyren_ytdl_")
        try:
            if mode == "audio":
                cmd = [
                    "yt-dlp", "-x", "--audio-format", "mp3",
                    "--audio-quality", "0",
                    "--max-filesize", str(MAX_SIZE),
                    "-o", f"{outdir}/%(title).80s.%(ext)s",
                    url,
                ]
            else:
                cmd = [
                    "yt-dlp",
                    "-f", "best[ext=mp4][filesize<500M]/best[filesize<500M]/best",
                    "--max-filesize", str(MAX_SIZE),
                    "-o", f"{outdir}/%(title).80s.%(ext)s",
                    url,
                ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if proc.returncode != 0:
                err = (proc.stderr or proc.stdout or "unknown")[:800]
                return await status.edit(f"❌ yt-dlp error:\n```\n{err}\n```")

            files = [os.path.join(outdir, f) for f in os.listdir(outdir)]
            files = [f for f in files if os.path.isfile(f)]
            if not files:
                return await status.edit("❌ yt-dlp finished but no file was produced.")

            for fpath in files[:3]:  # cap at 3 files per request
                size = os.path.getsize(fpath)
                await status.edit(f"⬆️ Uploading `{os.path.basename(fpath)}` ({_human(size)})...")
                try:
                    if mode == "audio":
                        await message.reply_audio(
                            audio=fpath,
                            caption=f"🎵 `{os.path.basename(fpath)}`\n📥 {url[:200]}",
                        )
                    else:
                        await message.reply_document(
                            document=fpath,
                            caption=f"📥 `{os.path.basename(fpath)}`\nSource: {url[:200]}",
                        )
                except Exception as e:
                    await status.edit(f"❌ Upload error: `{e}`")

            try: await status.delete()
            except Exception: pass
        finally:
            # Cleanup
            for f in os.listdir(outdir):
                try: os.remove(os.path.join(outdir, f))
                except Exception: pass
            try: os.rmdir(outdir)
            except Exception: pass

    # ─────────── GENERIC YTDLP ───────────

    @app.on_message(filters.command("ytdl", prefixes=".") & filters.me)
    async def _ytdl_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.ytdl <url>` (video) or `.ytdl audio <url>` (mp3)")
        mode = "video"
        if message.command[1] in ("audio", "mp3", "a"):
            if len(message.command) < 3:
                return await message.reply("Usage: `.ytdl audio <url>`")
            mode = "audio"
            url = message.command[2]
        else:
            url = message.command[1]
        if not url.startswith("http"):
            return await message.reply("❌ URL must start with http(s)://")
        await _download_and_send(message, url, mode=mode)
    register_command("Download", "ytdl", "Download video/audio via yt-dlp. .ytdl [audio] <url>", ["yt"])

    @app.on_message(filters.command("ytmp3", prefixes=".") & filters.me)
    async def _ytmp3_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.ytmp3 <youtube_url>`")
        url = message.command[1]
        await _download_and_send(message, url, mode="audio")
    register_command("Download", "ytmp3", "Download YouTube audio as MP3", [])

    @app.on_message(filters.command("ytmp4", prefixes=".") & filters.me)
    async def _ytmp4_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.ytmp4 <youtube_url>`")
        url = message.command[1]
        await _download_and_send(message, url, mode="video")
    register_command("Download", "ytmp4", "Download YouTube video as MP4", [])

    # ─────────── INSTAGRAM ───────────

    @app.on_message(filters.command("insta", prefixes=".") & filters.me)
    async def _insta_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.insta <instagram_post_or_reel_url>`")
        url = message.command[1]
        await _download_and_send(message, url, mode="video")
    register_command("Download", "insta", "Download Instagram post/reel", ["instagram"])

    # ─────────── TIKTOK ───────────

    @app.on_message(filters.command("tiktok", prefixes=".") & filters.me)
    async def _tiktok_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.tiktok <tiktok_url>`")
        url = message.command[1]
        await _download_and_send(message, url, mode="video")
    register_command("Download", "tiktok", "Download TikTok video", ["tt"])

    # ─────────── TWITTER / X ───────────

    @app.on_message(filters.command("twitter", prefixes=".") & filters.me)
    async def _twitter_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.twitter <tweet_url>`")
        url = message.command[1]
        await _download_and_send(message, url, mode="video")
    register_command("Download", "twitter", "Download Twitter/X video", ["x"])

    # ─────────── FACEBOOK ───────────

    @app.on_message(filters.command("facebook", prefixes=".") & filters.me)
    async def _facebook_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.facebook <fb_video_url>`")
        url = message.command[1]
        await _download_and_send(message, url, mode="video")
    register_command("Download", "facebook", "Download Facebook video", ["fb"])

    # ─────────── GENERIC DIRECT DOWNLOAD ───────────

    @app.on_message(filters.command("download", prefixes=".") & filters.me)
    async def _download_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.download <direct_url>`")
        url = message.command[1]
        await _download_and_send(message, url, mode="video")
    register_command("Download", "download", "Download any URL via yt-dlp (or direct HTTP fallback)", ["dl"])

    # ─────────── YT-DLP INFO ───────────

    @app.on_message(filters.command("ytdl_info", prefixes=".") & filters.me)
    async def _ytdl_info_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.ytdl_info <url>` (shows formats without downloading)")
        url = message.command[1]
        status = await message.reply("ℹ️ Fetching info...")
        try:
            proc = subprocess.run(
                ["yt-dlp", "--list-formats", "--no-playlist", url],
                capture_output=True, text=True, timeout=60,
            )
            out = (proc.stdout or proc.stderr)[:3500]
            await status.edit(f"📋 **Formats for** `{url[:80]}`\n```\n{out}\n```")
        except Exception as e:
            await status.edit(f"❌ {e}")
    register_command("Download", "ytdl_info", "List available formats for a URL", ["ytdl_formats"])

    # ─────────── YTDLP UPDATE ───────────

    @app.on_message(filters.command("ytdl_update", prefixes=".") & filters.me)
    async def _ytdl_update_cmd(client, message):
        status = await message.reply("⬆️ Updating yt-dlp...")
        try:
            proc = subprocess.run(
                ["pip", "install", "--upgrade", "yt-dlp"],
                capture_output=True, text=True, timeout=120,
            )
            out = (proc.stdout or proc.stderr)[-2000:]
            await status.edit(f"```\n{out}\n```")
        except Exception as e:
            await status.edit(f"❌ {e}")
    register_command("Download", "ytdl_update", "Update yt-dlp to latest version", [])

    # ─────────── PLAYLIST INFO ───────────

    @app.on_message(filters.command("playlist", prefixes=".") & filters.me)
    async def _playlist_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.playlist <url>` (lists first 20 items)")
        url = message.command[1]
        status = await message.reply("📋 Fetching playlist...")
        try:
            proc = subprocess.run(
                ["yt-dlp", "--flat-playlist", "--print", "%(position)s. %(title)s [%(id)s]",
                 "--playlist-items", "1-20", url],
                capture_output=True, text=True, timeout=60,
            )
            out = (proc.stdout or "(empty)")[:3500]
            await status.edit(f"📋 **Playlist** `{url[:80]}`\n```\n{out}\n```")
        except Exception as e:
            await status.edit(f"❌ {e}")
    register_command("Download", "playlist", "List first 20 items in a playlist", [])

    print("[Download] Registered media downloader commands")
