"""
KyrenUB - Docker Management Plugin
==================================
Manage Docker containers straight from Telegram. Requires docker CLI on the VPS.
"""

def register(app):
    from pyrogram import filters
    from plugins import register_command
    import subprocess, json, asyncio

    def _docker(*args, timeout=30):
        return subprocess.run(["docker"] + list(args),
                              capture_output=True, text=True, timeout=timeout)

    def _has_docker():
        try:
            subprocess.run(["docker", "--version"], capture_output=True, timeout=5)
            return True
        except Exception:
            return False

    # ─────────── DOCKER ROOT COMMAND ───────────

    @app.on_message(filters.command("docker", prefixes=".") & filters.me)
    async def _docker_cmd(client, message):
        """
        .docker ps                          -> list running containers
        .docker ps -a                       -> list all (incl stopped)
        .docker images                      -> list images
        .docker logs <container>            -> last 30 lines
        .docker logs <container> <n>        -> last n lines
        .docker restart <container>
        .docker stop <container>
        .docker start <container>
        .docker rm <container>
        .docker rmi <image>
        .docker exec <container> <cmd...>
        .docker stats                       -> resource usage
        .docker top <container>             -> processes inside container
        .docker inspect <container>         -> JSON metadata
        .docker compose <up|down|ps> [path] -> docker compose
        """
        if not _has_docker():
            return await message.reply("❌ Docker not installed on this VPS.")
        if len(message.command) < 2:
            return await message.reply(
                "🐳 **Docker commands:**\n"
                "`.docker ps` - running containers\n"
                "`.docker ps -a` - all containers\n"
                "`.docker images` - list images\n"
                "`.docker logs <c> [n]` - last n log lines\n"
                "`.docker restart <c>`\n"
                "`.docker stop <c>`\n"
                "`.docker start <c>`\n"
                "`.docker rm <c>`\n"
                "`.docker rmi <img>`\n"
                "`.docker exec <c> <cmd...>`\n"
                "`.docker stats`\n"
                "`.docker top <c>`\n"
                "`.docker inspect <c>`\n"
                "`.docker compose up|down|ps [path]`"
            )
        sub = message.command[1]
        args = message.command[2:]

        try:
            if sub == "ps":
                out = _docker("ps", *args)
                text = out.stdout or out.stderr
                await message.reply(f"```\n{text[:3500]}\n```")
            elif sub == "images":
                out = _docker("images")
                text = out.stdout or out.stderr
                await message.reply(f"```\n{text[:3500]}\n```")
            elif sub == "logs":
                if not args:
                    return await message.reply("Usage: `.docker logs <container> [n]`")
                container = args[0]
                n = args[1] if len(args) > 1 and args[1].isdigit() else "30"
                out = _docker("logs", "--tail", n, container)
                text = (out.stdout or out.stderr)[:3500]
                await message.reply(f"📋 Logs `{container}` (last {n}):\n```\n{text}\n```")
            elif sub in ("restart", "stop", "start", "rm", "pause", "unpause"):
                if not args:
                    return await message.reply(f"Usage: `.docker {sub} <container>`")
                out = _docker(sub, args[0])
                if out.returncode == 0:
                    await message.reply(f"✅ `{sub} {args[0]}` OK")
                else:
                    await message.reply(f"❌ {out.stderr.strip()[:500]}")
            elif sub == "rmi":
                if not args:
                    return await message.reply("Usage: `.docker rmi <image>`")
                out = _docker("rmi", args[0])
                text = (out.stdout or out.stderr)[:1500]
                await message.reply(f"```\n{text}\n```")
            elif sub == "exec":
                if len(args) < 2:
                    return await message.reply("Usage: `.docker exec <container> <cmd...>`")
                container = args[0]
                cmd_args = args[1:]
                out = _docker("exec", container, *cmd_args, timeout=60)
                text = (out.stdout + out.stderr)[:3500]
                await message.reply(f"```\n{text}\n```")
            elif sub == "stats":
                out = _docker("stats", "--no-stream")
                await message.reply(f"```\n{(out.stdout or out.stderr)[:3500]}\n```")
            elif sub == "top":
                if not args:
                    return await message.reply("Usage: `.docker top <container>`")
                out = _docker("top", args[0])
                await message.reply(f"```\n{(out.stdout or out.stderr)[:3500]}\n```")
            elif sub == "inspect":
                if not args:
                    return await message.reply("Usage: `.docker inspect <container>`")
                out = _docker("inspect", args[0])
                try:
                    data = json.loads(out.stdout)
                    text = json.dumps(data[0], indent=2)[:3500]
                except Exception:
                    text = out.stdout[:3500]
                await message.reply(f"```json\n{text}\n```")
            elif sub == "compose":
                if not args:
                    return await message.reply("Usage: `.docker compose up|down|ps [path]`")
                action = args[0]
                path = args[1] if len(args) > 1 else "."
                if action == "up":
                    out = subprocess.run(["docker", "compose", "-f", path, "up", "-d"],
                                         capture_output=True, text=True, timeout=120)
                elif action == "down":
                    out = subprocess.run(["docker", "compose", "-f", path, "down"],
                                         capture_output=True, text=True, timeout=120)
                else:
                    out = subprocess.run(["docker", "compose", "-f", path, action],
                                         capture_output=True, text=True, timeout=60)
                text = (out.stdout or out.stderr)[:3500]
                await message.reply(f"```\n{text}\n```")
            else:
                await message.reply(f"Unknown subcommand: `{sub}`. Try `.docker` for help.")
        except subprocess.TimeoutExpired:
            await message.reply("❌ Docker command timed out.")
        except Exception as e:
            await message.reply(f"❌ {e}")
    register_command("Docker", "docker", "Manage Docker containers (ps/logs/restart/stop/start/exec/stats)", [])

    @app.on_message(filters.command("dps", prefixes=".") & filters.me)
    async def _dps_cmd(client, message):
        """Shortcut for .docker ps"""
        if not _has_docker():
            return await message.reply("❌ Docker not installed.")
        out = _docker("ps")
        await message.reply(f"```\n{(out.stdout or out.stderr)[:3500]}\n```")
    register_command("Docker", "dps", "Shortcut for .docker ps", [])

    @app.on_message(filters.command("dlogs", prefixes=".") & filters.me)
    async def _dlogs_cmd(client, message):
        """Shortcut for .docker logs <c> [n]"""
        if not _has_docker():
            return await message.reply("❌ Docker not installed.")
        if len(message.command) < 2:
            return await message.reply("Usage: `.dlogs <container> [n]`")
        container = message.command[1]
        n = message.command[2] if len(message.command) > 2 and message.command[2].isdigit() else "50"
        out = _docker("logs", "--tail", n, container)
        text = (out.stdout or out.stderr)[:3500]
        await message.reply(f"📋 Logs `{container}` (last {n}):\n```\n{text}\n```")
    register_command("Docker", "dlogs", "Shortcut for .docker logs", [])

    print("[Docker] Registered Docker management commands")
