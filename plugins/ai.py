"""
KyrenUB - AI Plugin (Free, no API key)
======================================
Uses Pollinations.ai for text completion, image generation, and OpenAI-compatible
endpoints that don't require a key. Falls back gracefully if a service is down.
"""

def register(app):
    from pyrogram import filters
    from plugins import register_command
    import asyncio, os, json, time, urllib.request, urllib.parse, urllib.error
    import tempfile, subprocess

    USER_AGENT = "KyrenUB/2.0"

    # ─────────── AI CHAT (Pollinations OpenAI-compatible endpoint) ───────────

    @app.on_message(filters.command("ai", prefixes=".") & filters.me)
    async def _ai_cmd(client, message):
        """Free AI chat using Pollinations OpenAI-compatible endpoint."""
        prompt = message.command[1:] if len(message.command) > 1 else None
        if message.reply_to_message and message.reply_to_message.text:
            prompt_text = message.reply_to_message.text
        elif prompt:
            prompt_text = " ".join(prompt)
        else:
            return await message.reply("Usage: `.ai <prompt>` or reply to a message with `.ai`")
        if len(prompt_text) > 4000:
            prompt_text = prompt_text[:4000]
        status = await message.reply("🤖 Thinking...")
        try:
            payload = json.dumps({
                "model": "openai",
                "messages": [{"role": "user", "content": prompt_text}],
                "temperature": 0.7,
            }).encode()
            req = urllib.request.Request(
                "https://text.pollinations.ai/openai/",
                data=payload,
                headers={
                    "User-Agent": USER_AGENT,
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read().decode("utf-8", errors="ignore")
            # Response may be JSON or plain text
            try:
                data = json.loads(body)
                text = data.get("choices", [{}])[0].get("message", {}).get("content", body)
            except Exception:
                text = body
            text = text.strip()
            if not text:
                return await status.edit("❌ Empty AI response. Try again.")
            # Truncate to TG 4096 limit
            if len(text) > 3500:
                text = text[:3500] + "\n\n… (truncated)"
            await status.edit(f"🤖 **AI**:\n\n{text}")
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="ignore")[:500]
            await status.edit(f"❌ AI HTTP {e.code}: {err}")
        except Exception as e:
            await status.edit(f"❌ AI error: `{e}`")
    register_command("AI", "ai", "Free AI chat (Pollinations, no key)", ["chat", "ask"])

    # ─────────── AI TEXT (raw, no system prompt) ───────────

    @app.on_message(filters.command("aitext", prefixes=".") & filters.me)
    async def _aitext_cmd(client, message):
        """Plain text from Pollinations GET endpoint."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.aitext <prompt>`")
        prompt = " ".join(message.command[1:])
        status = await message.reply("🤖 Generating...")
        try:
            url = "https://text.pollinations.ai/" + urllib.parse.quote(prompt)
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as r:
                text = r.read().decode("utf-8", errors="ignore").strip()
            if len(text) > 3500:
                text = text[:3500] + "… (truncated)"
            await status.edit(f"🤖 {text}")
        except Exception as e:
            await status.edit(f"❌ {e}")
    register_command("AI", "aitext", "Plain AI text generation (GET endpoint)", [])

    # ─────────── AI IMAGE ───────────

    @app.on_message(filters.command("aimage", prefixes=".") & filters.me)
    async def _aimage_cmd(client, message):
        """AI image generation via Pollinations."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.aimage <prompt>` (reply with `.aimage <seed> <prompt>` for reproducible)")
        if message.command[1].isdigit():
            seed = message.command[1]
            prompt = " ".join(message.command[2:])
        else:
            seed = int(time.time()) % 1000000
            prompt = " ".join(message.command[1:])
        if not prompt:
            return await message.reply("No prompt provided.")
        status = await message.reply("🎨 Generating image...")
        tmp_path = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
        try:
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&seed={seed}&nologo=true"
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=120) as r:
                with open(tmp_path, "wb") as f:
                    while True:
                        chunk = r.read(65536)
                        if not chunk:
                            break
                        f.write(chunk)
            size = os.path.getsize(tmp_path)
            if size < 1000:
                with open(tmp_path, "r", errors="ignore") as f:
                    err = f.read()[:500]
                return await status.edit(f"❌ Image generation failed: {err}")
            await message.reply_photo(
                photo=tmp_path,
                caption=f"🎨 **AI Image**\nSeed: `{seed}`\nPrompt: {prompt[:300]}",
            )
            try: await status.delete()
            except Exception: pass
        except Exception as e:
            await status.edit(f"❌ {e}")
        finally:
            if os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except Exception: pass
    register_command("AI", "aimage", "AI image generation (Pollinations, no key)", ["genimg", "draw"])

    # ─────────── AI SUMMARIZE ───────────

    @app.on_message(filters.command("summarize", prefixes=".") & filters.me)
    async def _summarize_cmd(client, message):
        """Summarize a long message using AI."""
        if message.reply_to_message and message.reply_to_message.text:
            text = message.reply_to_message.text
        elif len(message.command) > 1:
            text = " ".join(message.command[1:])
        else:
            return await message.reply("Reply to a long message with `.summarize` or pass text.")
        if len(text) < 100:
            return await message.reply("Text too short to summarize.")
        status = await message.reply("📝 Summarizing...")
        try:
            prompt = f"Summarize the following text in 5 bullet points:\n\n{text[:3000]}"
            url = "https://text.pollinations.ai/" + urllib.parse.quote(prompt)
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as r:
                summary = r.read().decode("utf-8", errors="ignore").strip()
            await status.edit(f"📝 **Summary:**\n\n{summary}")
        except Exception as e:
            await status.edit(f"❌ {e}")
    register_command("AI", "summarize", "AI-summarize a long message", ["summary"])

    # ─────────── AI CODE ───────────

    @app.on_message(filters.command("code", prefixes=".") & filters.me)
    async def _code_cmd(client, message):
        """Ask AI to write code."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.code <prompt>` (e.g. `.code python script to find duplicate files`)")
        prompt = "Write code for: " + " ".join(message.command[1:])
        status = await message.reply("💻 Coding...")
        try:
            url = "https://text.pollinations.ai/" + urllib.parse.quote(prompt)
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=90) as r:
                text = r.read().decode("utf-8", errors="ignore").strip()
            await status.edit(f"💻 **Code**:\n\n{text[:3500]}")
        except Exception as e:
            await status.edit(f"❌ {e}")
    register_command("AI", "code", "Ask AI to write code", ["codegen"])

    # ─────────── AI EXPLAIN ───────────

    @app.on_message(filters.command("explain", prefixes=".") & filters.me)
    async def _explain_cmd(client, message):
        """AI explains a concept or replied code."""
        if message.reply_to_message and message.reply_to_message.text:
            target = message.reply_to_message.text
        elif len(message.command) > 1:
            target = " ".join(message.command[1:])
        else:
            return await message.reply("Reply to code/concept with `.explain` or pass text.")
        status = await message.reply("📚 Explaining...")
        try:
            prompt = f"Explain this in simple terms with examples:\n\n{target[:3000]}"
            url = "https://text.pollinations.ai/" + urllib.parse.quote(prompt)
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as r:
                text = r.read().decode("utf-8", errors="ignore").strip()
            await status.edit(f"📚 **Explanation**:\n\n{text[:3500]}")
        except Exception as e:
            await status.edit(f"❌ {e}")
    register_command("AI", "explain", "AI explains code/concept", [])

    # ─────────── AI TRANSLATE ───────────

    @app.on_message(filters.command("translate", prefixes=".") & filters.me)
    async def _translate_cmd(client, message):
        """Translate text using AI."""
        if len(message.command) < 2:
            return await message.reply(
                "Usage: `.translate <target_lang> <text>`\n"
                "Example: `.translate hindi Hello world`"
            )
        target = message.command[1]
        text = " ".join(message.command[2:])
        if not text:
            return await message.reply("No text to translate.")
        status = await message.reply("🌐 Translating...")
        try:
            prompt = f"Translate the following text to {target}. Reply with ONLY the translation, no explanations.\n\n{text[:2000]}"
            url = "https://text.pollinations.ai/" + urllib.parse.quote(prompt)
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as r:
                translated = r.read().decode("utf-8", errors="ignore").strip()
            await status.edit(f"🌐 **{target}**:\n\n{translated}")
        except Exception as e:
            await status.edit(f"❌ {e}")
    register_command("AI", "translate", "AI-powered translation", ["tr"])

    # ─────────── DICTIONARY (free dictionaryapi.dev) ───────────

    @app.on_message(filters.command("define", prefixes=".") & filters.me)
    async def _define_cmd(client, message):
        """Dictionary definition (free, no key)."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.define <word>`")
        word = message.command[1]
        try:
            req = urllib.request.Request(
                f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}",
                headers={"User-Agent": USER_AGENT},
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
            if not data:
                return await message.reply(f"No definition for `{word}`.")
            entry = data[0]
            phonetic = entry.get("phonetic", "")
            meanings = entry.get("meanings", [])[:3]
            lines = [f"📖 **{word}** {phonetic}"]
            for m in meanings:
                pos = m.get("partOfSpeech", "")
                defs = m.get("definitions", [])[:2]
                for d in defs:
                    lines.append(f"\n*({pos})* {d.get('definition', '')}")
                    if d.get("example"):
                        lines.append(f"  _\"{d['example']}\"_")
            await message.reply("\n".join(lines)[:3500])
        except urllib.error.HTTPError as e:
            if e.code == 404:
                await message.reply(f"❌ No definition found for `{word}`.")
            else:
                await message.reply(f"❌ HTTP {e.code}")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("AI", "define", "Dictionary lookup (free)", ["dict"])

    # ─────────── WIKIPEDIA ───────────

    @app.on_message(filters.command("wiki", prefixes=".") & filters.me)
    async def _wiki_cmd(client, message):
        """Wikipedia summary."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.wiki <topic>`")
        topic = " ".join(message.command[1:])
        try:
            req = urllib.request.Request(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(topic)}",
                headers={"User-Agent": USER_AGENT},
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
            title = data.get("title", topic)
            extract = data.get("extract", "No summary available.")
            url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            await message.reply(f"📚 **{title}**\n\n{extract}\n\n🔗 {url}")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("AI", "wiki", "Wikipedia summary", ["wikipedia"])

    # ─────────── URBAN DICTIONARY ───────────

    @app.on_message(filters.command("urban", prefixes=".") & filters.me)
    async def _urban_cmd(client, message):
        """Urban Dictionary definition."""
        if len(message.command) < 2:
            return await message.reply("Usage: `.urban <term>`")
        term = " ".join(message.command[1:])
        try:
            req = urllib.request.Request(
                f"https://api.urbandictionary.com/v0/define?term={urllib.parse.quote(term)}",
                headers={"User-Agent": USER_AGENT},
            )
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read())
            items = data.get("list", [])
            if not items:
                return await message.reply(f"No urban def for `{term}`.")
            top = items[0]
            definition = top.get("definition", "")[:1500]
            example = top.get("example", "")
            text = f"📚 **{term}** (Urban)\n\n{definition}"
            if example:
                text += f"\n\n_Example: {example[:500]}_"
            await message.reply(text[:3500])
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("AI", "urban", "Urban Dictionary lookup", [])

    # ─────────── OCR (image to text) ───────────

    @app.on_message(filters.command("ocr", prefixes=".") & filters.me)
    async def _ocr_cmd(client, message):
        """OCR on a replied image using free OCR.space API (no key needed for limited use)."""
        if not message.reply_to_message or not (message.reply_to_message.photo or message.reply_to_message.document):
            return await message.reply("Reply to an image with `.ocr`")
        status = await message.reply("👁️ Running OCR...")
        tmp = None
        try:
            tmp = await message.reply_to_message.download(in_memory=False)
            # Try pytesseract first
            try:
                import pytesseract
                from PIL import Image
                img = Image.open(tmp)
                text = pytesseract.image_to_string(img).strip()
                if text:
                    return await status.edit(f"👁️ **OCR Result**:\n\n```\n{text[:3000]}\n```")
            except ImportError:
                pass

            # Fallback to OCR.space free API
            import mimetypes, base64
            with open(tmp, "rb") as f:
                file_data = f.read()
            boundary = "----KyrenOCRB" + str(int(time.time()))
            body = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="file"; filename="image.jpg"\r\n'
                f"Content-Type: image/jpeg\r\n\r\n"
            ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
            req = urllib.request.Request(
                "https://api.ocr.space/parse/image",
                data=body,
                headers={
                    "User-Agent": USER_AGENT,
                    "Content-Type": f"multipart/form-data; boundary={boundary}",
                    "apikey": "K8456794158857",  # public free demo key
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read())
            parsed = data.get("ParsedResults", [{}])[0].get("ParsedText", "").strip()
            if parsed:
                await status.edit(f"👁️ **OCR Result**:\n\n```\n{parsed[:3000]}\n```")
            else:
                await status.edit("❌ No text found in image.")
        except Exception as e:
            await status.edit(f"❌ OCR error: `{e}`")
        finally:
            if tmp and os.path.exists(tmp):
                try: os.remove(tmp)
                except Exception: pass
    register_command("AI", "ocr", "Extract text from image (reply to photo)", [])

    print("[AI] Registered AI/translate/OCR commands")
