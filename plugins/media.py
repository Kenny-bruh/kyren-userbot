"""
KyrenUB - Media Plugin
======================
57 commands for image manipulation, stickers, screen capture,
downloads, and media utilities. Uses PIL/Pillow.
Download with message.download(). Clean temp files.
"""


def register(app):
    from pyrogram import filters
    from pyrogram.errors import FloodWait
    from plugins import register_command
    import asyncio
    import os
    import random
    import time
    import subprocess
    import tempfile
    import shutil

    _TMP = tempfile.gettempdir()

    def _tmp_path(ext="png"):
        return os.path.join(_TMP, f"kyrenub_{random.randint(10000,99999)}.{ext}")

    def _cleanup(*paths):
        for p in paths:
            try:
                if p and os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass

    def _get_pil():
        try:
            from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont, ImageOps
            return Image, ImageDraw, ImageFilter, ImageEnhance, ImageFont, ImageOps
        except ImportError:
            return None

    # ═══════════════════════════════════════════════════════════════
    #  IMAGE (19 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("resize", prefixes=".") & filters.me)
    async def resize_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.resize <width> <height>`")
            return
        try:
            w, h = int(args[1]), int(args[2])
        except ValueError:
            await message.edit("❌ Invalid dimensions.")
            return
        msg = await message.edit("⏳ Resizing...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            img = img.resize((w, h), Image.LANCZOS)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "resize", "Resize image to WxH", [])

    @app.on_message(filters.command(["convert", "cnv"], prefixes=".") & filters.me)
    async def convert_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        fmt = args[1].lower() if len(args) > 1 else "png"
        if fmt not in ("png", "jpg", "jpeg", "webp", "bmp", "gif"):
            await message.edit("❌ Supported: png, jpg, webp, bmp, gif")
            return
        msg = await message.edit("⏳ Converting...")
        path = await message.reply_to_message.download()
        out = _tmp_path(fmt if fmt != "jpeg" else "jpg")
        try:
            img = Image.open(path)
            if fmt in ("jpg", "jpeg"):
                img = img.convert("RGB")
            img.save(out, fmt.upper() if fmt != "jpg" else "JPEG")
            await client.send_document(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "convert", "Convert image format", ["cnv"])

    @app.on_message(filters.command("rotate", prefixes=".") & filters.me)
    async def rotate_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        try:
            angle = int(args[1]) if len(args) > 1 else 90
        except ValueError:
            await message.edit("❌ Angle must be a number.")
            return
        msg = await message.edit("⏳ Rotating...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            img = img.rotate(angle, expand=True)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "rotate", "Rotate image by degrees", [])

    @app.on_message(filters.command("flip_h", prefixes=".") & filters.me)
    async def flip_h_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, _, _, _, ImageOps = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Flipping...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            img = ImageOps.mirror(img)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "flip_h", "Flip image horizontally", [])

    @app.on_message(filters.command("flip_v", prefixes=".") & filters.me)
    async def flip_v_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, _, _, _, ImageOps = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Flipping...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            img = ImageOps.flip(img)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "flip_v", "Flip image vertically", [])

    @app.on_message(filters.command(["grayscale", "grey"], prefixes=".") & filters.me)
    async def grayscale_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Converting to grayscale...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).convert("L")
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "grayscale", "Convert to grayscale", ["grey"])

    @app.on_message(filters.command("invert", prefixes=".") & filters.me)
    async def invert_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, _, _, _, ImageOps = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Inverting...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            img = ImageOps.invert(img.convert("RGB"))
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "invert", "Invert image colors", [])

    @app.on_message(filters.command("blur", prefixes=".") & filters.me)
    async def blur_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, ImageFilter, _, _, _ = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        try:
            radius = int(args[1]) if len(args) > 1 else 5
        except ValueError:
            radius = 5
        msg = await message.edit("⏳ Blurring...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).filter(ImageFilter.GaussianBlur(radius=radius))
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "blur", "Apply Gaussian blur", [])

    @app.on_message(filters.command("sharpen", prefixes=".") & filters.me)
    async def sharpen_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, ImageFilter, _, _, _ = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Sharpening...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).filter(ImageFilter.SHARPEN)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "sharpen", "Sharpen image", [])

    @app.on_message(filters.command("brightness", prefixes=".") & filters.me)
    async def brightness_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, _, ImageEnhance, _, _ = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        try:
            factor = float(args[1]) if len(args) > 1 else 1.5
        except ValueError:
            factor = 1.5
        msg = await message.edit("⏳ Adjusting brightness...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            img = ImageEnhance.Brightness(img).enhance(factor)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "brightness", "Adjust image brightness", [])

    @app.on_message(filters.command("contrast", prefixes=".") & filters.me)
    async def contrast_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, _, ImageEnhance, _, _ = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        try:
            factor = float(args[1]) if len(args) > 1 else 1.5
        except ValueError:
            factor = 1.5
        msg = await message.edit("⏳ Adjusting contrast...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            img = ImageEnhance.Contrast(img).enhance(factor)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "contrast", "Adjust image contrast", [])

    @app.on_message(filters.command("crop", prefixes=".") & filters.me)
    async def crop_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 4)
        if len(args) < 5:
            await message.edit("❌ **Usage:** `.crop <left> <top> <right> <bottom>`")
            return
        try:
            l, t, r, b = int(args[1]), int(args[2]), int(args[3]), int(args[4])
        except ValueError:
            await message.edit("❌ Invalid dimensions.")
            return
        msg = await message.edit("⏳ Cropping...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).crop((l, t, r, b))
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "crop", "Crop image with box coordinates", [])

    @app.on_message(filters.command(["thumbnail", "thumb"], prefixes=".") & filters.me)
    async def thumbnail_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        try:
            size = int(args[1]) if len(args) > 1 else 128
        except ValueError:
            size = 128
        msg = await message.edit("⏳ Creating thumbnail...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            img.thumbnail((size, size), Image.LANCZOS)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "thumbnail", "Create thumbnail", ["thumb"])

    @app.on_message(filters.command("watermark", prefixes=".") & filters.me)
    async def watermark_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, ImageDraw, _, _, ImageFont, _ = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.watermark <text>`")
            return
        text = args[1]
        msg = await message.edit("⏳ Adding watermark...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).convert("RGBA")
            overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            except Exception:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x = img.width - tw - 20
            y = img.height - th - 20
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))
            result = Image.alpha_composite(img, overlay).convert("RGB")
            result.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "watermark", "Add text watermark to image", [])

    @app.on_message(filters.command("pixelate", prefixes=".") & filters.me)
    async def pixelate_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        try:
            pixels = int(args[1]) if len(args) > 1 else 10
        except ValueError:
            pixels = 10
        msg = await message.edit("⏳ Pixelating...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            small = img.resize((img.width // pixels, img.height // pixels), Image.LANCZOS)
            result = small.resize(img.size, Image.NEAREST)
            result.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "pixelate", "Pixelate image", [])

    @app.on_message(filters.command("sepia", prefixes=".") & filters.me)
    async def sepia_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Applying sepia...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).convert("RGB")
            pixels = img.load()
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b = pixels[x, y]
                    tr = min(255, int(0.393 * r + 0.769 * g + 0.189 * b))
                    tg = min(255, int(0.349 * r + 0.686 * g + 0.168 * b))
                    tb = min(255, int(0.272 * r + 0.534 * g + 0.131 * b))
                    pixels[x, y] = (tr, tg, tb)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "sepia", "Apply sepia filter", [])

    @app.on_message(filters.command("emboss", prefixes=".") & filters.me)
    async def emboss_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, ImageFilter, _, _, _ = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Embossing...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).filter(ImageFilter.EMBOSS)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "emboss", "Apply emboss filter", [])

    @app.on_message(filters.command("edge", prefixes=".") & filters.me)
    async def edge_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, ImageFilter, _, _, _ = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Detecting edges...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).filter(ImageFilter.FIND_EDGES)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "edge", "Edge detection filter", [])

    @app.on_message(filters.command("mirror", prefixes=".") & filters.me)
    async def mirror_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, _, _, _, ImageOps = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Mirroring...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            left = img.crop((0, 0, img.width // 2, img.height))
            mirrored = ImageOps.mirror(left)
            result = Image.new(img.mode, img.size)
            result.paste(left, (0, 0))
            result.paste(mirrored, (img.width // 2, 0))
            result.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "mirror", "Mirror image left-to-right", [])

    # ═══════════════════════════════════════════════════════════════
    #  STICKER (11 commands)
    # ═══════════════════════════════════════════════════════════════

    _sticker_cache = {}

    @app.on_message(filters.command(["steal", "stealpack"], prefixes=".") & filters.me)
    async def steal_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.sticker:
            await message.edit("❌ Reply to a sticker to steal it.")
            return
        sticker = message.reply_to_message.sticker
        if not sticker.is_animated and not sticker.is_video:
            pil = _get_pil()
            if not pil:
                await message.edit("❌ Pillow not installed.")
                return
            Image = pil[0]
            msg = await message.edit("⏳ Stealing sticker...")
            path = await message.reply_to_message.download()
            out = _tmp_path("webp")
            try:
                img = Image.open(path).convert("RGBA")
                img.save(out, "WEBP")
                await client.send_sticker(message.chat.id, out)
                await msg.delete()
            except Exception as e:
                await msg.edit(f"❌ Error: `{e}`")
            finally:
                _cleanup(path, out)
        else:
            await message.edit("❌ Cannot steal animated/video stickers this way.")

    register_command("Media", "steal", "Steal a sticker", ["stealpack"])

    @app.on_message(filters.command("stealpack2", prefixes=".") & filters.me)
    async def stealpack2_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.stealpack2 <pack_link_or_name>`")
            return
        await message.edit("⚠️ stealpack2 requires manual pack operations. Use .steal for individual stickers.")

    register_command("Media", "stealpack2", "Steal entire sticker pack (manual)", [])

    @app.on_message(filters.command("kang", prefixes=".") & filters.me)
    async def kang_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.sticker:
            await message.edit("❌ Reply to a sticker to kang it.")
            return
        sticker = message.reply_to_message.sticker
        args = message.text.split(None, 1)
        emoji = args[1] if len(args) > 1 else sticker.emoji or "😀"
        msg = await message.edit("⏳ Kanging sticker...")
        try:
            path = await message.reply_to_message.download()
            await client.send_sticker(message.chat.id, path)
            await msg.edit(f"✅ **Kanged!** Emoji: {emoji}")
            _cleanup(path)
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("Media", "kang", "Kang a sticker with custom emoji", [])

    @app.on_message(filters.command("addsticker", prefixes=".") & filters.me)
    async def addsticker_cmd(client, message):
        await message.edit("⚠️ addsticker requires creating a sticker pack first. Use .createpack then add via @Stickers bot.")

    register_command("Media", "addsticker", "Add sticker to pack (via @Stickers)", [])

    @app.on_message(filters.command("delsticker", prefixes=".") & filters.me)
    async def delsticker_cmd(client, message):
        await message.edit("⚠️ Use @Stickers bot to remove stickers from your packs.")

    register_command("Media", "delsticker", "Delete sticker from pack (via @Stickers)", [])

    @app.on_message(filters.command("createpack", prefixes=".") & filters.me)
    async def createpack_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.createpack <pack_name>`")
            return
        await message.edit(f"⚠️ To create pack '{args[1]}', send /newpack to @Stickers bot and follow instructions.")

    register_command("Media", "createpack", "Create sticker pack (via @Stickers)", [])

    @app.on_message(filters.command("packinfo", prefixes=".") & filters.me)
    async def packinfo_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.sticker:
            await message.edit("❌ Reply to a sticker to get pack info.")
            return
        sticker = message.reply_to_message.sticker
        text = f"🏷 **Sticker Info**\n\n"
        text += f"🆔 **File ID:** `{sticker.file_id}`\n"
        text += f"📐 **Dimensions:** `{sticker.width}x{sticker.height}`\n"
        text += f"😀 **Emoji:** {sticker.emoji or 'N/A'}\n"
        text += f"📦 **Set Name:** `{sticker.set_name or 'N/A'}`\n"
        text += f"🎭 **Animated:** `{sticker.is_animated}`\n"
        text += f"🎬 **Video:** `{sticker.is_video}`\n"
        text += f"📁 **File Size:** `{sticker.file_size or 'N/A'}`\n"
        if sticker.set_name:
            try:
                pack = await client.get_sticker_set(sticker.set_name)
                text += f"\n📦 **Pack:** {pack.title}\n"
                text += f"📊 **Stickers in pack:** `{pack.count}`\n"
                text += f"🆔 **Short name:** `{pack.short_name}`\n"
            except Exception:
                pass
        await message.edit(text)

    register_command("Media", "packinfo", "Get sticker pack info", [])

    @app.on_message(filters.command("getsticker", prefixes=".") & filters.me)
    async def getsticker_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.sticker:
            await message.edit("❌ Reply to a sticker.")
            return
        msg = await message.edit("⏳ Downloading sticker...")
        try:
            path = await message.reply_to_message.download()
            await client.send_document(message.chat.id, path)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            try:
                if path and os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass

    register_command("Media", "getsticker", "Download sticker as file", [])

    @app.on_message(filters.command("stealemoji", prefixes=".") & filters.me)
    async def stealemoji_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.stealemoji <emoji>`")
            return
        await message.edit(f"⚠️ Custom emoji stealing requires premium. Emoji: {args[1]}")

    register_command("Media", "stealemoji", "Steal custom emoji (requires premium)", [])

    @app.on_message(filters.command("stickerid", prefixes=".") & filters.me)
    async def stickerid_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.sticker:
            await message.edit("❌ Reply to a sticker.")
            return
        sticker = message.reply_to_message.sticker
        await message.edit(f"🆔 **Sticker File ID:**\n`{sticker.file_id}`")

    register_command("Media", "stickerid", "Get sticker file ID", [])

    @app.on_message(filters.command("sticache", prefixes=".") & filters.me)
    async def sticache_cmd(client, message):
        _sticker_cache.clear()
        await message.edit("🧹 **Sticker cache cleared!**")

    register_command("Media", "sticache", "Clear sticker cache", [])

    # ═══════════════════════════════════════════════════════════════
    #  SCREEN (8 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command(["screenshot", "ss"], prefixes=".") & filters.me)
    async def screenshot_cmd(client, message):
        await message.edit("⚠️ Screenshot requires running on a device with display.")

    register_command("Media", "screenshot", "Take screenshot (requires display)", ["ss"])

    @app.on_message(filters.command("takeshot", prefixes=".") & filters.me)
    async def takeshot_cmd(client, message):
        await message.edit("⚠️ Takeshot requires running on a device with display.")

    register_command("Media", "takeshot", "Take screenshot (alternate)", [])

    @app.on_message(filters.command("webss", prefixes=".") & filters.me)
    async def webss_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.webss <url>`")
            return
        url = args[1]
        await message.edit(f"⚠️ Web screenshot requires a headless browser. URL: `{url}`")

    register_command("Media", "webss", "Take website screenshot (requires browser)", [])

    @app.on_message(filters.command("gif", prefixes=".") & filters.me)
    async def gif_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo to make GIF.")
            return
        msg = await message.edit("⏳ Creating GIF...")
        path = await message.reply_to_message.download()
        out = _tmp_path("gif")
        try:
            img = Image.open(path)
            frames = []
            for i in range(10):
                angle = i * 36
                rotated = img.rotate(angle, expand=True)
                frames.append(rotated.copy().convert("RGBA").resize((256, 256), Image.LANCZOS))
            frames[0].save(out, save_all=True, append_images=frames[1:], duration=100, loop=0)
            await client.send_animation(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "gif", "Create simple GIF from photo", [])

    @app.on_message(filters.command("tovideo", prefixes=".") & filters.me)
    async def tovideo_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a GIF or video note.")
            return
        r = message.reply_to_message
        if not (r.animation or r.video_note or r.video):
            await message.edit("❌ Reply to a GIF or video note.")
            return
        msg = await message.edit("⏳ Converting to video...")
        try:
            path = await r.download()
            out = _tmp_path("mp4")
            if r.animation:
                proc = subprocess.run(
                    ["ffmpeg", "-y", "-i", path, "-c:v", "libx264", "-movflags", "+faststart", out],
                    capture_output=True, timeout=60
                )
                if proc.returncode == 0 and os.path.exists(out):
                    await client.send_video(message.chat.id, out)
                    await msg.delete()
                else:
                    await msg.edit("❌ FFmpeg conversion failed.")
            else:
                await client.send_video(message.chat.id, path)
                await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out if 'out' in dir() else None)

    register_command("Media", "tovideo", "Convert GIF to video", [])

    @app.on_message(filters.command("roundvideo", prefixes=".") & filters.me)
    async def roundvideo_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.video:
            await message.edit("❌ Reply to a video.")
            return
        msg = await message.edit("⏳ Creating round video...")
        try:
            path = await message.reply_to_message.download()
            out = _tmp_path("mp4")
            proc = subprocess.run(
                ["ffmpeg", "-y", "-i", path, "-c:v", "libx264",
                 "-vf", "crop=min(iw\\,ih):min(iw\\,ih),scale=320:320",
                 "-c:a", "aac", "-movflags", "+faststart", out],
                capture_output=True, timeout=60
            )
            if proc.returncode == 0 and os.path.exists(out):
                await client.send_video_note(message.chat.id, out)
                await msg.delete()
            else:
                await msg.edit("❌ FFmpeg conversion failed.")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out if 'out' in dir() else None)

    register_command("Media", "roundvideo", "Convert video to round video note", [])

    @app.on_message(filters.command("voice", prefixes=".") & filters.me)
    async def voice_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.audio and not message.reply_to_message.video and not message.reply_to_message.voice:
            await message.edit("❌ Reply to audio/video/voice.")
            return
        msg = await message.edit("⏳ Converting to voice...")
        try:
            path = await message.reply_to_message.download()
            out = _tmp_path("ogg")
            proc = subprocess.run(
                ["ffmpeg", "-y", "-i", path, "-c:a", "libopus", out],
                capture_output=True, timeout=60
            )
            if proc.returncode == 0 and os.path.exists(out):
                await client.send_voice(message.chat.id, out)
                await msg.delete()
            else:
                await msg.edit("❌ FFmpeg conversion failed.")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out if 'out' in dir() else None)

    register_command("Media", "voice", "Convert to voice message", [])

    @app.on_message(filters.command("audio", prefixes=".") & filters.me)
    async def audio_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.video and not message.reply_to_message.voice:
            await message.edit("❌ Reply to video/voice.")
            return
        msg = await message.edit("⏳ Extracting audio...")
        try:
            path = await message.reply_to_message.download()
            out = _tmp_path("mp3")
            proc = subprocess.run(
                ["ffmpeg", "-y", "-i", path, "-vn", "-c:a", "libmp3lame", "-q:a", "2", out],
                capture_output=True, timeout=60
            )
            if proc.returncode == 0 and os.path.exists(out):
                await client.send_audio(message.chat.id, out)
                await msg.delete()
            else:
                await msg.edit("❌ FFmpeg conversion failed.")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out if 'out' in dir() else None)

    register_command("Media", "audio", "Extract audio as MP3", [])

    # ═══════════════════════════════════════════════════════════════
    #  DOWNLOAD (8 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command(["download", "dl"], prefixes=".") & filters.me)
    async def download_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a media message.")
            return
        r = message.reply_to_message
        if not (r.photo or r.video or r.audio or r.document or r.voice or r.sticker or r.animation):
            await message.edit("❌ No downloadable media found.")
            return
        msg = await message.edit("⏳ Downloading...")
        try:
            path = await r.download()
            await msg.edit(f"✅ **Downloaded:** `{path}`")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("Media", "download", "Download media from reply", ["dl"])

    @app.on_message(filters.command(["upload", "ul"], prefixes=".") & filters.me)
    async def upload_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.upload <file_path>`")
            return
        file_path = args[1].strip()
        if not os.path.exists(file_path):
            await message.edit(f"❌ File not found: `{file_path}`")
            return
        msg = await message.edit("⏳ Uploading...")
        try:
            await client.send_document(message.chat.id, file_path)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("Media", "upload", "Upload a local file", ["ul"])

    @app.on_message(filters.command("savemedia", prefixes=".") & filters.me)
    async def savemedia_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a media message.")
            return
        r = message.reply_to_message
        msg = await message.edit("⏳ Saving to Saved Messages...")
        try:
            await r.copy("me")
            await msg.edit("✅ **Saved to Saved Messages!**")
        except FloodWait as e:
            await asyncio.sleep(e.value + 1)
            await r.copy("me")
            await msg.edit("✅ **Saved to Saved Messages!**")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("Media", "savemedia", "Save media to Saved Messages", [])

    @app.on_message(filters.command("extract_frames", prefixes=".") & filters.me)
    async def extract_frames_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.video:
            await message.edit("❌ Reply to a video.")
            return
        args = message.text.split(None, 1)
        try:
            fps = int(args[1]) if len(args) > 1 else 1
        except ValueError:
            fps = 1
        msg = await message.edit("⏳ Extracting frames...")
        try:
            path = await message.reply_to_message.download()
            frame_dir = os.path.join(_TMP, f"kyrenub_frames_{random.randint(10000,99999)}")
            os.makedirs(frame_dir, exist_ok=True)
            proc = subprocess.run(
                ["ffmpeg", "-y", "-i", path, "-vf", f"fps={fps}",
                 os.path.join(frame_dir, "frame_%04d.png")],
                capture_output=True, timeout=120
            )
            frames = sorted(os.listdir(frame_dir))[:5]
            if frames:
                for f in frames:
                    fpath = os.path.join(frame_dir, f)
                    await client.send_photo(message.chat.id, fpath)
                await msg.edit(f"✅ Extracted {len(frames)} frames (showing first 5).")
            else:
                await msg.edit("❌ No frames extracted.")
            shutil.rmtree(frame_dir, ignore_errors=True)
            _cleanup(path)
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("Media", "extract_frames", "Extract frames from video", [])

    @app.on_message(filters.command("extract_audio", prefixes=".") & filters.me)
    async def extract_audio_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.video:
            await message.edit("❌ Reply to a video.")
            return
        msg = await message.edit("⏳ Extracting audio...")
        try:
            path = await message.reply_to_message.download()
            out = _tmp_path("mp3")
            proc = subprocess.run(
                ["ffmpeg", "-y", "-i", path, "-vn", "-c:a", "libmp3lame", out],
                capture_output=True, timeout=60
            )
            if proc.returncode == 0 and os.path.exists(out):
                await client.send_audio(message.chat.id, out)
                await msg.delete()
            else:
                await msg.edit("❌ FFmpeg failed.")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out if 'out' in dir() else None)

    register_command("Media", "extract_audio", "Extract audio from video", [])

    @app.on_message(filters.command("mediainfo", prefixes=".") & filters.me)
    async def mediainfo_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a media message.")
            return
        r = message.reply_to_message
        text = "📎 **Media Info**\n\n"
        if r.photo:
            p = r.photo
            text += f"📷 **Type:** Photo\n"
            text += f"📅 **Date:** `{p.date}`\n"
            text += f"📐 **Size:** `{p.width}x{p.height}`\n"
            text += f"🆔 **File ID:** `{p.file_id[:40]}...`\n"
            text += f"📁 **File Size:** `{p.file_size or 'N/A'}`\n"
        elif r.video:
            v = r.video
            text += f"🎬 **Type:** Video\n"
            text += f"📐 **Size:** `{v.width}x{v.height}`\n"
            text += f"⏱ **Duration:** `{v.duration}s`\n"
            text += f"📁 **File Size:** `{v.file_size or 'N/A'}`\n"
            text += f"🏷 **Mime:** `{v.mime_type or 'N/A'}`\n"
        elif r.audio:
            a = r.audio
            text += f"🎵 **Type:** Audio\n"
            text += f"⏱ **Duration:** `{a.duration}s`\n"
            text += f"🎵 **Title:** `{a.title or 'N/A'}`\n"
            text += f"🎤 **Performer:** `{a.performer or 'N/A'}`\n"
            text += f"📁 **File Size:** `{a.file_size or 'N/A'}`\n"
        elif r.document:
            d = r.document
            text += f"📄 **Type:** Document\n"
            text += f"🏷 **Mime:** `{d.mime_type or 'N/A'}`\n"
            text += f"📁 **File Size:** `{d.file_size or 'N/A'}`\n"
            if d.file_name:
                text += f"📝 **Name:** `{d.file_name}`\n"
        elif r.sticker:
            s = r.sticker
            text += f"🏷 **Type:** Sticker\n"
            text += f"📐 **Size:** `{s.width}x{s.height}`\n"
            text += f"😀 **Emoji:** `{s.emoji or 'N/A'}`\n"
        elif r.animation:
            a = r.animation
            text += f"🎞 **Type:** GIF/Animation\n"
            text += f"📐 **Size:** `{a.width}x{a.height}`\n"
            text += f"⏱ **Duration:** `{a.duration}s`\n"
        elif r.voice:
            v = r.voice
            text += f"🎙 **Type:** Voice\n"
            text += f"⏱ **Duration:** `{v.duration}s`\n"
        else:
            text += "❓ Unknown media type\n"
        await message.edit(text)

    register_command("Media", "mediainfo", "Get detailed media info", [])

    @app.on_message(filters.command("fileinfo", prefixes=".") & filters.me)
    async def fileinfo_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.document:
            await message.edit("❌ Reply to a document.")
            return
        d = message.reply_to_message.document
        text = f"📄 **File Info**\n\n"
        text += f"📝 **Name:** `{d.file_name or 'N/A'}`\n"
        text += f"🏷 **Mime:** `{d.mime_type or 'N/A'}`\n"
        text += f"📁 **Size:** `{d.file_size or 'N/A'}` bytes\n"
        text += f"📅 **Date:** `{d.date or 'N/A'}`\n"
        text += f"🆔 **File ID:** `{d.file_id[:50]}...`\n"
        await message.edit(text)

    register_command("Media", "fileinfo", "Get document file info", [])

    @app.on_message(filters.command("metainfo", prefixes=".") & filters.me)
    async def metainfo_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message.")
            return
        r = message.reply_to_message
        text = "📋 **Message Meta Info**\n\n"
        text += f"🆔 **ID:** `{r.id}`\n"
        text += f"📅 **Date:** `{r.date}`\n"
        if r.from_user:
            text += f"👤 **From:** `{r.from_user.id}`\n"
        text += f"💬 **Chat:** `{r.chat.id}`\n"
        if r.forward_from:
            text += f"↗️ **Forward from:** `{r.forward_from.id}`\n"
        if r.reply_to_message:
            text += f"↩️ **Reply to:** `{r.reply_to_message.id}`\n"
        if r.media:
            text += f"📎 **Media:** `{type(r.media).__name__}`\n"
        if r.views:
            text += f"👁 **Views:** `{r.views}`\n"
        if r.edit_date:
            text += f"✏️ **Edited:** `{r.edit_date}`\n"
        await message.edit(text)

    register_command("Media", "metainfo", "Get message metadata info", [])

    # ═══════════════════════════════════════════════════════════════
    #  UTILS (11 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("sticker2img", prefixes=".") & filters.me)
    async def sticker2img_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.sticker:
            await message.edit("❌ Reply to a sticker.")
            return
        msg = await message.edit("⏳ Converting sticker to image...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).convert("RGBA")
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            bg.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "sticker2img", "Convert sticker to image", [])

    @app.on_message(filters.command("img2sticker", prefixes=".") & filters.me)
    async def img2sticker_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Converting image to sticker...")
        path = await message.reply_to_message.download()
        out = _tmp_path("webp")
        try:
            img = Image.open(path).convert("RGBA")
            img = img.resize((512, 512), Image.LANCZOS)
            img.save(out, "WEBP")
            await client.send_sticker(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "img2sticker", "Convert image to sticker", [])

    @app.on_message(filters.command("video2audio", prefixes=".") & filters.me)
    async def video2audio_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.video:
            await message.edit("❌ Reply to a video.")
            return
        msg = await message.edit("⏳ Extracting audio from video...")
        try:
            path = await message.reply_to_message.download()
            out = _tmp_path("mp3")
            proc = subprocess.run(
                ["ffmpeg", "-y", "-i", path, "-vn", "-c:a", "libmp3lame", out],
                capture_output=True, timeout=60
            )
            if proc.returncode == 0 and os.path.exists(out):
                await client.send_audio(message.chat.id, out)
                await msg.delete()
            else:
                await msg.edit("❌ FFmpeg failed.")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out if 'out' in dir() else None)

    register_command("Media", "video2audio", "Extract audio from video", [])

    @app.on_message(filters.command("compress", prefixes=".") & filters.me)
    async def compress_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        try:
            quality = int(args[1]) if len(args) > 1 else 50
        except ValueError:
            quality = 50
        msg = await message.edit("⏳ Compressing...")
        path = await message.reply_to_message.download()
        out = _tmp_path("jpg")
        try:
            img = Image.open(path).convert("RGB")
            img.save(out, "JPEG", quality=quality, optimize=True)
            orig_size = os.path.getsize(path)
            comp_size = os.path.getsize(out)
            ratio = (1 - comp_size / orig_size) * 100
            await client.send_photo(message.chat.id, out,
                caption=f"📏 Original: `{orig_size}` bytes\n📏 Compressed: `{comp_size}` bytes\n📉 Reduced: `{ratio:.1f}%`")
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "compress", "Compress image with quality", [])

    @app.on_message(filters.command("zoom", prefixes=".") & filters.me)
    async def zoom_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        try:
            factor = float(args[1]) if len(args) > 1 else 2.0
        except ValueError:
            factor = 2.0
        msg = await message.edit("⏳ Zooming...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path)
            w, h = img.size
            cx, cy = w // 2, h // 2
            crop_w, crop_h = int(w / factor), int(h / factor)
            img = img.crop((cx - crop_w // 2, cy - crop_h // 2,
                           cx + crop_w // 2, cy + crop_h // 2))
            img = img.resize((w, h), Image.LANCZOS)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "zoom", "Zoom into center of image", [])

    @app.on_message(filters.command("ascii_image", prefixes=".") & filters.me)
    async def ascii_image_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Creating ASCII art...")
        path = await message.reply_to_message.download()
        try:
            img = Image.open(path).convert("L")
            img = img.resize((80, 40))
            chars = "@%#*+=-:. "
            pixels = list(img.getdata())
            ascii_art = ""
            for i, p in enumerate(pixels):
                if i % 80 == 0 and i > 0:
                    ascii_art += "\n"
                ascii_art += chars[p * (len(chars) - 1) // 255]
            await msg.edit(f"```\n{ascii_art}\n```")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path)

    register_command("Media", "ascii_image", "Convert image to ASCII art", [])

    @app.on_message(filters.command("colorize", prefixes=".") & filters.me)
    async def colorize_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, _, _, ImageEnhance, _, _ = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Colorizing...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).convert("RGB")
            img = ImageEnhance.Color(img).enhance(2.0)
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "colorize", "Enhance colors in image", [])

    @app.on_message(filters.command("collage", prefixes=".") & filters.me)
    async def collage_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image = pil[0]
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        msg = await message.edit("⏳ Creating collage...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).convert("RGB")
            w, h = img.size
            hw, hh = w // 2, h // 2
            tl = img.crop((0, 0, hw, hh))
            tr = img.crop((hw, 0, w, hh))
            bl = img.crop((0, hh, hw, h))
            br = img.crop((hw, hh, w, h))
            collage = Image.new("RGB", (w, h))
            collage.paste(tl.resize((hw, hh)), (0, 0))
            collage.paste(tr.resize((hw, hh)).rotate(90), (hw, 0))
            collage.paste(bl.resize((hw, hh)).rotate(180), (0, hh))
            collage.paste(br.resize((hw, hh)).rotate(270), (hw, hh))
            collage.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "collage", "Create 4-panel collage", [])

    @app.on_message(filters.command("meme", prefixes=".") & filters.me)
    async def meme_cmd(client, message):
        pil = _get_pil()
        if not pil:
            await message.edit("❌ Pillow not installed.")
            return
        Image, ImageDraw, _, _, ImageFont, _ = pil
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 2)
        top = args[1].upper() if len(args) > 1 else "TOP TEXT"
        bottom = args[2].upper() if len(args) > 2 else "BOTTOM TEXT"
        msg = await message.edit("⏳ Creating meme...")
        path = await message.reply_to_message.download()
        out = _tmp_path()
        try:
            img = Image.open(path).convert("RGB")
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
            except Exception:
                font = ImageFont.load_default()
            # Top text
            bbox = draw.textbbox((0, 0), top, font=font)
            tw = bbox[2] - bbox[0]
            draw.text(((img.width - tw) // 2, 10), top, fill="white", font=font,
                      stroke_width=2, stroke_fill="black")
            # Bottom text
            bbox = draw.textbbox((0, 0), bottom, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((img.width - tw) // 2, img.height - th - 10), bottom, fill="white",
                      font=font, stroke_width=2, stroke_fill="black")
            img.save(out, "PNG")
            await client.send_photo(message.chat.id, out)
            await msg.delete()
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")
        finally:
            _cleanup(path, out)

    register_command("Media", "meme", "Add meme text to image", [])

    @app.on_message(filters.command(["caption2", "changecaption"], prefixes=".") & filters.me)
    async def caption2_cmd(client, message):
        if not message.reply_to_message:
            await message.edit("❌ Reply to a message.")
            return
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.caption2 <new caption>`")
            return
        new_caption = args[1]
        r = message.reply_to_message
        if not r.media:
            await message.edit("❌ Replied message has no media to recaption.")
            return
        msg = await message.edit("⏳ Changing caption...")
        try:
            path = await r.download()
            if r.photo:
                await client.send_photo(message.chat.id, path, caption=new_caption)
            elif r.video:
                await client.send_video(message.chat.id, path, caption=new_caption)
            elif r.audio:
                await client.send_audio(message.chat.id, path, caption=new_caption)
            elif r.document:
                await client.send_document(message.chat.id, path, caption=new_caption)
            elif r.animation:
                await client.send_animation(message.chat.id, path, caption=new_caption)
            else:
                await msg.edit("❌ Unsupported media type.")
                _cleanup(path)
                return
            await msg.delete()
            _cleanup(path)
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("Media", "caption2", "Change media caption", ["changecaption"])

    @app.on_message(filters.command(["spam_pic", "picspam"], prefixes=".") & filters.me)
    async def spam_pic_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.edit("❌ Reply to a photo.")
            return
        args = message.text.split(None, 1)
        try:
            count = int(args[1]) if len(args) > 1 else 5
        except ValueError:
            count = 5
        if count > 50:
            await message.edit("❌ Max 50.")
            return
        photo_id = message.reply_to_message.photo.file_id
        await message.delete()
        for _ in range(count):
            try:
                await client.send_photo(message.chat.id, photo_id)
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await client.send_photo(message.chat.id, photo_id)
            await asyncio.sleep(0.3)

    register_command("Media", "spam_pic", "Spam a photo N times", ["picspam"])
