"""
KyrenUB - Text-to-Speech Plugin
===============================
Voice message generation using Google TTS (gTTS) — no API key needed.
Supports 50+ languages. Send the resulting voice message back to the chat.
"""

def register(app):
    from pyrogram import filters
    from plugins import register_command
    import asyncio, os, time, subprocess, tempfile

    # Lazy import — gTTS may not be installed in some environments
    def _gtts():
        from gtts import gTTS
        return gTTS

    # Common language codes for /tts langs
    LANGS = {
        "en": "English", "hi": "Hindi", "es": "Spanish", "fr": "French",
        "de": "German", "it": "Italian", "pt": "Portuguese", "ru": "Russian",
        "ja": "Japanese", "ko": "Korean", "zh": "Chinese", "ar": "Arabic",
        "bn": "Bengali", "ur": "Urdu", "tr": "Turkish", "nl": "Dutch",
        "pl": "Polish", "sv": "Swedish", "id": "Indonesian", "th": "Thai",
        "vi": "Vietnamese", "ta": "Tamil", "te": "Telugu", "ml": "Malayalam",
        "mr": "Marathi", "gu": "Gujarati", "pa": "Punjabi", "kn": "Kannada",
        "fa": "Persian", "he": "Hebrew", "el": "Greek", "cs": "Czech",
        "uk": "Ukrainian", "ro": "Romanian", "hu": "Hungarian", "fi": "Finnish",
        "da": "Danish", "no": "Norwegian", "bg": "Bulgarian", "hr": "Croatian",
        "sk": "Slovak", "sl": "Slovenian", "sr": "Serbian", "lt": "Lithuanian",
        "lv": "Latvian", "et": "Estonian", "is": "Icelandic", "ms": "Malay",
        "sw": "Swahili", "af": "Afrikaans", "cy": "Welsh", "eu": "Basque",
        "ca": "Catalan", "gl": "Galician", "sq": "Albanian", "mk": "Macedonian",
    }

    # ─────────── TTS (text -> voice) ───────────

    @app.on_message(filters.command("tts", prefixes=".") & filters.me)
    async def _tts_cmd(client, message):
        """
        .tts <text>                 -> English voice
        .tts hi <text>              -> Hindi voice
        .tts en-in <text>           -> Indian English accent
        Reply to a message: .tts [lang]
        """
        text = ""
        lang = "en"
        if message.reply_to_message and message.reply_to_message.text:
            text = message.reply_to_message.text
            if len(message.command) > 1:
                lang = message.command[1]
        else:
            if len(message.command) < 2:
                return await message.reply(
                    "Usage: `.tts <text>` or `.tts <lang> <text>`\n"
                    "Use `.tts langs` for language codes."
                )
            if message.command[1] == "langs":
                lines = [f"`{k}` {v}" for k, v in LANGS.items()]
                await message.reply("🎙️ **Supported languages:**\n" + "\n".join(lines))
                return
            # if first arg is a known language code, treat as lang
            if message.command[1].lower() in LANGS or "-" in message.command[1]:
                lang = message.command[1]
                text = " ".join(message.command[2:])
            else:
                text = " ".join(message.command[1:])

        if not text:
            return await message.reply("No text to speak. Usage: `.tts <lang> <text>`")

        if len(text) > 500:
            text = text[:500]
            await message.reply("⚠️ Text truncated to 500 chars (gTTS limit).")

        try:
            gTTS = _gtts()
        except ImportError:
            return await message.reply(
                "❌ gTTS not installed. Run:\n"
                "```\npip install gTTS\n```\n"
                "Then `.restart` the bot."
            )

        tmp_ogg = None
        tmp_mp3 = None
        try:
            tmp_mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
            tts = gTTS(text=text, lang=lang.split("-")[0], tld=lang.split("-")[1] if "-" in lang else "com", slow=False)
            tts.save(tmp_mp3)

            # Convert to OGG opus for Telegram voice message
            tmp_ogg = tmp_mp3.replace(".mp3", ".ogg")
            subprocess.run(
                ["ffmpeg", "-y", "-i", tmp_mp3, "-c:a", "libopus", "-b:a", "64k", tmp_ogg],
                capture_output=True, timeout=30, check=True,
            )

            await client.send_voice(
                chat_id=message.chat.id,
                voice=tmp_ogg,
                caption=f"🎙️ TTS (`{lang}`): {text[:200]}{'...' if len(text) > 200 else ''}",
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
            )
            # delete the trigger command silently
            try:
                await message.delete()
            except Exception:
                pass
        except subprocess.CalledProcessError as e:
            # ffmpeg failed — send mp3 directly as audio file
            try:
                await client.send_audio(
                    chat_id=message.chat.id,
                    audio=tmp_mp3,
                    caption=f"🎙️ TTS (`{lang}`): {text[:200]}",
                )
            except Exception as e2:
                await message.reply(f"❌ TTS failed: ffmpeg missing? {e2}")
        except Exception as e:
            await message.reply(f"❌ TTS error: `{e}`")
        finally:
            for p in [tmp_mp3, tmp_ogg]:
                if p and os.path.exists(p):
                    try:
                        os.remove(p)
                    except Exception:
                        pass
    register_command("Voice", "tts", "Text-to-speech voice message (gTTS). .tts [lang] <text>", [])

    # ─────────── TTS LANGS ───────────

    @app.on_message(filters.command("tts_langs", prefixes=".") & filters.me)
    async def _tts_langs_cmd(client, message):
        lines = [f"`{k}` {v}" for k, v in LANGS.items()]
        # Split into chunks of 50 lines to avoid message size limit
        for i in range(0, len(lines), 50):
            chunk = "\n".join(lines[i:i+50])
            await message.reply(f"🎙️ **Supported TTS languages** ({i+1}-{min(i+50, len(lines))} of {len(lines)}):\n{chunk}")
            if i + 50 < len(lines):
                await asyncio.sleep(0.5)
    register_command("Voice", "tts_langs", "List supported TTS languages", [])

    # ─────────── VOICE LIST (saved voice presets) ───────────

    @app.on_message(filters.command("voice", prefixes=".") & filters.me)
    async def _voice_cmd(client, message):
        """Alias for tts."""
        await _tts_cmd(client, message)
    register_command("Voice", "voice", "Alias for .tts", ["speak"])

    # ─────────── STT (speech-to-text via Google Web Speech, free) ───────────

    @app.on_message(filters.command("stt", prefixes=".") & filters.me)
    async def _stt_cmd(client, message):
        """Transcribe a voice message to text."""
        if not message.reply_to_message or not message.reply_to_message.voice:
            return await message.reply("Reply to a voice message with `.stt`")
        try:
            import speech_recognition as sr
        except ImportError:
            return await message.reply(
                "❌ speech_recognition not installed. Run:\n"
                "```\npip install SpeechRecognition\n```\n"
                "Then `.restart`."
            )
        tmp_ogg = None
        tmp_wav = None
        try:
            await message.reply("⏬ Downloading voice...")
            tmp_ogg = await message.reply_to_message.download(in_memory=False)
            tmp_wav = tmp_ogg + ".wav"
            subprocess.run(
                ["ffmpeg", "-y", "-i", tmp_ogg, "-ar", "16000", "-ac", "1", tmp_wav],
                capture_output=True, timeout=30, check=True,
            )
            r = sr.Recognizer()
            with sr.AudioFile(tmp_wav) as src:
                audio = r.record(src)
            try:
                text = r.recognize_google(audio)
                await message.reply(f"📝 **Transcription:**\n\n{text}")
            except sr.UnknownValueError:
                await message.reply("❌ Could not understand audio.")
            except sr.RequestError as e:
                await message.reply(f"❌ STT API error: {e}")
        except subprocess.CalledProcessError:
            await message.reply("❌ ffmpeg not available. Install ffmpeg on the VPS.")
        except Exception as e:
            await message.reply(f"❌ STT error: `{e}`")
        finally:
            for p in [tmp_ogg, tmp_wav]:
                if p and os.path.exists(p):
                    try:
                        os.remove(p)
                    except Exception:
                        pass
    register_command("Voice", "stt", "Speech-to-text transcription (reply to voice)", ["transcribe"])

    print("[Voice] Registered TTS/STT commands")
