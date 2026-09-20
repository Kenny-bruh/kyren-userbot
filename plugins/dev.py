"""
KyrenUB - Developer Tools Plugin
=================================
100+ developer-focused commands: API testing, format converters,
code tools, package info, crypto hashes, network tools, DB tools,
regex tools, time utilities, and misc dev helpers.
"""

def register(app):
    from pyrogram import filters
    from plugins import register_command
    import asyncio, os, sys, json, re, hashlib, hmac as _hmac
    import base64, binascii, time, datetime, struct, uuid, random
    import string, secrets, subprocess, socket, ssl, urllib.parse
    import urllib.request, urllib.error
    from email.message import Message as _EmailMsg
    import zlib

    # ─────────── API TESTING (15) ───────────

    @app.on_message(filters.command("get", prefixes=".") & filters.me)
    async def _get_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.get <url>`")
        url = message.command[1]
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read(8000).decode("utf-8", errors="ignore")
                await message.reply(f"**GET** {url}\nStatus: {r.status}\n```\n{body[:3000]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "get", "HTTP GET request", [])

    @app.on_message(filters.command("post", prefixes=".") & filters.me)
    async def _post_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.post <url> <json_data>`")
        url = message.command[1]
        try:
            data = json.loads(" ".join(message.command[2:]).encode().decode("unicode_escape"))
            req = urllib.request.Request(url, data=json.dumps(data).encode(),
                                          headers={"User-Agent": "KyrenUB/2.0", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                body = r.read(3000).decode("utf-8", errors="ignore")
                await message.reply(f"**POST** {url}\nStatus: {r.status}\n```\n{body[:2500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "post", "HTTP POST request with JSON", [])

    @app.on_message(filters.command("put", prefixes=".") & filters.me)
    async def _put_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.put <url> <json_data>`")
        url = message.command[1]
        try:
            data = json.loads(" ".join(message.command[2:]))
            req = urllib.request.Request(url, data=json.dumps(data).encode(), method="PUT",
                                          headers={"User-Agent": "KyrenUB/2.0", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                await message.reply(f"**PUT** {url}\nStatus: {r.status}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "put", "HTTP PUT request", [])

    @app.on_message(filters.command("delete", prefixes=".") & filters.me)
    async def _delete_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.delete <url>`")
        url = message.command[1]
        try:
            req = urllib.request.Request(url, method="DELETE", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                await message.reply(f"**DELETE** {url}\nStatus: {r.status}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "delete", "HTTP DELETE request", [])

    @app.on_message(filters.command("patch", prefixes=".") & filters.me)
    async def _patch_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.patch <url> <json_data>`")
        url = message.command[1]
        try:
            data = json.loads(" ".join(message.command[2:]))
            req = urllib.request.Request(url, data=json.dumps(data).encode(), method="PATCH",
                                          headers={"User-Agent": "KyrenUB/2.0", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                await message.reply(f"**PATCH** {url}\nStatus: {r.status}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "patch", "HTTP PATCH request", [])

    @app.on_message(filters.command("head", prefixes=".") & filters.me)
    async def _head_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.head <url>`")
        url = message.command[1]
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                headers = "\n".join(f"{k}: {v}" for k, v in r.headers.items())
                await message.reply(f"**HEAD** {url}\nStatus: {r.status}\n```\n{headers}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "head", "HTTP HEAD request", [])

    @app.on_message(filters.command("options", prefixes=".") & filters.me)
    async def _options_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.options <url>`")
        url = message.command[1]
        try:
            req = urllib.request.Request(url, method="OPTIONS", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                allow = r.headers.get("Allow", "N/A")
                await message.reply(f"**OPTIONS** {url}\nStatus: {r.status}\nAllow: {allow}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "options", "HTTP OPTIONS request", [])

    @app.on_message(filters.command("curl2", prefixes=".") & filters.me)
    async def _curl2_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.curl2 <url>`")
        url = message.command[1]
        try:
            result = subprocess.run(["curl", "-sIL", url], capture_output=True, text=True, timeout=15)
            await message.reply(f"```\n{result.stdout[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "curl2", "Curl headers", [])

    @app.on_message(filters.command("headers2", prefixes=".") & filters.me)
    async def _headers2_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.headers2 <url>`")
        url = message.command[1]
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                txt = "\n".join(f"{k}: {v}" for k, v in r.headers.items())
                await message.reply(f"```\n{txt}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "headers2", "Get HTTP headers", [])

    @app.on_message(filters.command("sslinfo", prefixes=".") & filters.me)
    async def _sslinfo_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.sslinfo <domain>`")
        domain = message.command[1]
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            subject = dict(x[0] for x in cert["subject"])
            issuer = dict(x[0] for x in cert["issuer"])
            await message.reply(
                f"**SSL Cert for {domain}**\n"
                f"Subject: {subject.get('commonName')}\n"
                f"Issuer: {issuer.get('commonName')}\n"
                f"Valid From: {cert['notBefore']}\n"
                f"Valid To: {cert['notAfter']}\n"
                f"Serial: {cert['serialNumber']}"
            )
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "sslinfo", "SSL certificate info", [])

    @app.on_message(filters.command("certinfo", prefixes=".") & filters.me)
    async def _certinfo_cmd(client, message):
        await _sslinfo_cmd(client, message)
    register_command("Dev", "certinfo", "Alias for sslinfo", [])

    @app.on_message(filters.command("webhook", prefixes=".") & filters.me)
    async def _webhook_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.webhook <url> <json>`")
        url = message.command[1]
        try:
            data = json.loads(" ".join(message.command[2:]))
            req = urllib.request.Request(url, data=json.dumps(data).encode(),
                                          headers={"User-Agent": "KyrenUB/2.0", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                await message.reply(f"Webhook sent!\nStatus: {r.status}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "webhook", "Send webhook", [])

    @app.on_message(filters.command("status2", prefixes=".") & filters.me)
    async def _status2_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.status2 <url>`")
        url = message.command[1]
        try:
            req = urllib.request.Request(url, method="GET", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                await message.reply(f"{url}\nStatus: {r.status} {r.reason}")
        except urllib.error.HTTPError as e:
            await message.reply(f"{url}\nStatus: {e.code} {e.reason}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "status2", "Get HTTP status", [])

    @app.on_message(filters.command("apitest", prefixes=".") & filters.me)
    async def _apitest_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.apitest <url>`")
        url = message.command[1]
        try:
            start = time.time()
            req = urllib.request.Request(url, headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                elapsed = round((time.time() - start) * 1000, 2)
                body = r.read(2000).decode("utf-8", errors="ignore")
                await message.reply(
                    f"**API Test** {url}\n"
                    f"Status: {r.status}\nTime: {elapsed}ms\nSize: {len(body)} bytes\n```\n{body[:1500]}\n```"
                )
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "apitest", "Test an API endpoint", [])

    @app.on_message(filters.command("rest", prefixes=".") & filters.me)
    async def _rest_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.rest <METHOD> <url>` (METHOD: GET/POST/PUT/DELETE)")
        method = message.command[1].upper()
        url = message.command[2]
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                await message.reply(f"**{method}** {url}\nStatus: {r.status}")
        except urllib.error.HTTPError as e:
            await message.reply(f"**{method}** {url}\nStatus: {e.code} {e.reason}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "rest", "REST API call", [])

    # ─────────── FORMAT CONVERTERS (15) ───────────

    def _json_to_yaml(data, indent=0):
        """Simple JSON to YAML converter."""
        result = []
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, (dict, list)):
                    result.append(f"{'  ' * indent}{k}:")
                    result.append(_json_to_yaml(v, indent + 1))
                else:
                    result.append(f"{'  ' * indent}{k}: {v}")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    result.append(f"{'  ' * indent}-")
                    result.append(_json_to_yaml(item, indent + 1))
                else:
                    result.append(f"{'  ' * indent}- {item}")
        return "\n".join(result)

    @app.on_message(filters.command("json2yaml", prefixes=".") & filters.me)
    async def _json2yaml_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to a JSON message")
        try:
            data = json.loads(message.reply_to_message.text)
            yaml_text = _json_to_yaml(data)
            await message.reply(f"```\n{yaml_text[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "json2yaml", "JSON to YAML", [])

    @app.on_message(filters.command("yaml2json", prefixes=".") & filters.me)
    async def _yaml2json_cmd(client, message):
        await message.reply("YAML parsing needs PyYAML. Install: `.pip install pyyaml` then use `.eval`")
    register_command("Dev", "yaml2json", "YAML to JSON (needs pyyaml)", [])

    @app.on_message(filters.command("json2csv", prefixes=".") & filters.me)
    async def _json2csv_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to JSON array of objects")
        try:
            data = json.loads(message.reply_to_message.text)
            if not isinstance(data, list) or not data:
                return await message.reply("Need a JSON array of objects")
            import csv, io
            out = io.StringIO()
            w = csv.DictWriter(out, fieldnames=data[0].keys())
            w.writeheader()
            w.writerows(data)
            await message.reply(f"```\n{out.getvalue()[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "json2csv", "JSON array to CSV", [])

    @app.on_message(filters.command("csv2json", prefixes=".") & filters.me)
    async def _csv2json_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to CSV")
        try:
            import csv, io
            reader = csv.DictReader(io.StringIO(message.reply_to_message.text))
            data = list(reader)
            await message.reply(f"```\n{json.dumps(data, indent=2)[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "csv2json", "CSV to JSON", [])

    @app.on_message(filters.command("json2xml", prefixes=".") & filters.me)
    async def _json2xml_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to JSON")
        try:
            data = json.loads(message.reply_to_message.text)
            def _to_xml(d, root="root"):
                if isinstance(d, dict):
                    return f"<{root}>" + "".join(_to_xml(v, k) for k, v in d.items()) + f"</{root}>"
                elif isinstance(d, list):
                    return f"<{root}>" + "".join(_to_xml(i, "item") for i in d) + f"</{root}>"
                else:
                    return f"<{root}>{d}</{root}>"
            xml = _to_xml(data)
            await message.reply(f"```\n{xml[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "json2xml", "JSON to XML", [])

    @app.on_message(filters.command("xml2json", prefixes=".") & filters.me)
    async def _xml2json_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to XML")
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(message.reply_to_message.text)
            def _to_json(el):
                d = {}
                for child in el:
                    d[child.tag] = _to_json(child) if len(child) else child.text
                return d or el.text
            data = {root.tag: _to_json(root)}
            await message.reply(f"```\n{json.dumps(data, indent=2)[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "xml2json", "XML to JSON", [])

    @app.on_message(filters.command("jsonmin", prefixes=".") & filters.me)
    async def _jsonmin_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to JSON")
        try:
            data = json.loads(message.reply_to_message.text)
            await message.reply(f"```\n{json.dumps(data, separators=(',', ':'))[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "jsonmin", "Minify JSON", [])

    @app.on_message(filters.command("jsonbeautify", prefixes=".") & filters.me)
    async def _jsonbeautify_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to JSON")
        try:
            data = json.loads(message.reply_to_message.text)
            await message.reply(f"```\n{json.dumps(data, indent=4)[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "jsonbeautify", "Beautify JSON", [])

    @app.on_message(filters.command("xmlmin", prefixes=".") & filters.me)
    async def _xmlmin_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to XML")
        try:
            text = re.sub(r">\s+<", "><", message.reply_to_message.text)
            text = re.sub(r"\s+", " ", text).strip()
            await message.reply(f"```\n{text[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "xmlmin", "Minify XML", [])

    @app.on_message(filters.command("cssmin", prefixes=".") & filters.me)
    async def _cssmin_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to CSS")
        try:
            text = re.sub(r"/\*.*?\*/", "", message.reply_to_message.text, flags=re.DOTALL)
            text = re.sub(r"\s+", " ", text)
            text = re.sub(r"\s*([{}:;,])\s*", r"\1", text).strip()
            await message.reply(f"```\n{text[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "cssmin", "Minify CSS", [])

    @app.on_message(filters.command("jsmin", prefixes=".") & filters.me)
    async def _jsmin_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to JS")
        try:
            text = re.sub(r"//.*", "", message.reply_to_message.text)
            text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
            text = re.sub(r"\s+", " ", text).strip()
            await message.reply(f"```\n{text[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "jsmin", "Minify JS (basic)", [])

    @app.on_message(filters.command("htmlmin", prefixes=".") & filters.me)
    async def _htmlmin_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to HTML")
        try:
            text = re.sub(r"<!--.*?-->", "", message.reply_to_message.text, flags=re.DOTALL)
            text = re.sub(r">\s+<", "><", text)
            text = re.sub(r"\s+", " ", text).strip()
            await message.reply(f"```\n{text[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "htmlmin", "Minify HTML", [])

    @app.on_message(filters.command("sqlformat", prefixes=".") & filters.me)
    async def _sqlformat_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to SQL")
        try:
            sql = message.reply_to_message.text
            for kw in ["SELECT", "FROM", "WHERE", "AND", "OR", "ORDER BY", "GROUP BY", "LIMIT", "INSERT INTO", "VALUES", "UPDATE", "SET", "DELETE FROM"]:
                sql = re.sub(rf"\b{kw}\b", f"\n{kw}", sql, flags=re.IGNORECASE)
            await message.reply(f"```sql\n{sql.strip()[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "sqlformat", "Format SQL", [])

    @app.on_message(filters.command("md2html", prefixes=".") & filters.me)
    async def _md2html_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to Markdown")
        try:
            md = message.reply_to_message.text
            md = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", md)
            md = re.sub(r"\*(.+?)\*", r"<i>\1</i>", md)
            md = re.sub(r"`(.+?)`", r"<code>\1</code>", md)
            md = re.sub(r"^# (.+)", r"<h1>\1</h1>", md, flags=re.MULTILINE)
            md = re.sub(r"^## (.+)", r"<h2>\1</h2>", md, flags=re.MULTILINE)
            md = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', md)
            await message.reply(f"```\n{md[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "md2html", "Markdown to HTML", [])

    @app.on_message(filters.command("html2md", prefixes=".") & filters.me)
    async def _html2md_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to HTML")
        try:
            html = message.reply_to_message.text
            html = re.sub(r"<b>(.+?)</b>", r"**\1**", html)
            html = re.sub(r"<strong>(.+?)</strong>", r"**\1**", html)
            html = re.sub(r"<i>(.+?)</i>", r"*\1*", html)
            html = re.sub(r"<em>(.+?)</em>", r"*\1*", html)
            html = re.sub(r"<code>(.+?)</code>", r"`\1`", html)
            html = re.sub(r"<h1>(.+?)</h1>", r"# \1", html)
            html = re.sub(r"<h2>(.+?)</h2>", r"## \1", html)
            html = re.sub(r'<a href="(.+?)">(.+?)</a>', r"[\2](\1)", html)
            html = re.sub(r"<[^>]+>", "", html)
            await message.reply(html[:3500])
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "html2md", "HTML to Markdown", [])

    # ─────────── CODE TOOLS (10) ───────────

    @app.on_message(filters.command("paste", prefixes=".") & filters.me)
    async def _paste_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to text/code to paste")
        try:
            data = urllib.parse.urlencode({"content": message.reply_to_message.text}).encode()
            req = urllib.request.Request("https://dpaste.org/api/", data=data,
                                          headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                link = r.read().decode().strip()
                await message.reply(f"Pastebin: {link}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "paste", "Paste code to dpaste.org", [])

    @app.on_message(filters.command("snippet", prefixes=".") & filters.me)
    async def _snippet_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.snippet save <name>` (reply to code) or `.snippet get <name>` or `.snippet list`")
        action = message.command[1]
        path = "/tmp/kyren_snippets.json"
        snippets = {}
        if os.path.exists(path):
            with open(path) as f:
                snippets = json.load(f)
        if action == "save":
            if len(message.command) < 3 or not message.reply_to_message:
                return await message.reply("Reply to code with `.snippet save <name>`")
            name = message.command[2]
            snippets[name] = message.reply_to_message.text
            with open(path, "w") as f:
                json.dump(snippets, f)
            await message.reply(f"Snippet '{name}' saved!")
        elif action == "get":
            if len(message.command) < 3:
                return await message.reply("Usage: `.snippet get <name>`")
            name = message.command[2]
            if name in snippets:
                await message.reply(f"```\n{snippets[name][:3500]}\n```")
            else:
                await message.reply("Snippet not found")
        elif action == "list":
            if not snippets:
                return await message.reply("No snippets saved")
            await message.reply("Snippets:\n" + "\n".join(f"• {n}" for n in snippets))
        elif action == "del":
            if len(message.command) < 3:
                return await message.reply("Usage: `.snippet del <name>`")
            name = message.command[2]
            if name in snippets:
                del snippets[name]
                with open(path, "w") as f:
                    json.dump(snippets, f)
                await message.reply(f"Deleted '{name}'")
            else:
                await message.reply("Not found")
    register_command("Dev", "snippet", "Save/get code snippets", [])

    @app.on_message(filters.command("loc", prefixes=".") & filters.me)
    async def _loc_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to code")
        text = message.reply_to_message.text
        lines = text.split("\n")
        chars = len(text)
        words = len(text.split())
        await message.reply(f"Lines: {len(lines)}\nChars: {chars}\nWords: {words}")
    register_command("Dev", "loc", "Lines of code counter", [])

    @app.on_message(filters.command("ascii_table", prefixes=".") & filters.me)
    async def _ascii_table_cmd(client, message):
        table = (
            "**ASCII Table**\n```\n"
            "DEC  HEX  OCT  CHAR\n"
            + "\n".join(f"{i:3d}  {i:02X}  {i:03o}  {chr(i) if 32 <= i < 127 else '?'}" for i in range(32, 127))
            + "\n```"
        )
        await message.reply(table)
    register_command("Dev", "ascii_table", "Show ASCII table", [])

    @app.on_message(filters.command("cron_explain", prefixes=".") & filters.me)
    async def _cron_explain_cmd(client, message):
        if len(message.command) < 6:
            return await message.reply("Usage: `.cron_explain <min> <hour> <day> <month> <weekday>`\nExample: `.cron_explain 0 9 * * *`")
        parts = message.command[1:6]
        names = ["Minute", "Hour", "Day of month", "Month", "Day of week"]
        explanation = "Cron expression breakdown:\n" + "\n".join(f"{n}: {p}" for n, p in zip(names, parts))
        await message.reply(explanation)
    register_command("Dev", "cron_explain", "Explain cron expression", [])

    @app.on_message(filters.command("color_conv", prefixes=".") & filters.me)
    async def _color_conv_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.color_conv #ff0000` or `.color_conv 255,0,0`")
        arg = message.command[1]
        try:
            if arg.startswith("#"):
                hex_val = arg.lstrip("#")
                r = int(hex_val[0:2], 16)
                g = int(hex_val[2:4], 16)
                b = int(hex_val[4:6], 16)
            else:
                r, g, b = map(int, arg.split(","))
            await message.reply(f"HEX: #{r:02X}{g:02X}{b:02X}\nRGB: {r},{g},{b}\nHSL: will add later")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "color_conv", "Color converter HEX/RGB", [])

    @app.on_message(filters.command("jwt_decode", prefixes=".") & filters.me)
    async def _jwt_decode_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.jwt_decode <token>`")
        token = message.command[1]
        try:
            parts = token.split(".")
            if len(parts) < 2:
                return await message.reply("Invalid JWT")
            def _decode(s):
                s += "=" * (4 - len(s) % 4)
                return base64.urlsafe_b64decode(s).decode("utf-8", errors="ignore")
            header = json.loads(_decode(parts[0]))
            payload = json.loads(_decode(parts[1]))
            await message.reply(f"**Header:**\n```json\n{json.dumps(header, indent=2)}\n```\n**Payload:**\n```json\n{json.dumps(payload, indent=2)}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "jwt_decode", "Decode JWT token", [])

    @app.on_message(filters.command("useragent", prefixes=".") & filters.me)
    async def _useragent_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.useragent <UA string>`")
        ua = " ".join(message.command[1:])
        info = {"browser": "Unknown", "os": "Unknown", "device": "Unknown"}
        if "Chrome" in ua: info["browser"] = "Chrome"
        elif "Firefox" in ua: info["browser"] = "Firefox"
        elif "Safari" in ua: info["browser"] = "Safari"
        if "Windows" in ua: info["os"] = "Windows"
        elif "Mac" in ua: info["os"] = "macOS"
        elif "Linux" in ua: info["os"] = "Linux"
        elif "Android" in ua: info["os"] = "Android"
        elif "iPhone" in ua or "iPad" in ua: info["os"] = "iOS"
        if "Mobile" in ua: info["device"] = "Mobile"
        else: info["device"] = "Desktop"
        await message.reply(f"UA: `{ua}`\nBrowser: {info['browser']}\nOS: {info['os']}\nDevice: {info['device']}")
    register_command("Dev", "useragent", "Parse User-Agent string", [])

    # ─────────── PACKAGE INFO (5) ───────────

    @app.on_message(filters.command("npm", prefixes=".") & filters.me)
    async def _npm_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.npm <package>`")
        pkg = message.command[1]
        try:
            req = urllib.request.Request(f"https://registry.npmjs.org/{pkg}", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            latest = data.get("dist-tags", {}).get("latest", "N/A")
            desc = data.get("description", "N/A")
            await message.reply(f"**npm: {pkg}**\nVersion: {latest}\nDesc: {desc}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "npm", "NPM package info", [])

    @app.on_message(filters.command("pypi", prefixes=".") & filters.me)
    async def _pypi_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.pypi <package>`")
        pkg = message.command[1]
        try:
            req = urllib.request.Request(f"https://pypi.org/pypi/{pkg}/json", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            info = data["info"]
            await message.reply(f"**PyPI: {pkg}**\nVersion: {info['version']}\nDesc: {info['summary']}\nAuthor: {info['author']}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "pypi", "PyPI package info", [])

    @app.on_message(filters.command("github_user", prefixes=".") & filters.me)
    async def _github_user_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.github_user <username>`")
        user = message.command[1]
        try:
            req = urllib.request.Request(f"https://api.github.com/users/{user}", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            await message.reply(
                f"**GitHub: {data['login']}**\nName: {data.get('name', 'N/A')}\n"
                f"Bio: {data.get('bio', 'N/A')}\nRepos: {data['public_repos']}\n"
                f"Followers: {data['followers']}\nFollowing: {data['following']}\n"
                f"URL: {data['html_url']}"
            )
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "github_user", "GitHub user info", [])

    @app.on_message(filters.command("github_repo", prefixes=".") & filters.me)
    async def _github_repo_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.github_repo <owner> <repo>`")
        owner, repo = message.command[1], message.command[2]
        try:
            req = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            await message.reply(
                f"**{data['full_name']}**\nDesc: {data.get('description', 'N/A')}\n"
                f"Stars: {data['stargazers_count']}\nForks: {data['forks_count']}\n"
                f"Language: {data.get('language', 'N/A')}\nURL: {data['html_url']}"
            )
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "github_repo", "GitHub repo info", [])

    @app.on_message(filters.command("dockerhub", prefixes=".") & filters.me)
    async def _dockerhub_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: `.dockerhub <image>`")
        img = message.command[1]
        try:
            req = urllib.request.Request(f"https://hub.docker.com/v2/repositories/library/{img}/", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            await message.reply(f"**Docker: {img}**\nPulls: {data.get('pull_count', 'N/A')}\nStars: {data.get('star_count', 'N/A')}\nDesc: {data.get('description', 'N/A')}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "dockerhub", "Docker Hub image info", [])

    # ─────────── CRYPTO HASHES (15) ───────────

    @app.on_message(filters.command("sha3_256", prefixes=".") & filters.me)
    async def _sha3_256_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            text = " ".join(message.command[1:]) if len(message.command) > 1 else ""
        else:
            text = message.reply_to_message.text
        if not text: return await message.reply("Reply to text or provide input")
        await message.reply(hashlib.sha3_256(text.encode()).hexdigest())
    register_command("Dev", "sha3_256", "SHA3-256 hash", [])

    @app.on_message(filters.command("sha3_512", prefixes=".") & filters.me)
    async def _sha3_512_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(hashlib.sha3_512(text.encode()).hexdigest())
    register_command("Dev", "sha3_512", "SHA3-512 hash", [])

    @app.on_message(filters.command("blake2", prefixes=".") & filters.me)
    async def _blake2_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(hashlib.blake2b(text.encode()).hexdigest())
    register_command("Dev", "blake2", "BLAKE2 hash", [])

    @app.on_message(filters.command("blake2s", prefixes=".") & filters.me)
    async def _blake2s_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(hashlib.blake2s(text.encode()).hexdigest())
    register_command("Dev", "blake2s", "BLAKE2s hash", [])

    @app.on_message(filters.command("crc32", prefixes=".") & filters.me)
    async def _crc32_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(f"{zlib.crc32(text.encode()) & 0xFFFFFFFF:08x}")
    register_command("Dev", "crc32", "CRC32 hash", [])

    @app.on_message(filters.command("adler32", prefixes=".") & filters.me)
    async def _adler32_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(f"{zlib.adler32(text.encode()) & 0xFFFFFFFF:08x}")
    register_command("Dev", "adler32", "Adler32 hash", [])

    @app.on_message(filters.command("hmac_gen", prefixes=".") & filters.me)
    async def _hmac_gen_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.hmac_gen <key> <message>`")
        key = message.command[1].encode()
        msg = " ".join(message.command[2:]).encode()
        await message.reply(_hmac.new(key, msg, hashlib.sha256).hexdigest())
    register_command("Dev", "hmac_gen", "HMAC-SHA256 generator", [])

    @app.on_message(filters.command("sha224", prefixes=".") & filters.me)
    async def _sha224_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(hashlib.sha224(text.encode()).hexdigest())
    register_command("Dev", "sha224", "SHA-224 hash", [])

    @app.on_message(filters.command("sha384", prefixes=".") & filters.me)
    async def _sha384_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(hashlib.sha384(text.encode()).hexdigest())
    register_command("Dev", "sha384", "SHA-384 hash", [])

    @app.on_message(filters.command("sha1_short", prefixes=".") & filters.me)
    async def _sha1_short_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(hashlib.sha1(text.encode()).hexdigest()[:12])
    register_command("Dev", "sha1_short", "Short SHA1 (git-style)", [])

    @app.on_message(filters.command("all_hashes", prefixes=".") & filters.me)
    async def _all_hashes_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        b = text.encode()
        result = "\n".join([
            f"MD5: {hashlib.md5(b).hexdigest()}",
            f"SHA1: {hashlib.sha1(b).hexdigest()}",
            f"SHA224: {hashlib.sha224(b).hexdigest()}",
            f"SHA256: {hashlib.sha256(b).hexdigest()}",
            f"SHA384: {hashlib.sha384(b).hexdigest()}",
            f"SHA512: {hashlib.sha512(b).hexdigest()}",
            f"SHA3-256: {hashlib.sha3_256(b).hexdigest()}",
            f"SHA3-512: {hashlib.sha3_512(b).hexdigest()}",
            f"BLAKE2b: {hashlib.blake2b(b).hexdigest()}",
            f"BLAKE2s: {hashlib.blake2s(b).hexdigest()}",
            f"CRC32: {zlib.crc32(b) & 0xFFFFFFFF:08x}",
            f"Adler32: {zlib.adler32(b) & 0xFFFFFFFF:08x}",
        ])
        await message.reply(result)
    register_command("Dev", "all_hashes", "All hashes at once", [])

    @app.on_message(filters.command("bcrypt_verify", prefixes=".") & filters.me)
    async def _bcrypt_verify_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.bcrypt_verify <hash> <password>`")
        await message.reply("Use `.shell pip install bcrypt` first, then run via `.eval`")
    register_command("Dev", "bcrypt_verify", "Verify bcrypt (needs bcrypt)", [])

    @app.on_message(filters.command("uuid_v5", prefixes=".") & filters.me)
    async def _uuid_v5_cmd(client, message):
        if len(message.command) < 3:
            return await message.reply("Usage: `.uuid_v5 <namespace> <name>`")
        ns_map = {"dns": uuid.NAMESPACE_DNS, "url": uuid.NAMESPACE_URL, "oid": uuid.NAMESPACE_OID}
        ns = ns_map.get(message.command[1].lower(), uuid.NAMESPACE_DNS)
        name = " ".join(message.command[2:])
        await message.reply(str(uuid.uuid5(ns, name)))
    register_command("Dev", "uuid_v5", "UUID v5 generator", [])

    @app.on_message(filters.command("nanoid", prefixes=".") & filters.me)
    async def _nanoid_cmd(client, message):
        size = int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else 21
        alphabet = string.ascii_letters + string.digits + "_-"
        await message.reply("".join(secrets.choice(alphabet) for _ in range(size)))
    register_command("Dev", "nanoid", "NanoID generator", [])

    @app.on_message(filters.command("snowflake", prefixes=".") & filters.me)
    async def _snowflake_cmd(client, message):
        ts = int(time.time() * 1000) - 1577836800000  # epoch since 2020
        rand = random.randint(0, 4095)
        worker = random.randint(0, 31)
        sid = (ts << 22) | (worker << 17) | rand
        await message.reply(str(sid))
    register_command("Dev", "snowflake", "Discord-style snowflake ID", [])

    # ─────────── ENCODING (10) ───────────

    @app.on_message(filters.command("b64url_e", prefixes=".") & filters.me)
    async def _b64url_e_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(base64.urlsafe_b64encode(text.encode()).decode())
    register_command("Dev", "b64url_e", "Base64 URL-safe encode", [])

    @app.on_message(filters.command("b64url_d", prefixes=".") & filters.me)
    async def _b64url_d_cmd(client, message):
        if len(message.command) < 2:
            return await message.reply("Provide base64")
        try:
            s = message.command[1] + "=" * (4 - len(message.command[1]) % 4)
            await message.reply(base64.urlsafe_b64decode(s).decode("utf-8", errors="ignore"))
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "b64url_d", "Base64 URL-safe decode", [])

    @app.on_message(filters.command("b85_e", prefixes=".") & filters.me)
    async def _b85_e_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(base64.b85encode(text.encode()).decode())
    register_command("Dev", "b85_e", "Base85 encode", [])

    @app.on_message(filters.command("b85_d", prefixes=".") & filters.me)
    async def _b85_d_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Provide base85")
        try:
            await message.reply(base64.b85decode(message.command[1].encode()).decode("utf-8", errors="ignore"))
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "b85_d", "Base85 decode", [])

    @app.on_message(filters.command("a85_e", prefixes=".") & filters.me)
    async def _a85_e_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(base64.a85encode(text.encode()).decode())
    register_command("Dev", "a85_e", "ASCII85 encode", [])

    @app.on_message(filters.command("a85_d", prefixes=".") & filters.me)
    async def _a85_d_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Provide ascii85")
        try:
            await message.reply(base64.a85decode(message.command[1].encode()).decode("utf-8", errors="ignore"))
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "a85_d", "ASCII85 decode", [])

    @app.on_message(filters.command("b32hex_e", prefixes=".") & filters.me)
    async def _b32hex_e_cmd(client, message):
        text = message.reply_to_message.text if message.reply_to_message else " ".join(message.command[1:])
        if not text: return await message.reply("Provide text")
        await message.reply(base64.b32hexencode(text.encode()).decode())
    register_command("Dev", "b32hex_e", "Base32 hex encode", [])

    @app.on_message(filters.command("b32hex_d", prefixes=".") & filters.me)
    async def _b32hex_d_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Provide base32hex")
        try:
            await message.reply(base64.b32hexdecode(message.command[1].upper().encode()).decode("utf-8", errors="ignore"))
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "b32hex_d", "Base32 hex decode", [])

    @app.on_message(filters.command("randombytes", prefixes=".") & filters.me)
    async def _randombytes_cmd(client, message):
        n = int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else 32
        n = min(n, 1024)
        await message.reply(secrets.token_hex(n))
    register_command("Dev", "randombytes", "Random hex bytes", [])

    @app.on_message(filters.command("random_token", prefixes=".") & filters.me)
    async def _random_token_cmd(client, message):
        n = int(message.command[1]) if len(message.command) > 1 and message.command[1].isdigit() else 32
        n = min(n, 256)
        await message.reply(secrets.token_urlsafe(n))
    register_command("Dev", "random_token", "Random URL-safe token", [])

    # ─────────── NETWORK (15) ───────────

    @app.on_message(filters.command("mx_lookup", prefixes=".") & filters.me)
    async def _mx_lookup_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.mx_lookup <domain>`")
        domain = message.command[1]
        try:
            import dns.resolver
            records = dns.resolver.resolve(domain, "MX")
            txt = "\n".join(f"{r.preference} {r.exchange}" for r in records)
            await message.reply(f"MX records for {domain}:\n{txt}")
        except ImportError:
            await message.reply("Install dnspython: `.pip install dnspython`")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "mx_lookup", "MX record lookup", [])

    @app.on_message(filters.command("txt_lookup", prefixes=".") & filters.me)
    async def _txt_lookup_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.txt_lookup <domain>`")
        domain = message.command[1]
        try:
            import dns.resolver
            records = dns.resolver.resolve(domain, "TXT")
            txt = "\n".join(str(r) for r in records)
            await message.reply(f"TXT records:\n{txt}")
        except ImportError:
            await message.reply("Install dnspython: `.pip install dnspython`")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "txt_lookup", "TXT record lookup", [])

    @app.on_message(filters.command("cname_lookup", prefixes=".") & filters.me)
    async def _cname_lookup_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.cname_lookup <domain>`")
        domain = message.command[1]
        try:
            import dns.resolver
            records = dns.resolver.resolve(domain, "CNAME")
            txt = "\n".join(str(r) for r in records)
            await message.reply(f"CNAME records:\n{txt}")
        except ImportError:
            await message.reply("Install dnspython: `.pip install dnspython`")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "cname_lookup", "CNAME record lookup", [])

    @app.on_message(filters.command("ptr_lookup", prefixes=".") & filters.me)
    async def _ptr_lookup_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.ptr_lookup <ip>`")
        ip = message.command[1]
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            await message.reply(f"PTR: {hostname}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "ptr_lookup", "Reverse DNS lookup", [])

    @app.on_message(filters.command("reverse_dns", prefixes=".") & filters.me)
    async def _reverse_dns_cmd(client, message):
        await _ptr_lookup_cmd(client, message)
    register_command("Dev", "reverse_dns", "Alias for ptr_lookup", [])

    @app.on_message(filters.command("tcp_ping", prefixes=".") & filters.me)
    async def _tcp_ping_cmd(client, message):
        if len(message.command) < 3: return await message.reply("Usage: `.tcp_ping <host> <port>`")
        host, port = message.command[1], int(message.command[2])
        try:
            start = time.time()
            s = socket.create_connection((host, port), timeout=5)
            elapsed = round((time.time() - start) * 1000, 2)
            s.close()
            await message.reply(f"TCP {host}:{port} - {elapsed}ms ✓")
        except Exception as e:
            await message.reply(f"TCP {host}:{port} - Failed: {e}")
    register_command("Dev", "tcp_ping", "TCP port ping", [])

    @app.on_message(filters.command("ssl_check", prefixes=".") & filters.me)
    async def _ssl_check_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.ssl_check <domain>`")
        domain = message.command[1]
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            expiry = cert["notAfter"]
            await message.reply(f"{domain}: SSL valid ✓\nExpires: {expiry}")
        except Exception as e:
            await message.reply(f"{domain}: SSL invalid ✗\n{e}")
    register_command("Dev", "ssl_check", "Check SSL validity", [])

    @app.on_message(filters.command("cert_expiry", prefixes=".") & filters.me)
    async def _cert_expiry_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.cert_expiry <domain>`")
        domain = message.command[1]
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            await message.reply(f"{domain} cert expires: {cert['notAfter']}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "cert_expiry", "Cert expiry date", [])

    @app.on_message(filters.command("resolve_ip", prefixes=".") & filters.me)
    async def _resolve_ip_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.resolve_ip <domain>`")
        domain = message.command[1]
        try:
            ips = socket.getaddrinfo(domain, None)
            unique = list(set(ip[4][0] for ip in ips))
            await message.reply(f"{domain}:\n" + "\n".join(unique))
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "resolve_ip", "Resolve domain to IP", [])

    @app.on_message(filters.command("ip_geo", prefixes=".") & filters.me)
    async def _ip_geo_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.ip_geo <ip>`")
        ip = message.command[1]
        try:
            req = urllib.request.Request(f"http://ip-api.com/json/{ip}", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            await message.reply(
                f"**IP: {ip}**\nCountry: {data.get('country', 'N/A')}\n"
                f"Region: {data.get('regionName', 'N/A')}\nCity: {data.get('city', 'N/A')}\n"
                f"ISP: {data.get('isp', 'N/A')}\nLat: {data.get('lat', 'N/A')}\nLon: {data.get('lon', 'N/A')}"
            )
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "ip_geo", "IP geolocation", [])

    @app.on_message(filters.command("my_ip", prefixes=".") & filters.me)
    async def _my_ip_cmd(client, message):
        try:
            req = urllib.request.Request("https://api.ipify.org", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                await message.reply(f"Public IP: {r.read().decode()}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "my_ip", "Get server public IP", [])

    @app.on_message(filters.command("my_useragent", prefixes=".") & filters.me)
    async def _my_useragent_cmd(client, message):
        await message.reply("User-Agent: KyrenUB/2.0 (Pyrogram)")
    register_command("Dev", "my_useragent", "Show bot UA", [])

    @app.on_message(filters.command("nslookup2", prefixes=".") & filters.me)
    async def _nslookup2_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.nslookup2 <domain>`")
        domain = message.command[1]
        try:
            ips = socket.getaddrinfo(domain, None)
            unique = list(set(ip[4][0] for ip in ips))
            await message.reply(f"{domain}:\n" + "\n".join(unique))
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "nslookup2", "DNS lookup", [])

    @app.on_message(filters.command("http_status_codes", prefixes=".") & filters.me)
    async def _http_status_codes_cmd(client, message):
        codes = {
            "1xx": "Informational",
            "2xx": "Success (200 OK, 201 Created, 204 No Content)",
            "3xx": "Redirection (301 Moved, 302 Found, 304 Not Modified)",
            "4xx": "Client Error (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests)",
            "5xx": "Server Error (500 Internal, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout)"
        }
        await message.reply("\n".join(f"**{k}**: {v}" for k, v in codes.items()))
    register_command("Dev", "http_status_codes", "HTTP status reference", [])

    @app.on_message(filters.command("port_list", prefixes=".") & filters.me)
    async def _port_list_cmd(client, message):
        common = {
            20: "FTP Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
            993: "IMAPS", 995: "POP3S", 1433: "MSSQL", 3306: "MySQL",
            3389: "RDP", 5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP Alt",
            27017: "MongoDB"
        }
        await message.reply("Common ports:\n" + "\n".join(f"{p}: {s}" for p, s in common.items()))
    register_command("Dev", "port_list", "Common ports reference", [])

    @app.on_message(filters.command("mac_lookup", prefixes=".") & filters.me)
    async def _mac_lookup_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.mac_lookup <mac>`")
        mac = message.command[1].upper()
        try:
            req = urllib.request.Request(f"https://api.macvendors.com/{mac}", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                vendor = r.read().decode()
            await message.reply(f"MAC {mac}: {vendor}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "mac_lookup", "MAC vendor lookup", [])

    # ─────────── REGEX TOOLS (10) ───────────

    @app.on_message(filters.command("regex_match", prefixes=".") & filters.me)
    async def _regex_match_cmd(client, message):
        if len(message.command) < 3: return await message.reply("Usage: `.regex_match <pattern> <text>`")
        pattern = message.command[1]
        text = " ".join(message.command[2:])
        try:
            match = re.fullmatch(pattern, text)
            await message.reply(f"Match: {bool(match)}\nGroups: {match.groups() if match else 'N/A'}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "regex_match", "Test regex fullmatch", [])

    @app.on_message(filters.command("regex_search", prefixes=".") & filters.me)
    async def _regex_search_cmd(client, message):
        if len(message.command) < 3: return await message.reply("Usage: `.regex_search <pattern> <text>`")
        pattern = message.command[1]
        text = " ".join(message.command[2:])
        try:
            match = re.search(pattern, text)
            if match:
                await message.reply(f"Found: `{match.group()}`\nSpan: {match.span()}")
            else:
                await message.reply("No match")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "regex_search", "Search regex", [])

    @app.on_message(filters.command("regex_findall", prefixes=".") & filters.me)
    async def _regex_findall_cmd(client, message):
        if len(message.command) < 3: return await message.reply("Usage: `.regex_findall <pattern> <text>`")
        pattern = message.command[1]
        text = " ".join(message.command[2:])
        try:
            matches = re.findall(pattern, text)
            await message.reply(f"Matches ({len(matches)}):\n" + "\n".join(f"• {m}" for m in matches[:30]))
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "regex_findall", "Find all regex matches", [])

    @app.on_message(filters.command("regex_sub", prefixes=".") & filters.me)
    async def _regex_sub_cmd(client, message):
        if len(message.command) < 4: return await message.reply("Usage: `.regex_sub <pattern> <repl> <text>`")
        pattern = message.command[1]
        repl = message.command[2]
        text = " ".join(message.command[3:])
        try:
            result = re.sub(pattern, repl, text)
            await message.reply(result)
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "regex_sub", "Regex substitute", [])

    @app.on_message(filters.command("regex_split", prefixes=".") & filters.me)
    async def _regex_split_cmd(client, message):
        if len(message.command) < 3: return await message.reply("Usage: `.regex_split <pattern> <text>`")
        pattern = message.command[1]
        text = " ".join(message.command[2:])
        try:
            parts = re.split(pattern, text)
            await message.reply(f"Parts ({len(parts)}):\n" + "\n".join(f"• {p}" for p in parts[:20]))
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "regex_split", "Regex split", [])

    @app.on_message(filters.command("regex_escape", prefixes=".") & filters.me)
    async def _regex_escape_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.regex_escape <text>`")
        text = " ".join(message.command[1:])
        await message.reply(re.escape(text))
    register_command("Dev", "regex_escape", "Escape regex special chars", [])

    @app.on_message(filters.command("regex_flags", prefixes=".") & filters.me)
    async def _regex_flags_cmd(client, message):
        flags = {
            "re.IGNORECASE": "Case insensitive",
            "re.MULTILINE": "^ and $ match line boundaries",
            "re.DOTALL": ". matches newline",
            "re.VERBOSE": "Allow comments in pattern",
            "re.UNICODE": "Unicode matching"
        }
        await message.reply("\n".join(f"**{k}**: {v}" for k, v in flags.items()))
    register_command("Dev", "regex_flags", "Regex flags reference", [])

    @app.on_message(filters.command("regex_validate", prefixes=".") & filters.me)
    async def _regex_validate_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.regex_validate <pattern>`")
        pattern = message.command[1]
        try:
            re.compile(pattern)
            await message.reply("Valid regex ✓")
        except re.error as e:
            await message.reply(f"Invalid regex ✗\n{e}")
    register_command("Dev", "regex_validate", "Validate regex pattern", [])

    @app.on_message(filters.command("email_regex", prefixes=".") & filters.me)
    async def _email_regex_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.email_regex <email>`")
        email = message.command[1]
        valid = bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))
        await message.reply(f"{email}: {'Valid ✓' if valid else 'Invalid ✗'}")
    register_command("Dev", "email_regex", "Validate email", [])

    @app.on_message(filters.command("url_regex", prefixes=".") & filters.me)
    async def _url_regex_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.url_regex <url>`")
        url = message.command[1]
        valid = bool(re.match(r"^https?://[^\s]+$", url))
        await message.reply(f"{url}: {'Valid ✓' if valid else 'Invalid ✗'}")
    register_command("Dev", "url_regex", "Validate URL", [])

    # ─────────── TIME UTILITIES (10) ───────────

    @app.on_message(filters.command("time_ago", prefixes=".") & filters.me)
    async def _time_ago_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.time_ago <unix_timestamp>`")
        try:
            ts = int(message.command[1])
            diff = time.time() - ts
            if diff < 0:
                diff = -diff
                suffix = "in the future"
            else:
                suffix = "ago"
            days = int(diff // 86400)
            hours = int((diff % 86400) // 3600)
            mins = int((diff % 3600) // 60)
            await message.reply(f"{days}d {hours}h {mins}m {suffix}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "time_ago", "Time ago from timestamp", [])

    @app.on_message(filters.command("time_until", prefixes=".") & filters.me)
    async def _time_until_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.time_until <unix_timestamp>`")
        try:
            ts = int(message.command[1])
            diff = ts - time.time()
            if diff < 0: return await message.reply("That time has passed")
            days = int(diff // 86400)
            hours = int((diff % 86400) // 3600)
            mins = int((diff % 3600) // 60)
            await message.reply(f"{days}d {hours}h {mins}m remaining")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "time_until", "Time until timestamp", [])

    @app.on_message(filters.command("time_diff", prefixes=".") & filters.me)
    async def _time_diff_cmd(client, message):
        if len(message.command) < 3: return await message.reply("Usage: `.time_diff <ts1> <ts2>`")
        try:
            diff = abs(int(message.command[1]) - int(message.command[2]))
            days = int(diff // 86400)
            hours = int((diff % 86400) // 3600)
            mins = int((diff % 3600) // 60)
            await message.reply(f"Difference: {days}d {hours}h {mins}m")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "time_diff", "Difference between timestamps", [])

    @app.on_message(filters.command("iso_now", prefixes=".") & filters.me)
    async def _iso_now_cmd(client, message):
        await message.reply(datetime.datetime.now(datetime.timezone.utc).isoformat())
    register_command("Dev", "iso_now", "Current ISO 8601 time", [])

    @app.on_message(filters.command("unix_now", prefixes=".") & filters.me)
    async def _unix_now_cmd(client, message):
        await message.reply(str(int(time.time())))
    register_command("Dev", "unix_now", "Current Unix timestamp", [])

    @app.on_message(filters.command("iso2unix", prefixes=".") & filters.me)
    async def _iso2unix_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.iso2unix <iso_time>`")
        try:
            dt = datetime.datetime.fromisoformat(message.command[1].replace("Z", "+00:00"))
            await message.reply(str(int(dt.timestamp())))
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "iso2unix", "ISO 8601 to Unix", [])

    @app.on_message(filters.command("unix2iso", prefixes=".") & filters.me)
    async def _unix2iso_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.unix2iso <timestamp>`")
        try:
            dt = datetime.datetime.fromtimestamp(int(message.command[1]), tz=datetime.timezone.utc)
            await message.reply(dt.isoformat())
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "unix2iso", "Unix to ISO 8601", [])

    @app.on_message(filters.command("epoch_ms", prefixes=".") & filters.me)
    async def _epoch_ms_cmd(client, message):
        await message.reply(str(int(time.time() * 1000)))
    register_command("Dev", "epoch_ms", "Current Unix ms", [])

    @app.on_message(filters.command("date_parse", prefixes=".") & filters.me)
    async def _date_parse_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.date_parse <YYYY-MM-DD>`")
        try:
            dt = datetime.datetime.strptime(message.command[1], "%Y-%m-%d")
            await message.reply(f"Parsed: {dt}\nUnix: {int(dt.timestamp())}\nDay: {dt.strftime('%A')}")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "date_parse", "Parse date string", [])

    @app.on_message(filters.command("timezone_list", prefixes=".") & filters.me)
    async def _timezone_list_cmd(client, message):
        common_tz = ["UTC", "America/New_York", "America/Los_Angeles", "Europe/London", "Europe/Paris",
                     "Asia/Tokyo", "Asia/Kolkata", "Asia/Dubai", "Australia/Sydney", "Pacific/Auckland"]
        await message.reply("Common timezones:\n" + "\n".join(f"• {tz}" for tz in common_tz))
    register_command("Dev", "timezone_list", "Common timezone list", [])

    # ─────────── MISC DEV TOOLS (15) ───────────

    @app.on_message(filters.command("str_escape", prefixes=".") & filters.me)
    async def _str_escape_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to text")
        text = message.reply_to_message.text
        escaped = text.encode("unicode_escape").decode()
        await message.reply(f"```\n{escaped[:3500]}\n```")
    register_command("Dev", "str_escape", "Escape string", [])

    @app.on_message(filters.command("str_unescape", prefixes=".") & filters.me)
    async def _str_unescape_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to escaped text")
        text = message.reply_to_message.text
        try:
            unescaped = text.encode().decode("unicode_escape")
            await message.reply(unescaped)
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "str_unescape", "Unescape string", [])

    @app.on_message(filters.command("json_path", prefixes=".") & filters.me)
    async def _json_path_cmd(client, message):
        if len(message.command) < 3: return await message.reply("Usage: `.json_path <path> <json>` (reply to json or provide)")
        path = message.command[1]
        try:
            if message.reply_to_message and message.reply_to_message.text:
                data = json.loads(message.reply_to_message.text)
            else:
                data = json.loads(" ".join(message.command[2:]))
            for key in path.split("."):
                if key.isdigit():
                    data = data[int(key)]
                else:
                    data = data[key]
            await message.reply(f"```\n{json.dumps(data, indent=2)[:3000]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "json_path", "JSON path evaluator", [])

    @app.on_message(filters.command("json_keys", prefixes=".") & filters.me)
    async def _json_keys_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to JSON object")
        try:
            data = json.loads(message.reply_to_message.text)
            if isinstance(data, dict):
                await message.reply("Keys:\n" + "\n".join(f"• {k}" for k in data.keys()))
            else:
                await message.reply("Not a JSON object")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "json_keys", "List JSON keys", [])

    @app.on_message(filters.command("json_validate", prefixes=".") & filters.me)
    async def _json_validate_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.text:
            return await message.reply("Reply to JSON")
        try:
            json.loads(message.reply_to_message.text)
            await message.reply("Valid JSON ✓")
        except json.JSONDecodeError as e:
            await message.reply(f"Invalid JSON ✗\n{e}")
    register_command("Dev", "json_validate", "Validate JSON", [])

    @app.on_message(filters.command("char_info", prefixes=".") & filters.me)
    async def _char_info_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.char_info <char>`")
        c = message.command[1][0] if message.command[1] else " "
        await message.reply(
            f"Char: `{c}`\nUnicode: U+{ord(c):04X}\nDecimal: {ord(c)}\n"
            f"Hex: 0x{ord(c):X}\nOctal: {ord(c):o}\nBinary: {ord(c):08b}\nName: {getattr(c, 'name', 'N/A')}"
        )
    register_command("Dev", "char_info", "Unicode char info", [])

    @app.on_message(filters.command("str_diff", prefixes=".") & filters.me)
    async def _str_diff_cmd(client, message):
        if len(message.command) < 3: return await message.reply("Usage: `.str_diff <str1> <str2>`")
        s1, s2 = message.command[1], message.command[2]
        import difflib
        diff = list(difflib.ndiff(s1, s2))
        await message.reply("Diff:\n" + "".join(diff))
    register_command("Dev", "str_diff", "String diff", [])

    @app.on_message(filters.command("pip_search", prefixes=".") & filters.me)
    async def _pip_search_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.pip_search <package>`")
        pkg = message.command[1]
        try:
            req = urllib.request.Request(f"https://pypi.org/pypi/{pkg}/json", headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            info = data["info"]
            await message.reply(
                f"**{info['name']}** v{info['version']}\n{info['summary']}\n"
                f"Author: {info['author']}\nHome: {info.get('home_page', 'N/A')}\n"
                f"License: {info.get('license', 'N/A')}"
            )
        except Exception as e:
            await message.reply(f"Not found: {e}")
    register_command("Dev", "pip_search", "Search PyPI package", [])

    @app.on_message(filters.command("git_log", prefixes=".") & filters.me)
    async def _git_log_cmd(client, message):
        try:
            n = message.command[1] if len(message.command) > 1 else "10"
            result = subprocess.run(["git", "log", f"-{n}", "--oneline"], capture_output=True, text=True, timeout=10)
            await message.reply(f"```\n{result.stdout[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "git_log", "Recent git commits", [])

    @app.on_message(filters.command("git_branch", prefixes=".") & filters.me)
    async def _git_branch_cmd(client, message):
        try:
            result = subprocess.run(["git", "branch"], capture_output=True, text=True, timeout=10)
            await message.reply(f"```\n{result.stdout}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "git_branch", "List git branches", [])

    @app.on_message(filters.command("git_status2", prefixes=".") & filters.me)
    async def _git_status2_cmd(client, message):
        try:
            result = subprocess.run(["git", "status"], capture_output=True, text=True, timeout=10)
            await message.reply(f"```\n{result.stdout[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "git_status2", "Git status", [])

    @app.on_message(filters.command("git_diff", prefixes=".") & filters.me)
    async def _git_diff_cmd(client, message):
        try:
            result = subprocess.run(["git", "diff"], capture_output=True, text=True, timeout=10)
            await message.reply(f"```diff\n{result.stdout[:3500]}\n```")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "git_diff", "Git diff", [])

    @app.on_message(filters.command("uptime_cmd", prefixes=".") & filters.me)
    async def _uptime_cmd(client, message):
        try:
            with open("/proc/uptime") as f:
                secs = float(f.read().split()[0])
            days = int(secs // 86400)
            hours = int((secs % 86400) // 3600)
            mins = int((secs % 3600) // 60)
            await message.reply(f"Server uptime: {days}d {hours}h {mins}m")
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "uptime_cmd", "Server uptime", [])

    @app.on_message(filters.command("env_vars", prefixes=".") & filters.me)
    async def _env_vars_cmd(client, message):
        safe = {k: "***" if any(s in k.upper() for s in ["KEY", "SECRET", "TOKEN", "PASSWORD", "HASH", "SESSION"]) else v
                for k, v in os.environ.items()}
        await message.reply("```\n" + "\n".join(f"{k}={v}" for k, v in safe.items())[:3500] + "\n```")
    register_command("Dev", "env_vars", "List env vars (sanitized)", [])

    @app.on_message(filters.command("file_hash", prefixes=".") & filters.me)
    async def _file_hash_cmd(client, message):
        if not message.reply_to_message or not message.reply_to_message.document:
            return await message.reply("Reply to a file")
        try:
            path = await message.reply_to_message.download()
            h = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            await message.reply(f"SHA256: {h.hexdigest()}")
            os.remove(path)
        except Exception as e:
            await message.reply(f"Error: {e}")
    register_command("Dev", "file_hash", "SHA256 of file", [])

    @app.on_message(filters.command("mimetype", prefixes=".") & filters.me)
    async def _mimetype_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.mimetype <extension>`")
        ext = message.command[1].lstrip(".").lower()
        import mimetypes
        mt = mimetypes.guess_type(f"file.{ext}")[0] or "Unknown"
        await message.reply(f".{ext}: {mt}")
    register_command("Dev", "mimetype", "Get MIME type for extension", [])

    @app.on_message(filters.command("uptime_check", prefixes=".") & filters.me)
    async def _uptime_check_cmd(client, message):
        if len(message.command) < 2: return await message.reply("Usage: `.uptime_check <url>`")
        url = message.command[1]
        try:
            start = time.time()
            req = urllib.request.Request(url, headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                elapsed = round((time.time() - start) * 1000, 2)
                await message.reply(f"✅ {url} is UP\nStatus: {r.status}\nResponse: {elapsed}ms")
        except urllib.error.HTTPError as e:
            await message.reply(f"⚠️ {url} returned {e.code}")
        except Exception as e:
            await message.reply(f"❌ {url} is DOWN\n{e}")
    register_command("Dev", "uptime_check", "Check if URL is up", [])

    print("[Dev] Developer tools plugin registered")
