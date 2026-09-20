"""
KyrenUB - Tools Plugin
=======================
119 commands for calculations, encoding, hashing, string ops, networking, and more.
Categories: Calculators(21), Encoders(20), Hash(12), String(21), Network(10),
            Misc(18), Codes(9), Other(8)
"""


def register(app):
    from pyrogram import filters
    from plugins import register_command
    import hashlib
    import base64
    import urllib.parse
    import html
    import json
    import re
    import math
    import random
    import string
    import struct
    import socket
    import uuid as _uuid
    import time
    import asyncio
    import os
    from datetime import datetime, timezone

    # ═══════════════════════════════════════════════════════════════
    #  SHARED HELPERS
    # ═══════════════════════════════════════════════════════════════

    _MORSE = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
        "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
        "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
        "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
        "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
        "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
        "3": "...--", "4": "....-", "5": ".....", "6": "-....",
        "7": "--...", "8": "---..", "9": "----.", " ": "/",
        ".": ".-.-.-", ",": "--..--", "?": "..--..", "!": "-.-.--",
    }
    _MORSE_REV = {v: k for k, v in _MORSE.items()}

    _ROMAN_MAP = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]

    def _int_to_roman(n):
        if not 1 <= n <= 3999:
            return None
        result = ""
        for val, sym in _ROMAN_MAP:
            while n >= val:
                result += sym
                n -= val
        return result

    def _roman_to_int(s):
        vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        total = 0
        prev = 0
        for ch in reversed(s.upper()):
            if ch not in vals:
                return None
            v = vals[ch]
            if v < prev:
                total -= v
            else:
                total += v
            prev = v
        return total

    _MATH_CONSTANTS = {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
        "phi": (1 + math.sqrt(5)) / 2,
        "sqrt2": math.sqrt(2),
        "sqrt3": math.sqrt(3),
        "ln2": math.log(2),
        "ln10": math.log(10),
        "euler_gamma": 0.5772156649015329,
        "inf": float("inf"),
    }

    # ═══════════════════════════════════════════════════════════════
    #  CALCULATORS (21 commands)
    # ═══════════════════════════════════════════════════════════════

    # 1. CALC / EVALUATE
    @app.on_message(filters.command(["calc", "evaluate"], prefixes=".") & filters.me)
    async def calc_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.calc <expression>`\nExample: `.calc 2+3*4`")
            return
        expr = args[1].strip()
        allowed = set("0123456789+-*/.()% ^")
        safe_expr = expr.replace("^", "**")
        if not all(c in allowed for c in safe_expr):
            await message.edit("❌ Only numbers and + - * / ^ % ( ) allowed.")
            return
        try:
            result = eval(safe_expr, {"__builtins__": {}}, {"math": math})
            await message.edit(f"🧮 **{expr}** = `{result}`")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "calc", "Evaluate a math expression", ["evaluate"])

    # 2. SQRT
    @app.on_message(filters.command("sqrt", prefixes=".") & filters.me)
    async def sqrt_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.sqrt <number>`")
            return
        try:
            n = float(args[1])
            if n < 0:
                await message.edit(f"🧮 √({n}) = `{complex(n) ** 0.5}`")
            else:
                await message.edit(f"🧮 √{n} = `{math.sqrt(n)}`")
        except ValueError:
            await message.edit("❌ Invalid number.")

    register_command("Tools", "sqrt", "Calculate square root", [])

    # 3. POWER / POW
    @app.on_message(filters.command(["power", "pow"], prefixes=".") & filters.me)
    async def power_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.power <base> <exponent>`")
            return
        try:
            base = float(args[1])
            exp = float(args[2])
            result = base ** exp
            await message.edit(f"🧮 {base}^{exp} = `{result}`")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "power", "Calculate power/exponent", ["pow"])

    # 4. PERCENTAGE / PCT
    @app.on_message(filters.command(["percentage", "pct"], prefixes=".") & filters.me)
    async def percentage_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.pct <value> <total>`\nExample: `.pct 25 200`")
            return
        try:
            val = float(args[1])
            total = float(args[2])
            if total == 0:
                await message.edit("❌ Total cannot be zero.")
                return
            result = (val / total) * 100
            await message.edit(f"🧮 {val} is `{result:.2f}%` of {total}")
        except ValueError:
            await message.edit("❌ Invalid numbers.")

    register_command("Tools", "percentage", "Calculate percentage", ["pct"])

    # 5. BMI
    @app.on_message(filters.command("bmi", prefixes=".") & filters.me)
    async def bmi_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.bmi <weight_kg> <height_m>`\nExample: `.bmi 70 1.75`")
            return
        try:
            weight = float(args[1])
            height = float(args[2])
            if height <= 0:
                await message.edit("❌ Height must be positive.")
                return
            bmi = weight / (height ** 2)
            if bmi < 18.5:
                cat = "Underweight"
            elif bmi < 25:
                cat = "Normal"
            elif bmi < 30:
                cat = "Overweight"
            else:
                cat = "Obese"
            await message.edit(f"🧮 **BMI:** `{bmi:.1f}` — **{cat}**")
        except ValueError:
            await message.edit("❌ Invalid numbers.")

    register_command("Tools", "bmi", "Calculate Body Mass Index", [])

    # 6. TIP
    @app.on_message(filters.command("tip", prefixes=".") & filters.me)
    async def tip_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.tip <amount> [percent]`\nDefault tip: 15%")
            return
        try:
            amount = float(args[1])
            pct = float(args[2]) if len(args) > 2 else 15.0
            tip_amt = amount * pct / 100
            total = amount + tip_amt
            await message.edit(
                f"🧮 **Tip Calculator**\n\n"
                f"💰 Bill: `${amount:.2f}`\n"
                f"📊 Tip ({pct}%): `${tip_amt:.2f}`\n"
                f"💵 Total: `${total:.2f}`"
            )
        except ValueError:
            await message.edit("❌ Invalid numbers.")

    register_command("Tools", "tip", "Calculate tip amount", [])

    # 7. DISCOUNT
    @app.on_message(filters.command("discount", prefixes=".") & filters.me)
    async def discount_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.discount <price> <discount_percent>`")
            return
        try:
            price = float(args[1])
            disc = float(args[2])
            saved = price * disc / 100
            final = price - saved
            await message.edit(
                f"🧮 **Discount Calculator**\n\n"
                f"🏷 Original: `${price:.2f}`\n"
                f"📉 Discount ({disc}%): `-${saved:.2f}`\n"
                f"💰 Final: `${final:.2f}`"
            )
        except ValueError:
            await message.edit("❌ Invalid numbers.")

    register_command("Tools", "discount", "Calculate discounted price", [])

    # 8. CONVERT / CNV
    @app.on_message(filters.command(["convert", "cnv"], prefixes=".") & filters.me)
    async def convert_cmd(client, message):
        _conversions = {
            "km_mi": lambda v: v * 0.621371,
            "mi_km": lambda v: v * 1.60934,
            "kg_lb": lambda v: v * 2.20462,
            "lb_kg": lambda v: v * 0.453592,
            "c_f": lambda v: v * 9/5 + 32,
            "f_c": lambda v: (v - 32) * 5/9,
            "cm_in": lambda v: v * 0.393701,
            "in_cm": lambda v: v * 2.54,
            "m_ft": lambda v: v * 3.28084,
            "ft_m": lambda v: v * 0.3048,
            "l_gal": lambda v: v * 0.264172,
            "gal_l": lambda v: v * 3.78541,
            "mb_gb": lambda v: v / 1024,
            "gb_mb": lambda v: v * 1024,
            "kb_mb": lambda v: v / 1024,
            "mb_kb": lambda v: v * 1024,
        }
        args = message.text.split(None, 3)
        if len(args) < 3:
            await message.edit(
                "❌ **Usage:** `.cnv <value> <type>`\n"
                "Types: km_mi, mi_km, kg_lb, lb_kg, c_f, f_c, "
                "cm_in, in_cm, m_ft, ft_m, l_gal, gal_l, "
                "mb_gb, gb_mb, kb_mb, mb_kb"
            )
            return
        try:
            val = float(args[1])
            conv_type = args[2].lower()
            if conv_type not in _conversions:
                await message.edit(f"❌ Unknown conversion: `{conv_type}`")
                return
            result = _conversions[conv_type](val)
            await message.edit(f"🔄 `{val}` {conv_type.split('_')[0]} → `{result:.6g}` {conv_type.split('_')[1]}")
        except ValueError:
            await message.edit("❌ Invalid number.")

    register_command("Tools", "convert", "Unit conversions", ["cnv"])

    # 9. CURRENCY (mock - no API)
    @app.on_message(filters.command("currency", prefixes=".") & filters.me)
    async def currency_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.currency <amount> <from_to>`\nExample: `.currency 100 usd_eur`")
            return
        try:
            amount = float(args[1])
            pair = args[2].lower()
            _mock_rates = {
                "usd_eur": 0.92, "eur_usd": 1.09, "usd_gbp": 0.79, "gbp_usd": 1.27,
                "usd_jpy": 149.5, "jpy_usd": 0.0067, "usd_cad": 1.36, "cad_usd": 0.74,
                "usd_aud": 1.53, "aud_usd": 0.65, "eur_gbp": 0.86, "gbp_eur": 1.16,
                "usd_inr": 83.0, "inr_usd": 0.012, "usd_cny": 7.24, "cny_usd": 0.14,
            }
            if pair not in _mock_rates:
                await message.edit(f"❌ Unknown pair. Available: {', '.join(_mock_rates.keys())}")
                return
            result = amount * _mock_rates[pair]
            fr, to = pair.split("_")
            await message.edit(f"💱 `{amount:.2f}` {fr.upper()} ≈ `{result:.2f}` {to.upper()}\n_⚠️ Mock rates for demo only_")
        except (ValueError, IndexError):
            await message.edit("❌ Invalid input.")

    register_command("Tools", "currency", "Currency conversion (mock rates)", [])

    # 10. HEX2DEC
    @app.on_message(filters.command("hex2dec", prefixes=".") & filters.me)
    async def hex2dec_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.hex2dec <hex>`\nExample: `.hex2dec FF`")
            return
        try:
            result = int(args[1].strip(), 16)
            await message.edit(f"🔄 `0x{args[1].strip().upper()}` → `{result}`")
        except ValueError:
            await message.edit("❌ Invalid hex value.")

    register_command("Tools", "hex2dec", "Convert hex to decimal", [])

    # 11. DEC2HEX
    @app.on_message(filters.command("dec2hex", prefixes=".") & filters.me)
    async def dec2hex_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.dec2hex <decimal>`")
            return
        try:
            n = int(args[1])
            await message.edit(f"🔄 `{n}` → `0x{n:X}`")
        except ValueError:
            await message.edit("❌ Invalid decimal number.")

    register_command("Tools", "dec2hex", "Convert decimal to hex", [])

    # 12. BIN2DEC
    @app.on_message(filters.command("bin2dec", prefixes=".") & filters.me)
    async def bin2dec_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.bin2dec <binary>`\nExample: `.bin2dec 1010`")
            return
        try:
            result = int(args[1].strip(), 2)
            await message.edit(f"🔄 `0b{args[1].strip()}` → `{result}`")
        except ValueError:
            await message.edit("❌ Invalid binary value.")

    register_command("Tools", "bin2dec", "Convert binary to decimal", [])

    # 13. DEC2BIN
    @app.on_message(filters.command("dec2bin", prefixes=".") & filters.me)
    async def dec2bin_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.dec2bin <decimal>`")
            return
        try:
            n = int(args[1])
            await message.edit(f"🔄 `{n}` → `0b{bin(n)[2:]}`")
        except ValueError:
            await message.edit("❌ Invalid decimal number.")

    register_command("Tools", "dec2bin", "Convert decimal to binary", [])

    # 14. OCT2DEC
    @app.on_message(filters.command("oct2dec", prefixes=".") & filters.me)
    async def oct2dec_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.oct2dec <octal>`")
            return
        try:
            result = int(args[1].strip(), 8)
            await message.edit(f"🔄 `0o{args[1].strip()}` → `{result}`")
        except ValueError:
            await message.edit("❌ Invalid octal value.")

    register_command("Tools", "oct2dec", "Convert octal to decimal", [])

    # 15. DEC2OCT
    @app.on_message(filters.command("dec2oct", prefixes=".") & filters.me)
    async def dec2oct_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.dec2oct <decimal>`")
            return
        try:
            n = int(args[1])
            await message.edit(f"🔄 `{n}` → `0o{oct(n)[2:]}`")
        except ValueError:
            await message.edit("❌ Invalid decimal number.")

    register_command("Tools", "dec2oct", "Convert decimal to octal", [])

    # 16. ROMAN
    @app.on_message(filters.command("roman", prefixes=".") & filters.me)
    async def roman_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.roman <1-3999>`")
            return
        try:
            n = int(args[1])
            result = _int_to_roman(n)
            if result is None:
                await message.edit("❌ Number must be 1-3999.")
                return
            await message.edit(f"🔄 `{n}` → `{result}`")
        except ValueError:
            await message.edit("❌ Invalid number.")

    register_command("Tools", "roman", "Convert number to Roman numeral", [])

    # 17. ROMAN2INT
    @app.on_message(filters.command("roman2int", prefixes=".") & filters.me)
    async def roman2int_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.roman2int <XIV>`")
            return
        result = _roman_to_int(args[1].strip())
        if result is None:
            await message.edit("❌ Invalid Roman numeral.")
            return
        await message.edit(f"🔄 `{args[1].strip().upper()}` → `{result}`")

    register_command("Tools", "roman2int", "Convert Roman numeral to integer", [])

    # 18. FACTORIAL
    @app.on_message(filters.command("factorial", prefixes=".") & filters.me)
    async def factorial_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.factorial <n>` (0 ≤ n ≤ 170)")
            return
        try:
            n = int(args[1])
            if n < 0 or n > 170:
                await message.edit("❌ n must be between 0 and 170.")
                return
            await message.edit(f"🧮 {n}! = `{math.factorial(n)}`")
        except ValueError:
            await message.edit("❌ Invalid number.")

    register_command("Tools", "factorial", "Calculate factorial", [])

    # 19. GCD
    @app.on_message(filters.command("gcd", prefixes=".") & filters.me)
    async def gcd_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.gcd <a> <b>`")
            return
        try:
            a, b = int(args[1]), int(args[2])
            await message.edit(f"🧮 GCD({a}, {b}) = `{math.gcd(a, b)}`")
        except ValueError:
            await message.edit("❌ Invalid numbers.")

    register_command("Tools", "gcd", "Calculate greatest common divisor", [])

    # 20. LCM
    @app.on_message(filters.command("lcm", prefixes=".") & filters.me)
    async def lcm_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.lcm <a> <b>`")
            return
        try:
            a, b = int(args[1]), int(args[2])
            result = abs(a * b) // math.gcd(a, b) if a and b else 0
            await message.edit(f"🧮 LCM({a}, {b}) = `{result}`")
        except ValueError:
            await message.edit("❌ Invalid numbers.")

    register_command("Tools", "lcm", "Calculate least common multiple", [])

    # 21. (extra calc: LOG)
    @app.on_message(filters.command("log", prefixes=".") & filters.me)
    async def log_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.log <value> [base]`\nDefault base: e (natural log)")
            return
        try:
            val = float(args[1])
            base = float(args[2]) if len(args) > 2 else math.e
            if val <= 0 or base <= 0 or base == 1:
                await message.edit("❌ Invalid values for logarithm.")
                return
            result = math.log(val, base)
            await message.edit(f"🧮 log_{base}({val}) = `{result}`")
        except ValueError:
            await message.edit("❌ Invalid numbers.")

    register_command("Tools", "log", "Calculate logarithm", [])

    # ═══════════════════════════════════════════════════════════════
    #  ENCODERS (20 commands)
    # ═══════════════════════════════════════════════════════════════

    # 22. BASE64_ENCODE / B64E
    @app.on_message(filters.command(["base64_encode", "b64e"], prefixes=".") & filters.me)
    async def b64e_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.b64e <text>`")
            return
        encoded = base64.b64encode(args[1].encode()).decode()
        await message.edit(f"🔒 **Base64 Encoded:**\n`{encoded}`")

    register_command("Tools", "base64_encode", "Encode text to Base64", ["b64e"])

    # 23. BASE64_DECODE / B64D
    @app.on_message(filters.command(["base64_decode", "b64d"], prefixes=".") & filters.me)
    async def b64d_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.b64d <base64>`")
            return
        try:
            decoded = base64.b64decode(args[1].strip()).decode(errors="replace")
            await message.edit(f"🔓 **Base64 Decoded:**\n`{decoded}`")
        except Exception as e:
            await message.edit(f"❌ **Decode error:** `{e}`")

    register_command("Tools", "base64_decode", "Decode Base64 to text", ["b64d"])

    # 24. BASE32_ENCODE / B32E
    @app.on_message(filters.command(["base32_encode", "b32e"], prefixes=".") & filters.me)
    async def b32e_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.b32e <text>`")
            return
        encoded = base64.b32encode(args[1].encode()).decode()
        await message.edit(f"🔒 **Base32 Encoded:**\n`{encoded}`")

    register_command("Tools", "base32_encode", "Encode text to Base32", ["b32e"])

    # 25. BASE32_DECODE / B32D
    @app.on_message(filters.command(["base32_decode", "b32d"], prefixes=".") & filters.me)
    async def b32d_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.b32d <base32>`")
            return
        try:
            decoded = base64.b32decode(args[1].strip()).decode(errors="replace")
            await message.edit(f"🔓 **Base32 Decoded:**\n`{decoded}`")
        except Exception as e:
            await message.edit(f"❌ **Decode error:** `{e}`")

    register_command("Tools", "base32_decode", "Decode Base32 to text", ["b32d"])

    # 26. URL_ENCODE / URLE
    @app.on_message(filters.command(["url_encode", "urle"], prefixes=".") & filters.me)
    async def urle_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.urle <text>`")
            return
        encoded = urllib.parse.quote(args[1])
        await message.edit(f"🔒 **URL Encoded:**\n`{encoded}`")

    register_command("Tools", "url_encode", "URL-encode text", ["urle"])

    # 27. URL_DECODE / URLD
    @app.on_message(filters.command(["url_decode", "urld"], prefixes=".") & filters.me)
    async def urld_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.urld <encoded>`")
            return
        try:
            decoded = urllib.parse.unquote(args[1])
            await message.edit(f"🔓 **URL Decoded:**\n`{decoded}`")
        except Exception as e:
            await message.edit(f"❌ **Decode error:** `{e}`")

    register_command("Tools", "url_decode", "URL-decode text", ["urld"])

    # 28. HTML_ENCODE / HTMLE
    @app.on_message(filters.command(["html_encode", "htmle"], prefixes=".") & filters.me)
    async def htmle_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.htmle <text>`")
            return
        encoded = html.escape(args[1])
        await message.edit(f"🔒 **HTML Encoded:**\n`{encoded}`")

    register_command("Tools", "html_encode", "HTML-encode text", ["htmle"])

    # 29. HTML_DECODE / HTMLD
    @app.on_message(filters.command(["html_decode", "htmld"], prefixes=".") & filters.me)
    async def htmld_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.htmld <encoded>`")
            return
        decoded = html.unescape(args[1])
        await message.edit(f"🔓 **HTML Decoded:**\n`{decoded}`")

    register_command("Tools", "html_decode", "HTML-decode text", ["htmld"])

    # 30. ROT13
    @app.on_message(filters.command("rot13", prefixes=".") & filters.me)
    async def rot13_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.rot13 <text>`")
            return
        result = args[1].translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
        ))
        await message.edit(f"🔄 **ROT13:**\n`{result}`")

    register_command("Tools", "rot13", "ROT13 encode/decode text", [])

    # 31. ROT47
    @app.on_message(filters.command("rot47", prefixes=".") & filters.me)
    async def rot47_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.rot47 <text>`")
            return
        result = []
        for c in args[1]:
            n = ord(c)
            if 33 <= n <= 126:
                result.append(chr(33 + (n - 33 + 47) % 94))
            else:
                result.append(c)
        await message.edit(f"🔄 **ROT47:**\n`{''.join(result)}`")

    register_command("Tools", "rot47", "ROT47 encode/decode text", [])

    # 32. CAESAR_ENCRYPT / CAESARE
    @app.on_message(filters.command(["caesar_encrypt", "caesare"], prefixes=".") & filters.me)
    async def caesare_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.caesare <shift> <text>`")
            return
        try:
            shift = int(args[1]) % 26
            text = args[2]
            result = []
            for c in text:
                if c.isalpha():
                    base = ord("A") if c.isupper() else ord("a")
                    result.append(chr(base + (ord(c) - base + shift) % 26))
                else:
                    result.append(c)
            await message.edit(f"🔒 **Caesar (+{shift}):**\n`{''.join(result)}`")
        except ValueError:
            await message.edit("❌ Shift must be a number.")

    register_command("Tools", "caesar_encrypt", "Caesar cipher encrypt", ["caesare"])

    # 33. CAESAR_DECRYPT / CAESARD
    @app.on_message(filters.command(["caesar_decrypt", "caesard"], prefixes=".") & filters.me)
    async def caesard_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.caesard <shift> <text>`")
            return
        try:
            shift = int(args[1]) % 26
            text = args[2]
            result = []
            for c in text:
                if c.isalpha():
                    base = ord("A") if c.isupper() else ord("a")
                    result.append(chr(base + (ord(c) - base - shift) % 26))
                else:
                    result.append(c)
            await message.edit(f"🔓 **Caesar (-{shift}):**\n`{''.join(result)}`")
        except ValueError:
            await message.edit("❌ Shift must be a number.")

    register_command("Tools", "caesar_decrypt", "Caesar cipher decrypt", ["caesard"])

    # 34. ASCII_ENCODE / ASCIIE
    @app.on_message(filters.command(["ascii_encode", "asciie"], prefixes=".") & filters.me)
    async def asciie_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.asciie <text>`")
            return
        encoded = " ".join(str(ord(c)) for c in args[1])
        await message.edit(f"🔒 **ASCII Encoded:**\n`{encoded}`")

    register_command("Tools", "ascii_encode", "Encode text to ASCII codes", ["asciie"])

    # 35. ASCII_DECODE / ASCIID
    @app.on_message(filters.command(["ascii_decode", "asciid"], prefixes=".") & filters.me)
    async def asciid_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.asciid <space-separated codes>`")
            return
        try:
            codes = args[1].strip().split()
            decoded = "".join(chr(int(c)) for c in codes)
            await message.edit(f"🔓 **ASCII Decoded:**\n`{decoded}`")
        except (ValueError, OverflowError):
            await message.edit("❌ Invalid ASCII codes.")

    register_command("Tools", "ascii_decode", "Decode ASCII codes to text", ["asciid"])

    # 36. HEX_ENCODE / HEXE
    @app.on_message(filters.command(["hex_encode", "hexe"], prefixes=".") & filters.me)
    async def hexe_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.hexe <text>`")
            return
        encoded = args[1].encode().hex()
        await message.edit(f"🔒 **Hex Encoded:**\n`{encoded}`")

    register_command("Tools", "hex_encode", "Encode text to hex", ["hexe"])

    # 37. HEX_DECODE / HEXD
    @app.on_message(filters.command(["hex_decode", "hexd"], prefixes=".") & filters.me)
    async def hexd_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.hexd <hex_string>`")
            return
        try:
            decoded = bytes.fromhex(args[1].strip()).decode(errors="replace")
            await message.edit(f"🔓 **Hex Decoded:**\n`{decoded}`")
        except ValueError:
            await message.edit("❌ Invalid hex string.")

    register_command("Tools", "hex_decode", "Decode hex to text", ["hexd"])

    # 38. BINARY_ENCODE / BINE
    @app.on_message(filters.command(["binary_encode", "bine"], prefixes=".") & filters.me)
    async def bine_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.bine <text>`")
            return
        encoded = " ".join(format(ord(c), "08b") for c in args[1])
        await message.edit(f"🔒 **Binary Encoded:**\n`{encoded}`")

    register_command("Tools", "binary_encode", "Encode text to binary", ["bine"])

    # 39. BINARY_DECODE / BIND
    @app.on_message(filters.command(["binary_decode", "bind"], prefixes=".") & filters.me)
    async def bind_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.bind <space-separated binary>`")
            return
        try:
            chunks = args[1].strip().split()
            decoded = "".join(chr(int(b, 2)) for b in chunks)
            await message.edit(f"🔓 **Binary Decoded:**\n`{decoded}`")
        except (ValueError, OverflowError):
            await message.edit("❌ Invalid binary values.")

    register_command("Tools", "binary_decode", "Decode binary to text", ["bind"])

    # 40. MORSE_ENCODE / MORSEE
    @app.on_message(filters.command(["morse_encode", "morsee"], prefixes=".") & filters.me)
    async def morsee_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.morsee <text>`")
            return
        text = args[1].upper()
        encoded = []
        for c in text:
            if c in _MORSE:
                encoded.append(_MORSE[c])
            else:
                encoded.append("?")
        await message.edit(f"📡 **Morse Encoded:**\n`{' '.join(encoded)}`")

    register_command("Tools", "morse_encode", "Encode text to Morse code", ["morsee"])

    # 41. MORSE_DECODE / MORSED
    @app.on_message(filters.command(["morse_decode", "morsed"], prefixes=".") & filters.me)
    async def morsed_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.morsed <morse>` (use spaces between letters, / for space)")
            return
        parts = args[1].strip().split()
        decoded = []
        for p in parts:
            if p == "/":
                decoded.append(" ")
            elif p in _MORSE_REV:
                decoded.append(_MORSE_REV[p])
            else:
                decoded.append("?")
        await message.edit(f"📡 **Morse Decoded:**\n`{''.join(decoded)}`")

    register_command("Tools", "morse_decode", "Decode Morse code to text", ["morsed"])

    # ═══════════════════════════════════════════════════════════════
    #  HASH (12 commands)
    # ═══════════════════════════════════════════════════════════════

    # 42. MD5
    @app.on_message(filters.command("md5", prefixes=".") & filters.me)
    async def md5_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.md5 <text>`")
            return
        result = hashlib.md5(args[1].encode()).hexdigest()
        await message.edit(f"🔑 **MD5:**\n`{result}`")

    register_command("Tools", "md5", "Generate MD5 hash", [])

    # 43. SHA1
    @app.on_message(filters.command("sha1", prefixes=".") & filters.me)
    async def sha1_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.sha1 <text>`")
            return
        result = hashlib.sha1(args[1].encode()).hexdigest()
        await message.edit(f"🔑 **SHA1:**\n`{result}`")

    register_command("Tools", "sha1", "Generate SHA1 hash", [])

    # 44. SHA256
    @app.on_message(filters.command("sha256", prefixes=".") & filters.me)
    async def sha256_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.sha256 <text>`")
            return
        result = hashlib.sha256(args[1].encode()).hexdigest()
        await message.edit(f"🔑 **SHA256:**\n`{result}`")

    register_command("Tools", "sha256", "Generate SHA256 hash", [])

    # 45. SHA512
    @app.on_message(filters.command("sha512", prefixes=".") & filters.me)
    async def sha512_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.sha512 <text>`")
            return
        result = hashlib.sha512(args[1].encode()).hexdigest()
        await message.edit(f"🔑 **SHA512:**\n`{result}`")

    register_command("Tools", "sha512", "Generate SHA512 hash", [])

    # 46. HASH (all at once)
    @app.on_message(filters.command("hash", prefixes=".") & filters.me)
    async def hash_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.hash <text>`")
            return
        data = args[1].encode()
        text = f"🔑 **All Hashes for:** `{args[1][:50]}`\n\n"
        text += f"**MD5:** `{hashlib.md5(data).hexdigest()}`\n"
        text += f"**SHA1:** `{hashlib.sha1(data).hexdigest()}`\n"
        text += f"**SHA256:** `{hashlib.sha256(data).hexdigest()}`\n"
        text += f"**SHA512:** `{hashlib.sha512(data).hexdigest()}`"
        await message.edit(text)

    register_command("Tools", "hash", "Generate MD5+SHA1+SHA256+SHA512 hashes", [])

    # 47. BCRYPT_HASH
    @app.on_message(filters.command("bcrypt_hash", prefixes=".") & filters.me)
    async def bcrypt_hash_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.bcrypt_hash <text>`")
            return
        try:
            import bcrypt
            result = bcrypt.hashpw(args[1].encode(), bcrypt.gensalt()).decode()
            await message.edit(f"🔑 **bcrypt:**\n`{result}`")
        except ImportError:
            # Fallback: use hashlib with salted SHA256
            salt = os.urandom(16).hex()
            result = hashlib.sha256((salt + args[1]).encode()).hexdigest()
            await message.edit(f"🔑 **Salted SHA256** (bcrypt not installed):\nSalt: `{salt}`\nHash: `{result}`")

    register_command("Tools", "bcrypt_hash", "Generate bcrypt hash (or salted SHA256 fallback)", [])

    # 48. UUID
    @app.on_message(filters.command("uuid", prefixes=".") & filters.me)
    async def uuid_cmd(client, message):
        result = str(_uuid.uuid4())
        await message.edit(f"🆔 **UUID v4:**\n`{result}`")

    register_command("Tools", "uuid", "Generate a random UUID v4", [])

    # 49. PASSWORD / PASSWD / GENPASS
    @app.on_message(filters.command(["password", "passwd", "genpass"], prefixes=".") & filters.me)
    async def password_cmd(client, message):
        args = message.text.split(None, 1)
        length = 16
        if len(args) > 1:
            try:
                length = int(args[1])
                if length < 4:
                    length = 4
                elif length > 128:
                    length = 128
            except ValueError:
                pass
        chars = string.ascii_letters + string.digits + string.punctuation
        pw = "".join(random.choices(chars, k=length))
        await message.edit(f"🔐 **Generated Password** (`{length}` chars):\n`{pw}`")

    register_command("Tools", "password", "Generate a random password", ["passwd", "genpass"])

    # 50. PASSWORD_STRENGTH
    @app.on_message(filters.command("password_strength", prefixes=".") & filters.me)
    async def password_strength_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.password_strength <password>`")
            return
        pw = args[1]
        score = 0
        feedback = []
        if len(pw) >= 8:
            score += 1
        else:
            feedback.append("Use at least 8 characters")
        if len(pw) >= 12:
            score += 1
        if any(c.islower() for c in pw):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        if any(c.isupper() for c in pw):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        if any(c.isdigit() for c in pw):
            score += 1
        else:
            feedback.append("Add numbers")
        if any(c in string.punctuation for c in pw):
            score += 1
        else:
            feedback.append("Add special characters")
        labels = {0: "💀 Very Weak", 1: "😰 Weak", 2: "😐 Fair",
                  3: "🙂 Good", 4: "💪 Strong", 5: "🛡 Very Strong", 6: "🔥 Unbreakable"}
        text = f"🔐 **Password Strength:** {labels.get(score, 'Unknown')} (`{score}/6`)\n"
        if feedback:
            text += "\n**Suggestions:**\n" + "\n".join(f"• {f}" for f in feedback)
        await message.edit(text)

    register_command("Tools", "password_strength", "Check password strength", [])

    # 51. OTP
    @app.on_message(filters.command("otp", prefixes=".") & filters.me)
    async def otp_cmd(client, message):
        args = message.text.split(None, 1)
        length = 6
        if len(args) > 1:
            try:
                length = int(args[1])
                if length < 4:
                    length = 4
                elif length > 32:
                    length = 32
            except ValueError:
                pass
        otp_val = "".join(random.choices(string.digits, k=length))
        await message.edit(f"🔑 **OTP:** `{otp_val}`")

    register_command("Tools", "otp", "Generate a one-time password", [])

    # 52. TOKENIZE
    @app.on_message(filters.command("tokenize", prefixes=".") & filters.me)
    async def tokenize_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.tokenize <text>`")
            return
        data = args[1].encode()
        h = hashlib.sha256(data + os.urandom(16)).hexdigest()
        token = f"tkn_{base64.urlsafe_b64encode(data)[:12].decode()}_{h[:24]}"
        await message.edit(f"🎫 **Token:**\n`{token}`")

    register_command("Tools", "tokenize", "Generate a token from text", [])

    # 53. RANDOMHEX
    @app.on_message(filters.command("randomhex", prefixes=".") & filters.me)
    async def randomhex_cmd(client, message):
        args = message.text.split(None, 1)
        length = 32
        if len(args) > 1:
            try:
                length = int(args[1])
                if length < 1:
                    length = 1
                elif length > 256:
                    length = 256
            except ValueError:
                pass
        result = os.urandom(length).hex()
        await message.edit(f"🎲 **Random Hex** (`{length}` bytes):\n`{result}`")

    register_command("Tools", "randomhex", "Generate random hex string", [])

    # ═══════════════════════════════════════════════════════════════
    #  STRING (21 commands)
    # ═══════════════════════════════════════════════════════════════

    # 54. LEN / LENGTH
    @app.on_message(filters.command(["len", "length"], prefixes=".") & filters.me)
    async def len_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.len <text>`")
            return
        text = args[1]
        chars = len(text)
        words = len(text.split())
        await message.edit(f"📏 **Length:** `{chars}` chars, `{words}` words")

    register_command("Tools", "len", "Count characters and words", ["length"])

    # 55. COUNT / WORDCOUNT
    @app.on_message(filters.command(["count", "wordcount"], prefixes=".") & filters.me)
    async def count_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.count <text>`")
            return
        words = args[1].split()
        counts = {}
        for w in words:
            w_lower = w.lower().strip(".,!?;:'\"")
            counts[w_lower] = counts.get(w_lower, 0) + 1
        text = "📊 **Word Count:**\n\n"
        for w, c in sorted(counts.items(), key=lambda x: -x[1])[:20]:
            text += f"  • `{w}`: {c}\n"
        await message.edit(text)

    register_command("Tools", "count", "Count word occurrences", ["wordcount"])

    # 56. CHARCOUNT
    @app.on_message(filters.command("charcount", prefixes=".") & filters.me)
    async def charcount_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.charcount <text>`")
            return
        text_val = args[1]
        counts = {}
        for c in text_val:
            if c != " ":
                counts[c] = counts.get(c, 0) + 1
        result = "📊 **Character Count:**\n\n"
        for ch, cnt in sorted(counts.items(), key=lambda x: -x[1])[:25]:
            result += f"  • `{ch}`: {cnt}\n"
        await message.edit(result)

    register_command("Tools", "charcount", "Count character occurrences", [])

    # 57. WORDFREQ
    @app.on_message(filters.command("wordfreq", prefixes=".") & filters.me)
    async def wordfreq_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.wordfreq <text>`")
            return
        words = args[1].lower().split()
        freq = {}
        for w in words:
            w = w.strip(".,!?;:'\"()")
            freq[w] = freq.get(w, 0) + 1
        total = len(words)
        text = f"📊 **Word Frequency** ({total} words):\n\n"
        for w, c in sorted(freq.items(), key=lambda x: -x[1])[:20]:
            pct = (c / total) * 100
            text += f"  • `{w}`: {c} ({pct:.1f}%)\n"
        await message.edit(text)

    register_command("Tools", "wordfreq", "Show word frequency distribution", [])

    # 58. SORT
    @app.on_message(filters.command("sort", prefixes=".") & filters.me)
    async def sort_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.sort <text>` (sorts words alphabetically)")
            return
        words = args[1].split()
        await message.edit(f"📋 **Sorted:**\n`{' '.join(sorted(words))}`")

    register_command("Tools", "sort", "Sort words alphabetically", [])

    # 59. SHUFFLE
    @app.on_message(filters.command("shuffle", prefixes=".") & filters.me)
    async def shuffle_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.shuffle <text>`")
            return
        words = args[1].split()
        random.shuffle(words)
        await message.edit(f"🔀 **Shuffled:**\n`{' '.join(words)}`")

    register_command("Tools", "shuffle", "Randomly shuffle words", [])

    # 60. UNIQUE / DEDUP
    @app.on_message(filters.command(["unique", "dedup"], prefixes=".") & filters.me)
    async def unique_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.unique <text>` (removes duplicate words)")
            return
        words = args[1].split()
        seen = set()
        result = []
        for w in words:
            if w.lower() not in seen:
                seen.add(w.lower())
                result.append(w)
        await message.edit(f"✨ **Unique:**\n`{' '.join(result)}`")

    register_command("Tools", "unique", "Remove duplicate words", ["dedup"])

    # 61. TRIM
    @app.on_message(filters.command("trim", prefixes=".") & filters.me)
    async def trim_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.trim <text>`")
            return
        await message.edit(f"✂️ **Trimmed:**\n`{args[1].strip()}`")

    register_command("Tools", "trim", "Trim leading/trailing whitespace", [])

    # 62. SQUEEZE
    @app.on_message(filters.command("squeeze", prefixes=".") & filters.me)
    async def squeeze_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.squeeze <text>` (collapse multiple spaces)")
            return
        result = re.sub(r"\s+", " ", args[1]).strip()
        await message.edit(f"🗜 **Squeezed:**\n`{result}`")

    register_command("Tools", "squeeze", "Collapse multiple spaces into one", [])

    # 63. REVERSE / REV
    @app.on_message(filters.command(["reverse", "rev"], prefixes=".") & filters.me)
    async def reverse_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.rev <text>`")
            return
        await message.edit(f"🔄 **Reversed:**\n`{args[1][::-1]}`")

    register_command("Tools", "reverse", "Reverse text", ["rev"])

    # 64. TITLE_CASE
    @app.on_message(filters.command("title_case", prefixes=".") & filters.me)
    async def title_case_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.title_case <text>`")
            return
        await message.edit(f"📝 **Title Case:**\n`{args[1].title()}`")

    register_command("Tools", "title_case", "Convert to Title Case", [])

    # 65. SENTENCE_CASE
    @app.on_message(filters.command("sentence_case", prefixes=".") & filters.me)
    async def sentence_case_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.sentence_case <text>`")
            return
        result = ". ".join(s.strip().capitalize() for s in args[1].split("."))
        await message.edit(f"📝 **Sentence Case:**\n`{result}`")

    register_command("Tools", "sentence_case", "Convert to Sentence case", [])

    # 66. CAMEL_CASE
    @app.on_message(filters.command("camel_case", prefixes=".") & filters.me)
    async def camel_case_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.camel_case <text>`")
            return
        parts = re.split(r"[\s_\-]+", args[1].strip())
        if not parts:
            await message.edit("❌ No text provided.")
            return
        result = parts[0].lower() + "".join(p.capitalize() for p in parts[1:])
        await message.edit(f"📝 **camelCase:**\n`{result}`")

    register_command("Tools", "camel_case", "Convert to camelCase", [])

    # 67. SNAKE_CASE
    @app.on_message(filters.command("snake_case", prefixes=".") & filters.me)
    async def snake_case_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.snake_case <text>`")
            return
        result = re.sub(r"[\s\-]+", "_", args[1].strip()).lower()
        result = re.sub(r"([A-Z])", r"_\1", result).strip("_").lower()
        result = re.sub(r"__+", "_", result)
        await message.edit(f"📝 **snake_case:**\n`{result}`")

    register_command("Tools", "snake_case", "Convert to snake_case", [])

    # 68. KEBAB_CASE
    @app.on_message(filters.command("kebab_case", prefixes=".") & filters.me)
    async def kebab_case_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.kebab_case <text>`")
            return
        result = re.sub(r"[\s_]+", "-", args[1].strip()).lower()
        result = re.sub(r"([A-Z])", r"-\1", result).strip("-").lower()
        result = re.sub(r"--+", "-", result)
        await message.edit(f"📝 **kebab-case:**\n`{result}`")

    register_command("Tools", "kebab_case", "Convert to kebab-case", [])

    # 69. PASCAL_CASE
    @app.on_message(filters.command("pascal_case", prefixes=".") & filters.me)
    async def pascal_case_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.pascal_case <text>`")
            return
        parts = re.split(r"[\s_\-]+", args[1].strip())
        result = "".join(p.capitalize() for p in parts if p)
        await message.edit(f"📝 **PascalCase:**\n`{result}`")

    register_command("Tools", "pascal_case", "Convert to PascalCase", [])

    # 70. DOT_CASE
    @app.on_message(filters.command("dot_case", prefixes=".") & filters.me)
    async def dot_case_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.dot_case <text>`")
            return
        result = re.sub(r"[\s_\-]+", ".", args[1].strip()).lower()
        result = re.sub(r"([A-Z])", r".\1", result).strip(".").lower()
        result = re.sub(r"\.\.+", ".", result)
        await message.edit(f"📝 **dot.case:**\n`{result}`")

    register_command("Tools", "dot_case", "Convert to dot.case", [])

    # 71. SLUG
    @app.on_message(filters.command("slug", prefixes=".") & filters.me)
    async def slug_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.slug <text>`")
            return
        result = args[1].strip().lower()
        result = re.sub(r"[^\w\s-]", "", result)
        result = re.sub(r"[\s_]+", "-", result)
        result = re.sub(r"-+", "-", result).strip("-")
        await message.edit(f"🔗 **Slug:**\n`{result}`")

    register_command("Tools", "slug", "Generate URL-safe slug", [])

    # 72. STRIPHTML
    @app.on_message(filters.command("striphtml", prefixes=".") & filters.me)
    async def striphtml_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.striphtml <html>`")
            return
        result = re.sub(r"<[^>]+>", "", args[1])
        result = html.unescape(result)
        await message.edit(f"🧹 **Stripped HTML:**\n`{result}`")

    register_command("Tools", "striphtml", "Strip HTML tags from text", [])

    # 73. COUNTCHAR
    @app.on_message(filters.command("countchar", prefixes=".") & filters.me)
    async def countchar_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.countchar <char> <text>`")
            return
        char = args[1][0]
        text_val = args[2]
        count = text_val.count(char)
        await message.edit(f"📊 `{char}` appears `{count}` time(s) in text.")

    register_command("Tools", "countchar", "Count occurrences of a character", [])

    # 74. FINDREPLACE / REPLACE
    @app.on_message(filters.command(["findreplace", "replace"], prefixes=".") & filters.me)
    async def findreplace_cmd(client, message):
        args = message.text.split(None, 3)
        if len(args) < 4:
            await message.edit("❌ **Usage:** `.replace <find> <replace_with> <text>`")
            return
        find = args[1]
        repl = args[2]
        text_val = args[3]
        result = text_val.replace(find, repl)
        await message.edit(f"🔄 **Replaced** `{find}` → `{repl}`:\n`{result}`")

    register_command("Tools", "findreplace", "Find and replace in text", ["replace"])

    # ═══════════════════════════════════════════════════════════════
    #  NETWORK (10 commands)
    # ═══════════════════════════════════════════════════════════════

    # 75. WHOIS (basic socket-based)
    @app.on_message(filters.command("whois", prefixes=".") & filters.me)
    async def whois_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.whois <domain>`")
            return
        domain = args[1].strip()
        try:
            addr_info = socket.getaddrinfo(domain, None)
            ips = list(set(ai[4][0] for ai in addr_info))
            host = socket.gethostbyaddr(ips[0]) if ips else None
            text = f"🌐 **WHOIS: {domain}**\n\n"
            text += f"📡 **IPs:** {', '.join(f'`{ip}`' for ip in ips[:5])}\n"
            if host:
                text += f"🏷 **Hostname:** `{host[0]}`\n"
            await message.edit(text)
        except socket.gaierror:
            await message.edit(f"❌ Cannot resolve `{domain}`.")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "whois", "Basic WHOIS/domain lookup", [])

    # 76. DNS
    @app.on_message(filters.command("dns", prefixes=".") & filters.me)
    async def dns_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.dns <domain>`")
            return
        domain = args[1].strip()
        try:
            results = socket.getaddrinfo(domain, None)
            text = f"🌐 **DNS Records: {domain}**\n\n"
            seen = set()
            for r in results[:10]:
                family = "IPv4" if r[0] == socket.AF_INET else "IPv6"
                ip = r[4][0]
                key = (family, ip)
                if key not in seen:
                    seen.add(key)
                    text += f"  • {family}: `{ip}`\n"
            await message.edit(text)
        except socket.gaierror:
            await message.edit(f"❌ Cannot resolve `{domain}`.")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "dns", "DNS lookup for a domain", [])

    # 77. HEADERS
    @app.on_message(filters.command("headers", prefixes=".") & filters.me)
    async def headers_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.headers <url>`")
            return
        url = args[1].strip()
        if not url.startswith("http"):
            url = "http://" + url
        try:
            import urllib.request
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=10) as resp:
                text = f"🌐 **Headers: {url}**\n\n"
                for header, value in resp.headers.items():
                    text += f"  • **{header}:** `{value}`\n"
                await message.edit(text)
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "headers", "Fetch HTTP headers from URL", [])

    # 78. IPINFO
    @app.on_message(filters.command("ipinfo", prefixes=".") & filters.me)
    async def ipinfo_cmd(client, message):
        args = message.text.split(None, 1)
        ip = args[1].strip() if len(args) > 1 else ""
        if not ip:
            # Try to get own IP
            try:
                import urllib.request
                with urllib.request.urlopen("https://api.ipify.org", timeout=10) as resp:
                    ip = resp.read().decode()
            except Exception:
                await message.edit("❌ Could not determine your IP.")
                return
        try:
            # Simple socket-based lookup
            hostname = socket.gethostbyaddr(ip)
            text = f"🌐 **IP Info: {ip}**\n\n"
            text += f"🏷 **Hostname:** `{hostname[0]}`\n"
            if hostname[1]:
                text += f"📋 **Aliases:** {', '.join(f'`{a}`' for a in hostname[1][:5])}\n"
            await message.edit(text)
        except socket.herror:
            await message.edit(f"🌐 **IP:** `{ip}`\n_(No reverse DNS found)_")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "ipinfo", "Get info about an IP address", [])

    # 79. PORTSCAN
    @app.on_message(filters.command("portscan", prefixes=".") & filters.me)
    async def portscan_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.portscan <host> [port_range]`\nExample: `.portscan example.com 1-100`")
            return
        host = args[1].strip()
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 5432, 8080, 8443]
        if len(args) > 2:
            try:
                parts = args[2].split("-")
                start, end = int(parts[0]), int(parts[1])
                common_ports = list(range(start, min(end + 1, 1024)))
            except (ValueError, IndexError):
                pass
        text = f"🔍 **Port Scan: {host}**\n\n"
        found = 0
        for port in common_ports[:25]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                if result == 0:
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = "unknown"
                    text += f"  ✅ Port `{port}` ({service}) — **OPEN**\n"
                    found += 1
                sock.close()
            except Exception:
                pass
        if found == 0:
            text += "  No open ports found in scanned range."
        await message.edit(text)

    register_command("Tools", "portscan", "Scan common ports on a host", [])

    # 80. MYIP
    @app.on_message(filters.command("myip", prefixes=".") & filters.me)
    async def myip_cmd(client, message):
        try:
            import urllib.request
            with urllib.request.urlopen("https://api.ipify.org", timeout=10) as resp:
                ip = resp.read().decode()
            await message.edit(f"🌐 **Your Public IP:** `{ip}`")
        except Exception as e:
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                await message.edit(f"🌐 **Local IP:** `{local_ip}`\n_(Could not fetch public IP: {e})_")
            except Exception:
                await message.edit(f"❌ Could not determine IP: `{e}`")

    register_command("Tools", "myip", "Show your public IP address", [])

    # 81. PING_HOST
    @app.on_message(filters.command("ping_host", prefixes=".") & filters.me)
    async def ping_host_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.ping_host <host>`")
            return
        host = args[1].strip()
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, 80))
            elapsed = round((time.time() - start) * 1000)
            sock.close()
            if result == 0:
                await message.edit(f"🏓 **{host}** is reachable — `{elapsed}ms`")
            else:
                await message.edit(f"❌ **{host}** is not reachable on port 80.")
        except socket.gaierror:
            await message.edit(f"❌ Cannot resolve `{host}`.")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "ping_host", "TCP ping a host", [])

    # 82. HTTPCODE
    _HTTP_CODES = {
        100: "Continue", 101: "Switching Protocols",
        200: "OK", 201: "Created", 204: "No Content", 206: "Partial Content",
        301: "Moved Permanently", 302: "Found", 304: "Not Modified",
        400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
        404: "Not Found", 405: "Method Not Allowed", 408: "Request Timeout",
        409: "Conflict", 410: "Gone", 413: "Payload Too Large",
        418: "I'm a Teapot", 429: "Too Many Requests",
        500: "Internal Server Error", 502: "Bad Gateway",
        503: "Service Unavailable", 504: "Gateway Timeout",
    }

    @app.on_message(filters.command("httpcode", prefixes=".") & filters.me)
    async def httpcode_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.httpcode <code>`\nExample: `.httpcode 404`")
            return
        try:
            code = int(args[1])
            desc = _HTTP_CODES.get(code, "Unknown")
            await message.edit(f"🌐 **HTTP {code}:** `{desc}`")
        except ValueError:
            await message.edit("❌ Invalid HTTP code.")

    register_command("Tools", "httpcode", "Look up HTTP status code meaning", [])

    # 83. URLEXPAND
    @app.on_message(filters.command("urlexpand", prefixes=".") & filters.me)
    async def urlexpand_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.urlexpand <short_url>`")
            return
        url = args[1].strip()
        if not url.startswith("http"):
            url = "http://" + url
        try:
            import urllib.request
            req = urllib.request.Request(url, method="HEAD")
            resp = urllib.request.urlopen(req, timeout=10)
            final_url = resp.url
            await message.edit(f"🔗 **Expanded:**\n`{final_url}`")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "urlexpand", "Expand a shortened URL", [])

    # 84. CHECKURL
    @app.on_message(filters.command("checkurl", prefixes=".") & filters.me)
    async def checkurl_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.checkurl <url>`")
            return
        url = args[1].strip()
        if not url.startswith("http"):
            url = "http://" + url
        try:
            import urllib.request
            req = urllib.request.Request(url, method="HEAD")
            resp = urllib.request.urlopen(req, timeout=10)
            code = resp.status
            await message.edit(f"✅ **URL is reachable** — Status: `{code}`")
        except urllib.error.HTTPError as e:
            await message.edit(f"⚠️ **URL returned** HTTP `{e.code}`")
        except Exception as e:
            await message.edit(f"❌ **URL unreachable:** `{e}`")

    register_command("Tools", "checkurl", "Check if a URL is reachable", [])

    # ═══════════════════════════════════════════════════════════════
    #  MISC (18 commands)
    # ═══════════════════════════════════════════════════════════════

    # 85. WEATHER (mock)
    _WEATHER_CONDITIONS = [
        "🌤 Partly Cloudy", "☀️ Sunny", "🌧 Rainy", "⛈ Thunderstorm",
        "🌨 Snowy", "🌪 Tornado Warning", "🌫 Foggy", "💨 Windy",
        "🥶 Freezing Cold", "🥵 Scorching Hot", "🌈 Rainbow After Rain",
        "☁️ Overcast", "🌊 Hurricane nearby", "🏜 Sandstorm",
        "🌋 Volcanic Ash", "🛸 Alien Weather (unconfirmed)",
        "🔥 Spontaneous Combustion Warning", "❄️ Blizzard",
    ]

    @app.on_message(filters.command("weather", prefixes=".") & filters.me)
    async def weather_cmd(client, message):
        args = message.text.split(None, 1)
        location = args[1].strip() if len(args) > 1 else "Your Location"
        cond = random.choice(_WEATHER_CONDITIONS)
        temp = random.randint(-20, 45)
        humidity = random.randint(10, 100)
        wind = random.randint(0, 80)
        text = (
            f"🌤 **Weather for {location}** _(mock)_\n\n"
            f"🌡 **Condition:** {cond}\n"
            f"🌡 **Temperature:** `{temp}°C` / `{round(temp * 9/5 + 32)}°F`\n"
            f"💧 **Humidity:** `{humidity}%`\n"
            f"💨 **Wind:** `{wind} km/h`\n"
            f"\n_⚠️ This is mock weather data for fun!_"
        )
        await message.edit(text)

    register_command("Tools", "weather", "Mock weather report (for fun)", [])

    # 86. QRCODE / QR
    @app.on_message(filters.command(["qrcode", "qr"], prefixes=".") & filters.me)
    async def qrcode_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.qr <text or URL>`")
            return
        try:
            import qrcode
            from io import BytesIO
            img = qrcode.make(args[1])
            bio = BytesIO()
            bio.name = "qr.png"
            img.save(bio, "PNG")
            bio.seek(0)
            await message.delete()
            await client.send_photo(message.chat.id, bio, caption=f"📱 **QR Code for:** `{args[1][:50]}`")
        except ImportError:
            await message.edit("❌ `qrcode` library not installed. `pip install qrcode[pil]`")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "qrcode", "Generate QR code from text/URL", ["qr"])

    # 87. BARCODE
    @app.on_message(filters.command("barcode", prefixes=".") & filters.me)
    async def barcode_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.barcode <text>`")
            return
        try:
            import qrcode
            from io import BytesIO
            # Use QR code as barcode substitute since we only have stdlib + qrcode
            img = qrcode.make(args[1], version=1, box_size=5)
            bio = BytesIO()
            bio.name = "barcode.png"
            img.save(bio, "PNG")
            bio.seek(0)
            await message.delete()
            await client.send_photo(message.chat.id, bio, caption=f"📊 **Barcode (QR) for:** `{args[1][:50]}`")
        except ImportError:
            await message.edit("❌ `qrcode` library not installed. `pip install qrcode[pil]`")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "barcode", "Generate barcode (QR format)", [])

    # 88. SHORTEN (mock - no API)
    @app.on_message(filters.command("shorten", prefixes=".") & filters.me)
    async def shorten_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.shorten <url>`")
            return
        url = args[1].strip()
        h = hashlib.md5(url.encode()).hexdigest()[:6]
        short = f"https://nxu.be/{h}"
        await message.edit(
            f"🔗 **Shortened URL** _(mock)_\n\n"
            f"📍 Original: `{url}`\n"
            f"🔗 Short: `{short}`\n\n"
            f"_⚠️ Mock shortener for demo_"
        )

    register_command("Tools", "shorten", "Shorten URL (mock)", [])

    # 89. UNSHORTEN (mock)
    @app.on_message(filters.command("unshorten", prefixes=".") & filters.me)
    async def unshorten_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.unshorten <short_url>`")
            return
        url = args[1].strip()
        if not url.startswith("http"):
            url = "http://" + url
        try:
            import urllib.request
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req, timeout=10)
            await message.edit(f"🔗 **Unshortened:**\n`{resp.url}`")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "unshorten", "Follow redirects to final URL", [])

    # 90. TIMESTAMP / EPOCH
    @app.on_message(filters.command(["timestamp", "epoch"], prefixes=".") & filters.me)
    async def timestamp_cmd(client, message):
        now = time.time()
        dt = datetime.fromtimestamp(now, tz=timezone.utc)
        text = (
            f"⏱ **Current Timestamp**\n\n"
            f"🕐 **Unix:** `{int(now)}`\n"
            f"🕐 **Unix (ms):** `{int(now * 1000)}`\n"
            f"📅 **UTC:** `{dt.strftime('%Y-%m-%d %H:%M:%S')}`\n"
            f"📅 **ISO:** `{dt.isoformat()}`"
        )
        await message.edit(text)

    register_command("Tools", "timestamp", "Show current Unix timestamp", ["epoch"])

    # 91. COUNTDOWN
    @app.on_message(filters.command("countdown", prefixes=".") & filters.me)
    async def countdown_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.countdown <YYYY-MM-DD HH:MM>` or `.countdown <seconds>`")
            return
        try:
            # Try as seconds first
            try:
                secs = int(args[1])
                target = datetime.now(tz=timezone.utc).timestamp() + secs
            except ValueError:
                # Try as date string
                target = datetime.strptime(args[1].strip(), "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc).timestamp()
            now = time.time()
            diff = target - now
            if diff <= 0:
                await message.edit("❌ That time has already passed!")
                return
            d, rem = divmod(int(diff), 86400)
            h, rem = divmod(rem, 3600)
            m, s = divmod(rem, 60)
            text = f"⏳ **Countdown:** `{d}d {h}h {m}m {s}s`"
            await message.edit(text)
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "countdown", "Countdown to a date/time", [])

    # 92. TIMER
    @app.on_message(filters.command("timer", prefixes=".") & filters.me)
    async def timer_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.timer <seconds>` (max 600)")
            return
        try:
            secs = int(args[1])
            if secs < 1 or secs > 600:
                await message.edit("❌ Timer must be 1-600 seconds.")
                return
            msg = await message.edit(f"⏲ **Timer:** `{secs}s` remaining...")
            for i in range(secs, 0, -1):
                await asyncio.sleep(1)
                try:
                    await msg.edit(f"⏲ **Timer:** `{i-1}s` remaining...")
                except Exception:
                    break
            try:
                await msg.edit("⏲ **Timer:** ⏰ **DONE!**")
            except Exception:
                pass
        except ValueError:
            await message.edit("❌ Invalid number.")

    register_command("Tools", "timer", "Set a countdown timer", [])

    # 93. STOPWATCH
    _stopwatch_start = {}

    @app.on_message(filters.command("stopwatch", prefixes=".") & filters.me)
    async def stopwatch_cmd(client, message):
        chat_id = message.chat.id
        if chat_id in _stopwatch_start:
            elapsed = time.time() - _stopwatch_start.pop(chat_id)
            m, s = divmod(int(elapsed), 60)
            h, m = divmod(m, 60)
            await message.edit(f"⏱ **Stopwatch stopped:** `{h}h {m}m {s}s`")
        else:
            _stopwatch_start[chat_id] = time.time()
            await message.edit("⏱ **Stopwatch started!** Use `.stopwatch` again to stop.")

    register_command("Tools", "stopwatch", "Start/stop a stopwatch", [])

    # 94. COLOR / HEXCOLOR
    @app.on_message(filters.command(["color", "hexcolor"], prefixes=".") & filters.me)
    async def color_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        else:
            color_str = args[1].strip().lstrip("#")
            try:
                if len(color_str) == 6:
                    r = int(color_str[0:2], 16)
                    g = int(color_str[2:4], 16)
                    b = int(color_str[4:6], 16)
                elif len(color_str) == 3:
                    r = int(color_str[0] * 2, 16)
                    g = int(color_str[1] * 2, 16)
                    b = int(color_str[2] * 2, 16)
                else:
                    await message.edit("❌ Invalid hex color. Use #RRGGBB or #RGB.")
                    return
            except ValueError:
                await message.edit("❌ Invalid hex color.")
                return
        hex_val = f"#{r:02X}{g:02X}{b:02X}"
        await message.edit(
            f"🎨 **Color Info**\n\n"
            f"🏷 **HEX:** `{hex_val}`\n"
            f"🔴 **RGB:** `rgb({r}, {g}, {b})`\n"
            f"📊 **R:** `{r}` | **G:** `{g}` | **B:** `{b}`"
        )

    register_command("Tools", "color", "Show color info from hex or random", ["hexcolor"])

    # 95. RGB2HEX
    @app.on_message(filters.command("rgb2hex", prefixes=".") & filters.me)
    async def rgb2hex_cmd(client, message):
        args = message.text.split(None, 3)
        if len(args) < 4:
            await message.edit("❌ **Usage:** `.rgb2hex <R> <G> <B>`")
            return
        try:
            r, g, b = int(args[1]), int(args[2]), int(args[3])
            if not all(0 <= v <= 255 for v in (r, g, b)):
                await message.edit("❌ Values must be 0-255.")
                return
            await message.edit(f"🎨 `rgb({r}, {g}, {b})` → `#{r:02X}{g:02X}{b:02X}`")
        except ValueError:
            await message.edit("❌ Invalid numbers.")

    register_command("Tools", "rgb2hex", "Convert RGB to hex color", [])

    # 96. HEX2RGB
    @app.on_message(filters.command("hex2rgb", prefixes=".") & filters.me)
    async def hex2rgb_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.hex2rgb <#RRGGBB>`")
            return
        h = args[1].strip().lstrip("#")
        try:
            if len(h) == 6:
                r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            elif len(h) == 3:
                r, g, b = int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16)
            else:
                await message.edit("❌ Invalid hex. Use RRGGBB or RGB.")
                return
            await message.edit(f"🎨 `#{h.upper()}` → `rgb({r}, {g}, {b})`")
        except ValueError:
            await message.edit("❌ Invalid hex color.")

    register_command("Tools", "hex2rgb", "Convert hex color to RGB", [])

    # 97. PALETTE
    @app.on_message(filters.command("palette", prefixes=".") & filters.me)
    async def palette_cmd(client, message):
        args = message.text.split(None, 1)
        count = 5
        if len(args) > 1:
            try:
                count = int(args[1])
                count = max(2, min(count, 10))
            except ValueError:
                pass
        colors = []
        for _ in range(count):
            r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            colors.append(f"#{r:02X}{g:02X}{b:02X}")
        text = f"🎨 **Random Palette** ({count} colors):\n\n"
        for c in colors:
            text += f"  🟦 `{c}`\n"
        await message.edit(text)

    register_command("Tools", "palette", "Generate random color palette", [])

    # 98. CONTRAST
    @app.on_message(filters.command("contrast", prefixes=".") & filters.me)
    async def contrast_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.contrast <#hex1> <#hex2>`")
            return
        def _parse_hex(h):
            h = h.strip().lstrip("#")
            return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        try:
            r1, g1, b1 = _parse_hex(args[1])
            r2, g2, b2 = _parse_hex(args[2])
            # Relative luminance
            def _lum(r, g, b):
                return 0.2126 * r/255 + 0.7152 * g/255 + 0.0722 * b/255
            l1, l2 = _lum(r1, g1, b1), _lum(r2, g2, b2)
            ratio = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
            if ratio >= 7:
                grade = "AAA ✅"
            elif ratio >= 4.5:
                grade = "AA ✅"
            elif ratio >= 3:
                grade = "AA Large ⚠️"
            else:
                grade = "Fail ❌"
            await message.edit(
                f"🎨 **Contrast Ratio**\n\n"
                f"🏷 `{args[1]}` vs `{args[2]}`\n"
                f"📊 Ratio: `{ratio:.2f}:1`\n"
                f"📋 WCAG: **{grade}**"
            )
        except (ValueError, IndexError):
            await message.edit("❌ Invalid hex colors.")

    register_command("Tools", "contrast", "Check WCAG contrast ratio between two colors", [])

    # 99. LOREM
    _LOREM = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor "
        "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
        "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure "
        "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt "
        "mollit anim id est laborum. Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. "
        "Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis "
        "sollicitudin mauris. Integer in mauris eu nibh euismod gravida. Duis ac tellus et risus "
        "vulputate vehicula."
    )

    @app.on_message(filters.command("lorem", prefixes=".") & filters.me)
    async def lorem_cmd(client, message):
        args = message.text.split(None, 1)
        words = 50
        if len(args) > 1:
            try:
                words = int(args[1])
                words = max(1, min(words, 200))
            except ValueError:
                pass
        all_words = _LOREM.split()
        result = " ".join(all_words[:words])
        if words > len(all_words):
            while len(result.split()) < words:
                result += " " + random.choice(all_words)
            result = " ".join(result.split()[:words])
        await message.edit(f"📝 **Lorem Ipsum** ({words} words):\n\n{result}")

    register_command("Tools", "lorem", "Generate Lorem Ipsum text", [])

    # 100. UUIDV4
    @app.on_message(filters.command("uuidv4", prefixes=".") & filters.me)
    async def uuidv4_cmd(client, message):
        args = message.text.split(None, 1)
        count = 1
        if len(args) > 1:
            try:
                count = int(args[1])
                count = max(1, min(count, 10))
            except ValueError:
                pass
        uuids = [str(_uuid.uuid4()) for _ in range(count)]
        text = "🆔 **UUID v4:**\n\n" + "\n".join(f"  `{u}`" for u in uuids)
        await message.edit(text)

    register_command("Tools", "uuidv4", "Generate UUID v4(s)", [])

    # 101. TIMESTAMP2DATE
    @app.on_message(filters.command("timestamp2date", prefixes=".") & filters.me)
    async def timestamp2date_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.timestamp2date <unix_timestamp>`")
            return
        try:
            ts = float(args[1])
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            await message.edit(
                f"📅 **Timestamp → Date:**\n\n"
                f"🕐 `{ts}` → `{dt.strftime('%Y-%m-%d %H:%M:%S')} UTC`\n"
                f"📋 ISO: `{dt.isoformat()}`"
            )
        except (ValueError, OSError, OverflowError):
            await message.edit("❌ Invalid timestamp.")

    register_command("Tools", "timestamp2date", "Convert Unix timestamp to date", [])

    # 102. DATE2TIMESTAMP
    @app.on_message(filters.command("date2timestamp", prefixes=".") & filters.me)
    async def date2timestamp_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.date2timestamp <YYYY-MM-DD HH:MM>`")
            return
        try:
            dt = datetime.strptime(args[1].strip(), "%Y-%m-%d %H:%M")
            ts = int(dt.replace(tzinfo=timezone.utc).timestamp())
            await message.edit(f"📅 **Date → Timestamp:**\n\n`{args[1]}` → `{ts}`")
        except ValueError:
            await message.edit("❌ Invalid date. Use `YYYY-MM-DD HH:MM` format.")

    register_command("Tools", "date2timestamp", "Convert date to Unix timestamp", [])

    # ═══════════════════════════════════════════════════════════════
    #  CODES (9 commands)
    # ═══════════════════════════════════════════════════════════════

    # 103. DATAMATRIX
    @app.on_message(filters.command("datamatrix", prefixes=".") & filters.me)
    async def datamatrix_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.datamatrix <text>`")
            return
        try:
            import qrcode
            from io import BytesIO
            img = qrcode.make(args[1], version=1, box_size=5)
            bio = BytesIO()
            bio.name = "datamatrix.png"
            img.save(bio, "PNG")
            bio.seek(0)
            await message.delete()
            await client.send_photo(message.chat.id, bio, caption=f"📊 **DataMatrix (QR) for:** `{args[1][:50]}`")
        except ImportError:
            await message.edit("❌ `qrcode` library not installed. `pip install qrcode[pil]`")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "datamatrix", "Generate DataMatrix-style code", [])

    # 104. AZTEC
    @app.on_message(filters.command("aztec", prefixes=".") & filters.me)
    async def aztec_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.aztec <text>`")
            return
        try:
            import qrcode
            from io import BytesIO
            img = qrcode.make(args[1], version=1, box_size=5)
            bio = BytesIO()
            bio.name = "aztec.png"
            img.save(bio, "PNG")
            bio.seek(0)
            await message.delete()
            await client.send_photo(message.chat.id, bio, caption=f"📊 **Aztec (QR) for:** `{args[1][:50]}`")
        except ImportError:
            await message.edit("❌ `qrcode` library not installed. `pip install qrcode[pil]`")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "aztec", "Generate Aztec-style code", [])

    # 105. ISBN_VALIDATE
    @app.on_message(filters.command("isbn_validate", prefixes=".") & filters.me)
    async def isbn_validate_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.isbn_validate <ISBN>`")
            return
        isbn = args[1].strip().replace("-", "").replace(" ", "")
        is_isbn13 = len(isbn) == 13
        is_isbn10 = len(isbn) == 10
        if not is_isbn10 and not is_isbn13:
            await message.edit("❌ ISBN must be 10 or 13 digits.")
            return
        try:
            if is_isbn10:
                total = sum(int(isbn[i]) * (10 - i) for i in range(9))
                check = (11 - total % 11) % 11
                expected = "X" if check == 10 else str(check)
                valid = isbn[9].upper() == expected
                await message.edit(f"📚 **ISBN-10:** `{args[1]}` — {'✅ Valid' if valid else '❌ Invalid'}\nExpected check digit: `{expected}`")
            else:
                total = sum(int(isbn[i]) * (1 if i % 2 == 0 else 3) for i in range(12))
                check = (10 - total % 10) % 10
                valid = int(isbn[12]) == check
                await message.edit(f"📚 **ISBN-13:** `{args[1]}` — {'✅ Valid' if valid else '❌ Invalid'}\nExpected check digit: `{check}`")
        except (ValueError, IndexError):
            await message.edit("❌ Invalid ISBN format.")

    register_command("Tools", "isbn_validate", "Validate ISBN-10 or ISBN-13", [])

    # 106. CREDITCARD_VALIDATE (Luhn)
    @app.on_message(filters.command("creditcard_validate", prefixes=".") & filters.me)
    async def creditcard_validate_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.creditcard_validate <number>`")
            return
        num = args[1].strip().replace("-", "").replace(" ", "")
        if not num.isdigit() or len(num) < 13 or len(num) > 19:
            await message.edit("❌ Invalid card number length (13-19 digits).")
            return
        # Luhn algorithm
        total = 0
        reverse_digits = [int(d) for d in num[::-1]]
        for i, d in enumerate(reverse_digits):
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        valid = total % 10 == 0
        # Identify card type
        card_type = "Unknown"
        if num.startswith("4"):
            card_type = "Visa"
        elif num.startswith(("51", "52", "53", "54", "55")):
            card_type = "Mastercard"
        elif num.startswith(("34", "37")):
            card_type = "Amex"
        elif num.startswith("6011") or num.startswith("65"):
            card_type = "Discover"
        await message.edit(
            f"💳 **Card Validation**\n\n"
            f"🔢 Number: `{'*' * (len(num) - 4)}{num[-4:]}`\n"
            f"🏷 Type: `{card_type}`\n"
            f"📋 Luhn: {'✅ Valid' if valid else '❌ Invalid'}"
        )

    register_command("Tools", "creditcard_validate", "Validate credit card using Luhn algorithm", [])

    # 107. IBAN_VALIDATE
    @app.on_message(filters.command("iban_validate", prefixes=".") & filters.me)
    async def iban_validate_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.iban_validate <IBAN>`")
            return
        iban = args[1].strip().replace(" ", "").upper()
        if len(iban) < 15 or len(iban) > 34:
            await message.edit("❌ IBAN must be 15-34 characters.")
            return
        if not iban[:2].isalpha() or not iban[2:4].isdigit():
            await message.edit("❌ IBAN must start with 2 letters + 2 digits.")
            return
        # Basic checksum: move first 4 chars to end, replace letters with numbers
        rearranged = iban[4:] + iban[:4]
        numeric = ""
        for c in rearranged:
            if c.isdigit():
                numeric += c
            elif c.isalpha():
                numeric += str(ord(c) - ord("A") + 10)
            else:
                await message.edit("❌ Invalid IBAN character.")
                return
        try:
            valid = int(numeric) % 97 == 1
        except ValueError:
            valid = False
        await message.edit(
            f"🏦 **IBAN Validation**\n\n"
            f"📋 IBAN: `{iban[:4]}{'*' * (len(iban) - 8)}{iban[-4:]}`\n"
            f"🌍 Country: `{iban[:2]}`\n"
            f"📋 Checksum: {'✅ Valid' if valid else '❌ Invalid'}"
        )

    register_command("Tools", "iban_validate", "Validate IBAN checksum", [])

    # 108. VIN_DECODE
    @app.on_message(filters.command("vin_decode", prefixes=".") & filters.me)
    async def vin_decode_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.vin_decode <VIN>`")
            return
        vin = args[1].strip().upper()
        if len(vin) != 17:
            await message.edit("❌ VIN must be exactly 17 characters.")
            return
        wmi = vin[:3]
        vds = vin[3:9]
        vis = vin[9:17]
        model_year_codes = "ABCDEFGHJKLMNPRSTVWXY123456789"
        year_char = vin[9]
        if year_char.isdigit():
            year = 2010 + int(year_char)
        elif year_char in model_year_codes:
            year = 2010 + model_year_codes.index(year_char)
            if year > datetime.now().year + 1:
                year -= 30
        else:
            year = "Unknown"
        region_map = {
            "1": "North America", "2": "North America", "3": "North America",
            "4": "North America", "5": "North America", "6": "Oceania",
            "7": "Oceania", "8": "South America", "9": "South America",
            "A": "Africa", "B": "Africa", "C": "Africa", "D": "Africa",
            "E": "Africa", "F": "Africa", "G": "Africa", "H": "Africa",
            "J": "Asia", "K": "Asia", "L": "Asia", "M": "Asia",
            "N": "Asia", "P": "Asia", "R": "Asia", "S": "Europe",
            "T": "Europe", "U": "Europe", "V": "Europe", "W": "Europe",
            "X": "Europe", "Y": "Europe", "Z": "Europe",
        }
        region = region_map.get(vin[0], "Unknown")
        await message.edit(
            f"🚗 **VIN Decode**\n\n"
            f"📋 VIN: `{vin}`\n"
            f"🏷 WMI (Manufacturer): `{wmi}`\n"
            f"🔧 VDS (Descriptor): `{vds}`\n"
            f"📅 VIS (Serial): `{vis}`\n"
            f"🌍 Region: `{region}`\n"
            f"📆 Model Year: `{year}`"
        )

    register_command("Tools", "vin_decode", "Decode a Vehicle Identification Number", [])

    # 109. BARCODE_GEN
    @app.on_message(filters.command("barcode_gen", prefixes=".") & filters.me)
    async def barcode_gen_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.barcode_gen <text>`")
            return
        try:
            import qrcode
            from io import BytesIO
            img = qrcode.make(args[1], version=1, box_size=5)
            bio = BytesIO()
            bio.name = "barcode.png"
            img.save(bio, "PNG")
            bio.seek(0)
            await message.delete()
            await client.send_photo(message.chat.id, bio, caption=f"📊 **Barcode for:** `{args[1][:50]}`")
        except ImportError:
            await message.edit("❌ `qrcode` library not installed. `pip install qrcode[pil]`")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "barcode_gen", "Generate a barcode image", [])

    # 110. UPC_CHECK
    @app.on_message(filters.command("upc_check", prefixes=".") & filters.me)
    async def upc_check_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.upc_check <12-digit UPC>`")
            return
        upc = args[1].strip().replace("-", "").replace(" ", "")
        if len(upc) != 12 or not upc.isdigit():
            await message.edit("❌ UPC-A must be exactly 12 digits.")
            return
        total = sum(int(upc[i]) * (3 if i % 2 else 1) for i in range(11))
        check = (10 - total % 10) % 10
        valid = int(upc[11]) == check
        await message.edit(
            f"📊 **UPC-A Check**\n\n"
            f"📋 Code: `{upc}`\n"
            f"🔢 Expected check digit: `{check}`\n"
            f"📋 Result: {'✅ Valid' if valid else '❌ Invalid'}"
        )

    register_command("Tools", "upc_check", "Validate UPC-A check digit", [])

    # 111. EAN_CHECK
    @app.on_message(filters.command("ean_check", prefixes=".") & filters.me)
    async def ean_check_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.ean_check <13-digit EAN>`")
            return
        ean = args[1].strip().replace("-", "").replace(" ", "")
        if len(ean) != 13 or not ean.isdigit():
            await message.edit("❌ EAN-13 must be exactly 13 digits.")
            return
        total = sum(int(ean[i]) * (1 if i % 2 == 0 else 3) for i in range(12))
        check = (10 - total % 10) % 10
        valid = int(ean[12]) == check
        await message.edit(
            f"📊 **EAN-13 Check**\n\n"
            f"📋 Code: `{ean}`\n"
            f"🔢 Expected check digit: `{check}`\n"
            f"📋 Result: {'✅ Valid' if valid else '❌ Invalid'}"
        )

    register_command("Tools", "ean_check", "Validate EAN-13 check digit", [])

    # ═══════════════════════════════════════════════════════════════
    #  OTHER (8 commands)
    # ═══════════════════════════════════════════════════════════════

    # 112. ZIPINFO
    @app.on_message(filters.command("zipinfo", prefixes=".") & filters.me)
    async def zipinfo_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.zipinfo <path_to_zip>`")
            return
        path = args[1].strip()
        if not os.path.exists(path):
            await message.edit(f"❌ File not found: `{path}`")
            return
        try:
            import zipfile
            with zipfile.ZipFile(path, "r") as zf:
                text = f"📦 **ZIP Info: `{os.path.basename(path)}`**\n\n"
                text += f"📋 Files: `{len(zf.namelist())}`\n"
                total_size = sum(i.file_size for i in zf.infolist())
                comp_size = sum(i.compress_size for i in zf.infolist())
                text += f"📊 Original: `{total_size:,}` bytes\n"
                text += f"🗜 Compressed: `{comp_size:,}` bytes\n"
                if total_size > 0:
                    text += f"📉 Ratio: `{(1 - comp_size / total_size) * 100:.1f}%`\n\n"
                else:
                    text += "\n"
                text += "**Contents:**\n"
                for info in zf.infolist()[:20]:
                    text += f"  • `{info.filename}` ({info.file_size:,} bytes)\n"
                if len(zf.namelist()) > 20:
                    text += f"  ... and {len(zf.namelist()) - 20} more"
                await message.edit(text)
        except zipfile.BadZipFile:
            await message.edit("❌ Not a valid ZIP file.")
        except Exception as e:
            await message.edit(f"❌ **Error:** `{e}`")

    register_command("Tools", "zipinfo", "Show info about a ZIP file", [])

    # 113. JSON_FORMAT / JSONFMT
    @app.on_message(filters.command(["json_format", "jsonfmt"], prefixes=".") & filters.me)
    async def json_format_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.jsonfmt <json_string>`")
            return
        try:
            parsed = json.loads(args[1])
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            await message.edit(f"📋 **Formatted JSON:**\n```json\n{formatted}\n```")
        except json.JSONDecodeError as e:
            await message.edit(f"❌ **JSON Error:** `{e}`")

    register_command("Tools", "json_format", "Pretty-format JSON", ["jsonfmt"])

    # 114. XML_FORMAT / XMLFMT
    @app.on_message(filters.command(["xml_format", "xmlfmt"], prefixes=".") & filters.me)
    async def xml_format_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.xmlfmt <xml_string>`")
            return
        try:
            import xml.dom.minidom
            dom = xml.dom.minidom.parseString(args[1])
            formatted = dom.toprettyxml(indent="  ")
            # Remove extra blank lines
            lines = [l for l in formatted.split("\n") if l.strip()]
            await message.edit(f"📋 **Formatted XML:**\n```xml\n{chr(10).join(lines)}\n```")
        except Exception as e:
            await message.edit(f"❌ **XML Error:** `{e}`")

    register_command("Tools", "xml_format", "Pretty-format XML", ["xmlfmt"])

    # 115. CSV_FORMAT / CSVFMT
    @app.on_message(filters.command(["csv_format", "csvfmt"], prefixes=".") & filters.me)
    async def csv_format_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.csvfmt <csv_string>`")
            return
        try:
            import csv
            from io import StringIO
            reader = csv.reader(StringIO(args[1]))
            rows = list(reader)
            if not rows:
                await message.edit("❌ No CSV data found.")
                return
            # Calculate column widths
            col_widths = [0] * len(rows[0])
            for row in rows:
                for i, cell in enumerate(row):
                    if i < len(col_widths):
                        col_widths[i] = max(col_widths[i], len(cell))
            # Format as table
            text = "📋 **Formatted CSV:**\n\n```\n"
            for idx, row in enumerate(rows):
                line = " | ".join(
                    cell.ljust(col_widths[i]) if i < len(col_widths) else cell
                    for i, cell in enumerate(row)
                )
                text += line + "\n"
                if idx == 0:
                    text += "-+-".join("-" * w for w in col_widths) + "\n"
            text += "```"
            await message.edit(text)
        except Exception as e:
            await message.edit(f"❌ **CSV Error:** `{e}`")

    register_command("Tools", "csv_format", "Pretty-format CSV as table", ["csvfmt"])

    # 116. MARKDOWN_PREVIEW / MD
    @app.on_message(filters.command(["markdown_preview", "md"], prefixes=".") & filters.me)
    async def markdown_preview_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.md <markdown_text>`")
            return
        # Just re-send as markdown (Telegram will render it)
        await message.delete()
        await client.send_message(message.chat.id, args[1])

    register_command("Tools", "markdown_preview", "Preview markdown by sending it", ["md"])

    # 117. REGEX_TEST / REGEXTEST
    @app.on_message(filters.command(["regex_test", "regextest"], prefixes=".") & filters.me)
    async def regex_test_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.regextest <pattern> <text>`\nExample: `.regextest \\d+ abc123def`")
            return
        pattern = args[1]
        text_val = args[2]
        try:
            matches = list(re.finditer(pattern, text_val))
            if not matches:
                await message.edit(f"🔍 Pattern `{pattern}` — **No matches** in text.")
                return
            text = f"🔍 **Regex Test**\n\nPattern: `{pattern}`\nText: `{text_val}`\n\n**Matches ({len(matches)}):**\n"
            for i, m in enumerate(matches[:20], 1):
                text += f"  {i}. `{m.group()}` (pos {m.start()}-{m.end()})\n"
            await message.edit(text)
        except re.error as e:
            await message.edit(f"❌ **Regex Error:** `{e}`")

    register_command("Tools", "regex_test", "Test a regex pattern against text", ["regextest"])

    # 118. BASE_CONVERT
    @app.on_message(filters.command("base_convert", prefixes=".") & filters.me)
    async def base_convert_cmd(client, message):
        args = message.text.split(None, 3)
        if len(args) < 4:
            await message.edit("❌ **Usage:** `.base_convert <number> <from_base> <to_base>`\nExample: `.base_convert FF 16 10`")
            return
        try:
            number = args[1].strip()
            from_base = int(args[2])
            to_base = int(args[3])
            if not (2 <= from_base <= 36) or not (2 <= to_base <= 36):
                await message.edit("❌ Bases must be between 2 and 36.")
                return
            # Convert to decimal first
            decimal = int(number, from_base)
            # Convert from decimal to target base
            if to_base == 10:
                result = str(decimal)
            else:
                digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                if decimal == 0:
                    result = "0"
                else:
                    temp = ""
                    n = decimal
                    while n > 0:
                        temp = digits[n % to_base] + temp
                        n //= to_base
                    result = temp
            await message.edit(f"🔄 `{number}` (base {from_base}) → `{result}` (base {to_base})")
        except ValueError:
            await message.edit("❌ Invalid number or base.")

    register_command("Tools", "base_convert", "Convert number between bases (2-36)", [])

    # 119. MATH_CONSTANTS
    @app.on_message(filters.command("math_constants", prefixes=".") & filters.me)
    async def math_constants_cmd(client, message):
        text = "📐 **Math Constants**\n\n"
        for name, val in _MATH_CONSTANTS.items():
            text += f"  • **{name}** = `{val}`\n"
        await message.edit(text)

    register_command("Tools", "math_constants", "Show common math constants", [])
