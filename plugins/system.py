"""
KyrenUB - System Plugin
========================
56 commands for system control, info, management, networking, and utilities.
Uses psutil, subprocess, speedtest. Module-level _sleeping=False flag.
"""

_sleeping = False


def register(app):
    from pyrogram import filters
    from pyrogram.errors import FloodWait
    from plugins import register_command
    import asyncio
    import os
    import sys
    import time
    import subprocess
    import platform
    import socket
    import struct
    import datetime
    import json
    import re
    import shutil
    import signal
    import textwrap
    import calendar
    import threading
    import traceback
    import random
    import tempfile

    _TMP = tempfile.gettempdir()

    def _cleanup(path):
        try:
            os.remove(path)
        except OSError:
            pass

    # ═══════════════════════════════════════════════════════════════
    #  CONTROL (12 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command(["shell", "sh"], prefixes=".") & filters.me)
    async def shell_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.sh <command>`")
            return
        cmd = args[1]
        msg = await message.edit(f"⏳ Running: `{cmd}`")
        try:
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            output = proc.stdout or proc.stderr or "No output."
            if len(output) > 4096:
                output = output[:4090] + "\n..."
            await msg.edit(f"💻 **Shell:** `{cmd}`\n\n```\n{output}\n```")
        except subprocess.TimeoutExpired:
            await msg.edit("❌ Command timed out (30s).")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "shell", "Run shell command", ["sh"])

    @app.on_message(filters.command(["eval", "ev"], prefixes=".") & filters.me)
    async def eval_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.ev <python expression>`")
            return
        code = args[1]
        try:
            result = eval(code, {"__builtins__": {}}, {"client": client, "message": message})
            await message.edit(f"🧮 **Eval:**\n`{code}`\n\n**Result:**\n`{result}`")
        except Exception as e:
            await message.edit(f"❌ **Eval Error:** `{type(e).__name__}: {e}`")

    register_command("System", "eval", "Evaluate Python expression", ["ev"])

    @app.on_message(filters.command(["exec", "ex"], prefixes=".") & filters.me)
    async def exec_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.ex <python code>`")
            return
        code = args[1]
        try:
            exec(code, {"__builtins__": {}}, {"client": client, "message": message})
            await message.edit(f"✅ **Exec done.**")
        except Exception as e:
            await message.edit(f"❌ **Exec Error:** `{type(e).__name__}: {e}`")

    register_command("System", "exec", "Execute Python code", ["ex"])

    @app.on_message(filters.command("restart", prefixes=".") & filters.me)
    async def restart_cmd(client, message):
        await message.edit("🔄 **Restarting...**")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    register_command("System", "restart", "Restart the bot", [])

    @app.on_message(filters.command(["shutdown", "off"], prefixes=".") & filters.me)
    async def shutdown_cmd(client, message):
        await message.edit("🔴 **Shutting down...**")
        os._exit(0)

    register_command("System", "shutdown", "Shut down the bot", ["off"])

    @app.on_message(filters.command("update", prefixes=".") & filters.me)
    async def update_cmd(client, message):
        msg = await message.edit("⏳ Updating...")
        try:
            proc = subprocess.run(["git", "pull"], capture_output=True, text=True, timeout=30)
            output = proc.stdout or proc.stderr
            if "Already up to date" in output or "Already up-to-date" in output:
                await msg.edit("✅ **Already up to date.**")
            else:
                await msg.edit(f"✅ **Updated:**\n```\n{output[:2000]}\n```")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "update", "Git pull update", [])

    @app.on_message(filters.command("logs", prefixes=".") & filters.me)
    async def logs_cmd(client, message):
        log_path = "kyrenub.log"
        if not os.path.exists(log_path):
            await message.edit("❌ No log file found.")
            return
        try:
            with open(log_path, "r") as f:
                content = f.read()[-4000:]
            await message.edit(f"📋 **Logs:**\n```\n{content}\n```")
        except Exception as e:
            await message.edit(f"❌ Error: `{e}`")

    register_command("System", "logs", "Show recent logs", [])

    @app.on_message(filters.command("clearlogs", prefixes=".") & filters.me)
    async def clearlogs_cmd(client, message):
        log_path = "kyrenub.log"
        try:
            if os.path.exists(log_path):
                with open(log_path, "w") as f:
                    f.write("")
                await message.edit("🧹 **Logs cleared.**")
            else:
                await message.edit("❌ No log file found.")
        except Exception as e:
            await message.edit(f"❌ Error: `{e}`")

    register_command("System", "clearlogs", "Clear log file", [])

    @app.on_message(filters.command("pip", prefixes=".") & filters.me)
    async def pip_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.pip <install|uninstall|list> <package>`")
            return
        action = args[1].lower()
        pkg = args[2]
        if action not in ("install", "uninstall", "list", "show"):
            await message.edit("❌ Action must be install/uninstall/list/show.")
            return
        msg = await message.edit(f"⏳ pip {action} {pkg}...")
        try:
            cmd = [sys.executable, "-m", "pip", action, pkg, "-q"]
            if action == "uninstall":
                cmd.append("-y")
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            output = (proc.stdout or proc.stderr or "Done.")[:2000]
            await msg.edit(f"📦 **pip {action} {pkg}:**\n```\n{output}\n```")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "pip", "pip install/uninstall/list/show", [])

    @app.on_message(filters.command("git", prefixes=".") & filters.me)
    async def git_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.git <git command>`")
            return
        cmd = args[1]
        msg = await message.edit(f"⏳ git {cmd}...")
        try:
            proc = subprocess.run(["git"] + cmd.split(), capture_output=True, text=True, timeout=30)
            output = (proc.stdout or proc.stderr or "Done.")[:2000]
            await msg.edit(f"🔧 **git {cmd}:**\n```\n{output}\n```")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "git", "Run git command", [])

    @app.on_message(filters.command("env", prefixes=".") & filters.me)
    async def env_cmd(client, message):
        env_vars = dict(os.environ)
        # Filter sensitive vars
        safe = {k: v[:20] + "..." if k in ("API_HASH", "STRING_SESSION", "TOKEN") else v
                for k, v in env_vars.items()}
        text = f"🌍 **Environment Variables** ({len(safe)}):\n\n"
        for k, v in sorted(safe.items()):
            text += f"  • `{k}`: `{v[:50]}`\n"
        if len(text) > 4096:
            text = text[:4090] + "\n..."
        await message.edit(text)

    register_command("System", "env", "Show environment variables", [])

    @app.on_message(filters.command("ps", prefixes=".") & filters.me)
    async def ps_cmd(client, message):
        msg = await message.edit("⏳ Getting process list...")
        try:
            import psutil as _ps
            procs = []
            for p in _ps.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = p.info
                    procs.append(f"  • PID `{info['pid']}`: {info['name']} "
                                f"(CPU: `{info['cpu_percent']:.1f}%`, MEM: `{info['memory_percent']:.1f}%`)")
                except (_ps.NoSuchProcess, _ps.AccessDenied):
                    pass
            text = f"📊 **Processes** (top 20):\n\n" + "\n".join(procs[:20])
            await msg.edit(text)
        except ImportError:
            try:
                proc = subprocess.run(["ps", "aux"], capture_output=True, text=True, timeout=10)
                lines = proc.stdout.splitlines()[:21]
                await msg.edit(f"📊 **Processes:**\n```\n" + "\n".join(lines) + "\n```")
            except Exception as e:
                await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "ps", "List running processes", [])

    # ═══════════════════════════════════════════════════════════════
    #  INFO (15 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command(["sysinfo", "system"], prefixes=".") & filters.me)
    async def sysinfo_cmd(client, message):
        msg = await message.edit("⏳ Gathering system info...")
        try:
            import psutil as _ps
            boot = datetime.datetime.fromtimestamp(_ps.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
            cpu_pct = _ps.cpu_percent(interval=1)
            mem = _ps.virtual_memory()
            disk = _ps.disk_usage("/")
            text = (
                f"🖥 **System Info**\n\n"
                f"💻 **Platform:** `{platform.system()} {platform.release()}`\n"
                f"🏗 **Architecture:** `{platform.machine()}`\n"
                f"📛 **Hostname:** `{socket.gethostname()}`\n"
                f"🐍 **Python:** `{sys.version.split()[0]}`\n"
                f"🧠 **CPU:** `{cpu_pct}%` usage\n"
                f"💾 **RAM:** `{_ps._common.bytes2human(mem.used)}` / `{_ps._common.bytes2human(mem.total)}` (`{mem.percent}%`)\n"
                f"💿 **Disk:** `{_ps._common.bytes2human(disk.used)}` / `{_ps._common.bytes2human(disk.total)}` (`{disk.percent}%`)\n"
                f"⏱ **Boot:** `{boot}`\n"
                f"🔧 **CPUs:** `{_ps.cpu_count()}`"
            )
            await msg.edit(text)
        except ImportError:
            text = (
                f"🖥 **System Info**\n\n"
                f"💻 **Platform:** `{platform.system()} {platform.release()}`\n"
                f"🏗 **Architecture:** `{platform.machine()}`\n"
                f"📛 **Hostname:** `{socket.gethostname()}`\n"
                f"🐍 **Python:** `{sys.version.split()[0]}`\n"
                f"🔧 **CPUs:** `{os.cpu_count()}`"
            )
            await msg.edit(text)

    register_command("System", "sysinfo", "Full system information", ["system"])

    @app.on_message(filters.command("cpu", prefixes=".") & filters.me)
    async def cpu_cmd(client, message):
        try:
            import psutil as _ps
            cpu_pct = _ps.cpu_percent(interval=1, percpu=True)
            freq = _ps.cpu_freq()
            text = f"🧠 **CPU Info**\n\n"
            text += f"🔧 **Cores:** `{_ps.cpu_count(logical=False)}` physical, `{_ps.cpu_count()}` logical\n"
            if freq:
                text += f"⚡ **Freq:** `{freq.current:.0f} MHz` (max: `{freq.max:.0f} MHz`)\n"
            text += f"📊 **Usage per core:**\n"
            for i, pct in enumerate(cpu_pct):
                bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
                text += f"  Core {i}: `{bar}` `{pct:.1f}%`\n"
            await message.edit(text)
        except ImportError:
            await message.edit(f"🧠 **CPU:** `{os.cpu_count()}` cores (install psutil for details)")

    register_command("System", "cpu", "CPU info and usage", [])

    @app.on_message(filters.command(["memory", "mem"], prefixes=".") & filters.me)
    async def memory_cmd(client, message):
        try:
            import psutil as _ps
            mem = _ps.virtual_memory()
            swap = _ps.swap_memory()
            text = (
                f"💾 **Memory Info**\n\n"
                f"📊 **RAM:**\n"
                f"  Total: `{_ps._common.bytes2human(mem.total)}`\n"
                f"  Used: `{_ps._common.bytes2human(mem.used)}`\n"
                f"  Free: `{_ps._common.bytes2human(mem.available)}`\n"
                f"  Usage: `{mem.percent}%`\n\n"
                f"📊 **Swap:**\n"
                f"  Total: `{_ps._common.bytes2human(swap.total)}`\n"
                f"  Used: `{_ps._common.bytes2human(swap.used)}`\n"
                f"  Free: `{_ps._common.bytes2human(swap.free)}`\n"
                f"  Usage: `{swap.percent}%`"
            )
            await message.edit(text)
        except ImportError:
            await message.edit("❌ Install psutil for memory info.")

    register_command("System", "memory", "Memory usage info", ["mem"])

    @app.on_message(filters.command("disk", prefixes=".") & filters.me)
    async def disk_cmd(client, message):
        try:
            import psutil as _ps
            text = "💿 **Disk Info**\n\n"
            for part in _ps.disk_partitions():
                try:
                    usage = _ps.disk_usage(part.mountpoint)
                    text += f"📂 **{part.mountpoint}** (`{part.fstype}`)\n"
                    text += f"  Total: `{_ps._common.bytes2human(usage.total)}`\n"
                    text += f"  Used: `{_ps._common.bytes2human(usage.used)}`\n"
                    text += f"  Free: `{_ps._common.bytes2human(usage.free)}`\n"
                    text += f"  Usage: `{usage.percent}%`\n\n"
                except PermissionError:
                    text += f"📂 **{part.mountpoint}** — Permission denied\n\n"
            await message.edit(text)
        except ImportError:
            await message.edit("❌ Install psutil for disk info.")

    register_command("System", "disk", "Disk usage info", [])

    @app.on_message(filters.command(["network", "net"], prefixes=".") & filters.me)
    async def network_cmd(client, message):
        try:
            import psutil as _ps
            text = "🌐 **Network Info**\n\n"
            addrs = _ps.net_if_addrs()
            for iface, addr_list in addrs.items():
                text += f"📡 **{iface}:**\n"
                for addr in addr_list:
                    if addr.family == socket.AF_INET:
                        text += f"  IPv4: `{addr.address}`\n"
                    elif addr.family == socket.AF_INET6:
                        text += f"  IPv6: `{addr.address[:30]}...`\n"
                text += "\n"
            io = _ps.net_io_counters()
            text += f"📊 **Total IO:**\n"
            text += f"  Sent: `{_ps._common.bytes2human(io.bytes_sent)}`\n"
            text += f"  Recv: `{_ps._common.bytes2human(io.bytes_recv)}`\n"
            await message.edit(text)
        except ImportError:
            await message.edit("❌ Install psutil for network info.")

    register_command("System", "network", "Network interfaces info", ["net"])

    @app.on_message(filters.command("uptime", prefixes=".") & filters.me)
    async def uptime_cmd(client, message):
        try:
            import psutil as _ps
            boot = datetime.datetime.fromtimestamp(_ps.boot_time())
            now = datetime.datetime.now()
            delta = now - boot
            d = delta.days
            h, rem = divmod(delta.seconds, 3600)
            m, s = divmod(rem, 60)
            await message.edit(f"⏱ **Uptime:** `{d}d {h}h {m}m {s}s`")
        except ImportError:
            await message.edit("❌ Install psutil for uptime.")

    register_command("System", "uptime", "System uptime", [])

    @app.on_message(filters.command(["python", "py"], prefixes=".") & filters.me)
    async def python_cmd(client, message):
        text = (
            f"🐍 **Python Info**\n\n"
            f"📌 **Version:** `{sys.version}`\n"
            f"📂 **Executable:** `{sys.executable}`\n"
            f"📁 **Path:** `{sys.path[:3]}`\n"
            f"📦 **Prefix:** `{sys.prefix}`\n"
            f"🏗 **Platform:** `{platform.python_implementation()}`\n"
            f"🔗 **Compiler:** `{platform.python_compiler()}`\n"
            f"🏗 **Build:** `{platform.python_build()}`"
        )
        await message.edit(text)

    register_command("System", "python", "Python version and build info", ["py"])

    @app.on_message(filters.command(["platform", "plat"], prefixes=".") & filters.me)
    async def platform_cmd(client, message):
        text = (
            f"💻 **Platform Info**\n\n"
            f"🖥 **System:** `{platform.system()}`\n"
            f"📦 **Release:** `{platform.release()}`\n"
            f"📌 **Version:** `{platform.version()}`\n"
            f"🏗 **Machine:** `{platform.machine()}`\n"
            f"🔧 **Processor:** `{platform.processor()}`\n"
            f"📛 **Node:** `{platform.node()}`\n"
            f"🎯 **Platform:** `{platform.platform()}`"
        )
        await message.edit(text)

    register_command("System", "platform", "Platform details", ["plat"])

    @app.on_message(filters.command("kernel", prefixes=".") & filters.me)
    async def kernel_cmd(client, message):
        text = (
            f"🔧 **Kernel Info**\n\n"
            f"📌 **System:** `{platform.system()}`\n"
            f"📦 **Release:** `{platform.release()}`\n"
            f"📌 **Version:** `{platform.version()}`\n"
            f"🏗 **Arch:** `{platform.machine()}`"
        )
        await message.edit(text)

    register_command("System", "kernel", "Kernel/OS version info", [])

    @app.on_message(filters.command("hostname", prefixes=".") & filters.me)
    async def hostname_cmd(client, message):
        await message.edit(f"📛 **Hostname:** `{socket.gethostname()}`")

    register_command("System", "hostname", "System hostname", [])

    @app.on_message(filters.command("arch", prefixes=".") & filters.me)
    async def arch_cmd(client, message):
        text = (
            f"🏗 **Architecture Info**\n\n"
            f"📌 **Machine:** `{platform.machine()}`\n"
            f"🔧 **Processor:** `{platform.processor()}`\n"
            f"💻 **Bits:** `{struct.calcsize('P') * 8}-bit`\n"
            f"🖥 **System:** `{platform.system()}`"
        )
        await message.edit(text)

    register_command("System", "arch", "Architecture info", [])

    @app.on_message(filters.command("users", prefixes=".") & filters.me)
    async def users_cmd(client, message):
        try:
            import psutil as _ps
            users = _ps.users()
            if not users:
                await message.edit("❌ No users found.")
                return
            text = f"👥 **Users** ({len(users)}):\n\n"
            for u in users:
                text += f"  • `{u.name}` — terminal: `{u.terminal or 'N/A'}`\n"
                if u.host:
                    text += f"    Host: `{u.host}`\n"
                text += f"    Started: `{datetime.datetime.fromtimestamp(u.started).strftime('%Y-%m-%d %H:%M')}`\n"
            await message.edit(text)
        except ImportError:
            await message.edit("❌ Install psutil for users info.")

    register_command("System", "users", "List logged-in users", [])

    @app.on_message(filters.command("load", prefixes=".") & filters.me)
    async def load_cmd(client, message):
        try:
            import psutil as _ps
            load1, load5, load15 = _ps.getloadavg()
            text = (
                f"📊 **System Load**\n\n"
                f"1 min: `{load1:.2f}`\n"
                f"5 min: `{load5:.2f}`\n"
                f"15 min: `{load15:.2f}`\n"
                f"CPU count: `{_ps.cpu_count()}`"
            )
            await message.edit(text)
        except (ImportError, AttributeError):
            await message.edit("❌ Install psutil for load info.")

    register_command("System", "load", "System load averages", [])

    @app.on_message(filters.command("temp", prefixes=".") & filters.me)
    async def temp_cmd(client, message):
        try:
            import psutil as _ps
            temps = _ps.sensors_temperatures()
            if not temps:
                await message.edit("❌ No temperature sensors available.")
                return
            text = "🌡 **Temperatures**\n\n"
            for name, entries in temps.items():
                for entry in entries:
                    text += f"  • {entry.label or name}: `{entry.current:.1f}°C`"
                    if entry.high:
                        text += f" (high: `{entry.high:.1f}°C`)"
                    text += "\n"
            await message.edit(text)
        except ImportError:
            await message.edit("❌ Install psutil for temperature info.")

    register_command("System", "temp", "System temperatures", [])

    @app.on_message(filters.command("battery", prefixes=".") & filters.me)
    async def battery_cmd(client, message):
        try:
            import psutil as _ps
            bat = _ps.sensors_battery()
            if not bat:
                await message.edit("❌ No battery detected (desktop/server).")
                return
            plugged = "🔌 Charging" if bat.power_plugged else "🔋 Discharging"
            text = (
                f"🔋 **Battery**\n\n"
                f"📊 **Percent:** `{bat.percent}%`\n"
                f"📌 **Status:** {plugged}\n"
            )
            if bat.secs_left != _ps.POWER_TIME_UNLIMITED:
                h, rem = divmod(bat.secs_left, 3600)
                m, s = divmod(rem, 60)
                text += f"⏱ **Time left:** `{h}h {m}m`"
            await message.edit(text)
        except ImportError:
            await message.edit("❌ Install psutil for battery info.")

    register_command("System", "battery", "Battery status", [])

    # ═══════════════════════════════════════════════════════════════
    #  MANAGE (11 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("sleep", prefixes=".") & filters.me)
    async def sleep_cmd(client, message):
        global _sleeping
        if _sleeping:
            await message.edit("❌ Already sleeping.")
            return
        args = message.text.split(None, 1)
        try:
            seconds = int(args[1]) if len(args) > 1 else 300
        except ValueError:
            seconds = 300
        _sleeping = True
        await message.edit(f"😴 **Sleeping for {seconds}s...** Use `.awake` to wake up.")
        await asyncio.sleep(seconds)
        _sleeping = False
        try:
            await message.edit("☀️ **Awake!**")
        except Exception:
            pass

    register_command("System", "sleep", "Sleep bot for N seconds", [])

    @app.on_message(filters.command("awake", prefixes=".") & filters.me)
    async def awake_cmd(client, message):
        global _sleeping
        _sleeping = False
        await message.edit("☀️ **Bot is awake!**")

    register_command("System", "awake", "Wake up the bot", [])

    @app.on_message(filters.command("backup", prefixes=".") & filters.me)
    async def backup_cmd(client, message):
        msg = await message.edit("⏳ Creating backup...")
        try:
            backup_name = f"kyrenub_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
            proc = subprocess.run(
                ["tar", "-czf", backup_name, "--exclude=__pycache__",
                 "--exclude=.git", "--exclude=*.session", "."],
                capture_output=True, text=True, timeout=60
            )
            if os.path.exists(backup_name):
                await client.send_document(message.chat.id, backup_name)
                await msg.edit("✅ **Backup created!**")
                _cleanup(backup_name)
            else:
                await msg.edit("❌ Backup creation failed.")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "backup", "Create backup archive", [])

    _scheduled = {}

    @app.on_message(filters.command("schedule", prefixes=".") & filters.me)
    async def schedule_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.schedule <seconds> <command>`")
            return
        try:
            delay = int(args[1])
            cmd = args[2]
        except ValueError:
            await message.edit("❌ Seconds must be a number.")
            return
        task_id = f"task_{random.randint(1000,9999)}" if 'random' in dir() else f"task_{int(time.time())}"
        _scheduled[task_id] = {"cmd": cmd, "delay": delay, "active": True}
        await message.edit(f"⏰ **Scheduled:** `{cmd}` in `{delay}s` (ID: `{task_id}`)")

        async def _run_scheduled():
            await asyncio.sleep(delay)
            if task_id in _scheduled and _scheduled[task_id]["active"]:
                fake_text = f".{cmd}"
                # Send the command as if user typed it
                try:
                    await client.send_message(message.chat.id, fake_text)
                except Exception:
                    pass
                _scheduled.pop(task_id, None)

        asyncio.ensure_future(_run_scheduled())

    register_command("System", "schedule", "Schedule a command", [])

    @app.on_message(filters.command("cancel", prefixes=".") & filters.me)
    async def cancel_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) > 1:
            task_id = args[1]
            if task_id in _scheduled:
                _scheduled[task_id]["active"] = False
                _scheduled.pop(task_id)
                await message.edit(f"✅ **Cancelled:** `{task_id}`")
            else:
                await message.edit(f"❌ Task `{task_id}` not found.")
        else:
            if _scheduled:
                for tid in list(_scheduled.keys()):
                    _scheduled[tid]["active"] = False
                _scheduled.clear()
                await message.edit("✅ **All scheduled tasks cancelled.**")
            else:
                await message.edit("❌ No scheduled tasks.")

    register_command("System", "cancel", "Cancel scheduled task(s)", [])

    @app.on_message(filters.command("export", prefixes=".") & filters.me)
    async def export_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.export <variable>`")
            return
        var_name = args[1].strip()
        val = os.environ.get(var_name)
        if val is not None:
            await message.edit(f"📤 **{var_name}:** `{val[:200]}`")
        else:
            await message.edit(f"❌ Variable `{var_name}` not found.")

    register_command("System", "export", "Show environment variable value", [])

    @app.on_message(filters.command("import", prefixes=".") & filters.me)
    async def import_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.import <module>`")
            return
        mod = args[1].strip()
        msg = await message.edit(f"⏳ Importing `{mod}`...")
        try:
            __import__(mod)
            await msg.edit(f"✅ **Imported:** `{mod}`")
        except ImportError as e:
            await msg.edit(f"❌ **Import Error:** `{e}`")

    register_command("System", "import", "Import a Python module", [])

    @app.on_message(filters.command("reset", prefixes=".") & filters.me)
    async def reset_cmd(client, message):
        await message.edit("🔄 **Resetting...**")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    register_command("System", "reset", "Reset the bot (restart)", [])

    @app.on_message(filters.command("debug", prefixes=".") & filters.me)
    async def debug_cmd(client, message):
        try:
            import psutil as _ps
            proc = _ps.Process(os.getpid())
            text = (
                f"🐛 **Debug Info**\n\n"
                f"🆔 **PID:** `{os.getpid()}`\n"
                f"🧵 **Threads:** `{proc.num_threads()}`\n"
                f"💾 **Memory:** `{_ps._common.bytes2human(proc.memory_info().rss)}`\n"
                f"📂 **CWD:** `{os.getcwd()}`\n"
                f"🐍 **Python:** `{sys.version.split()[0]}`\n"
                f"⏱ **CPU Time:** `{sum(proc.cpu_times()[:2]):.2f}s`\n"
                f"🔗 **Connections:** `{len(proc.connections())}`\n"
                f"📂 **Open Files:** `{len(proc.open_files())}`"
            )
        except ImportError:
            text = (
                f"🐛 **Debug Info**\n\n"
                f"🆔 **PID:** `{os.getpid()}`\n"
                f"📂 **CWD:** `{os.getcwd()}`\n"
                f"🐍 **Python:** `{sys.version.split()[0]}`"
            )
        await message.edit(text)

    register_command("System", "debug", "Bot process debug info", [])

    @app.on_message(filters.command("verbose", prefixes=".") & filters.me)
    async def verbose_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) > 1 and args[1].lower() in ("on", "true", "1"):
            os.environ["KYRENUB_VERBOSE"] = "1"
            await message.edit("📢 **Verbose mode: ON**")
        elif len(args) > 1 and args[1].lower() in ("off", "false", "0"):
            os.environ["KYRENUB_VERBOSE"] = "0"
            await message.edit("🔇 **Verbose mode: OFF**")
        else:
            current = os.environ.get("KYRENUB_VERBOSE", "0")
            await message.edit(f"📢 **Verbose mode:** `{'ON' if current == '1' else 'OFF'}`")

    register_command("System", "verbose", "Toggle verbose mode", [])

    @app.on_message(filters.command("quota", prefixes=".") & filters.me)
    async def quota_cmd(client, message):
        try:
            import psutil as _ps
            disk = _ps.disk_usage("/")
            mem = _ps.virtual_memory()
            text = (
                f"📊 **Resource Quota**\n\n"
                f"💾 **RAM:** `{_ps._common.bytes2human(mem.used)}` / `{_ps._common.bytes2human(mem.total)}` (`{mem.percent}%`)\n"
                f"💿 **Disk:** `{_ps._common.bytes2human(disk.used)}` / `{_ps._common.bytes2human(disk.total)}` (`{disk.percent}%`)\n"
                f"🧠 **CPU:** `{_ps.cpu_percent()}%`\n"
                f"📂 **CWD:** `{os.getcwd()}`"
            )
            await message.edit(text)
        except ImportError:
            await message.edit("❌ Install psutil for quota info.")

    register_command("System", "quota", "Resource usage quota", [])

    # ═══════════════════════════════════════════════════════════════
    #  NET (8 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command(["speedtest", "speed"], prefixes=".") & filters.me)
    async def speedtest_cmd(client, message):
        msg = await message.edit("⏳ Running speed test (this may take a minute)...")
        try:
            import speedtest as _st
            st = _st.Speedtest()
            st.get_best_server()
            download = st.download() / 1024 / 1024
            upload = st.upload() / 1024 / 1024
            ping = st.results.ping
            text = (
                f"🚀 **Speed Test Results**\n\n"
                f"📥 **Download:** `{download:.2f} Mbps`\n"
                f"📤 **Upload:** `{upload:.2f} Mbps`\n"
                f"📡 **Ping:** `{ping:.2f} ms`\n"
                f"🌐 **Server:** `{st.results.server['sponsor']}` ({st.results.server['name']})"
            )
            await msg.edit(text)
        except ImportError:
            await msg.edit("❌ Install speedtest-cli: `pip install speedtest-cli`")
        except Exception as e:
            await msg.edit(f"❌ Speedtest error: `{e}`")

    register_command("System", "speedtest", "Internet speed test", ["speed"])

    @app.on_message(filters.command("ping2", prefixes=".") & filters.me)
    async def ping2_cmd(client, message):
        args = message.text.split(None, 1)
        host = args[1] if len(args) > 1 else "google.com"
        msg = await message.edit(f"⏳ Pinging `{host}`...")
        try:
            proc = subprocess.run(
                ["ping", "-c", "4", host],
                capture_output=True, text=True, timeout=15
            )
            output = proc.stdout or proc.stderr
            lines = output.strip().splitlines()
            result = "\n".join(lines[-3:])
            await msg.edit(f"📡 **Ping `{host}`:**\n```\n{result}\n```")
        except subprocess.TimeoutExpired:
            await msg.edit(f"❌ Ping to `{host}` timed out.")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "ping2", "Ping a host (ICMP)", [])

    @app.on_message(filters.command("trace", prefixes=".") & filters.me)
    async def trace_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.trace <host>`")
            return
        host = args[1]
        msg = await message.edit(f"⏳ Tracing route to `{host}`...")
        try:
            proc = subprocess.run(
                ["traceroute", host],
                capture_output=True, text=True, timeout=60
            )
            output = (proc.stdout or proc.stderr)[:3000]
            await msg.edit(f"🗺 **Traceroute `{host}`:**\n```\n{output}\n```")
        except FileNotFoundError:
            await msg.edit("❌ traceroute not installed.")
        except subprocess.TimeoutExpired:
            await msg.edit("❌ Traceroute timed out.")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "trace", "Traceroute to host", [])

    @app.on_message(filters.command("nslookup", prefixes=".") & filters.me)
    async def nslookup_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.nslookup <domain>`")
            return
        domain = args[1]
        msg = await message.edit(f"⏳ Looking up `{domain}`...")
        try:
            proc = subprocess.run(
                ["nslookup", domain],
                capture_output=True, text=True, timeout=15
            )
            output = (proc.stdout or proc.stderr)[:2000]
            await msg.edit(f"🔍 **NSLookup `{domain}`:**\n```\n{output}\n```")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "nslookup", "DNS lookup", [])

    @app.on_message(filters.command("ifconfig", prefixes=".") & filters.me)
    async def ifconfig_cmd(client, message):
        msg = await message.edit("⏳ Getting network config...")
        try:
            proc = subprocess.run(
                ["ifconfig"] if os.name != "nt" else ["ipconfig", "/all"],
                capture_output=True, text=True, timeout=10
            )
            output = (proc.stdout or "")[:3000]
            await msg.edit(f"🌐 **Network Config:**\n```\n{output}\n```")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "ifconfig", "Network interface config", [])

    @app.on_message(filters.command("curl", prefixes=".") & filters.me)
    async def curl_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.curl <url>`")
            return
        url = args[1]
        msg = await message.edit(f"⏳ Fetching `{url}`...")
        try:
            import urllib.request
            req = urllib.request.Request(url, headers={"User-Agent": "KyrenUB/2.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read(4096).decode(errors="replace")
            await msg.edit(f"🌐 **curl `{url}`:**\n```\n{data[:3000]}\n```")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "curl", "Fetch URL content", [])

    @app.on_message(filters.command("wget", prefixes=".") & filters.me)
    async def wget_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.wget <url>`")
            return
        url = args[1]
        msg = await message.edit(f"⏳ Downloading `{url}`...")
        try:
            import urllib.request
            filename = url.split("/")[-1] or "downloaded_file"
            filepath = os.path.join(_TMP, f"kyrenub_{filename}")
            urllib.request.urlretrieve(url, filepath)
            if os.path.getsize(filepath) < 50 * 1024 * 1024:
                await client.send_document(message.chat.id, filepath)
                await msg.delete()
            else:
                await msg.edit("✅ **Downloaded** (too large to upload).")
            _cleanup(filepath)
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "wget", "Download file from URL", [])

    @app.on_message(filters.command("portcheck", prefixes=".") & filters.me)
    async def portcheck_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.portcheck <host> <port>`")
            return
        host = args[1]
        try:
            port = int(args[2])
        except ValueError:
            await message.edit("❌ Port must be a number.")
            return
        msg = await message.edit(f"⏳ Checking `{host}:{port}`...")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            status = "🟢 **OPEN**" if result == 0 else "🔴 **CLOSED**"
            await msg.edit(f"🔌 **Port Check:** `{host}:{port}` — {status}")
        except Exception as e:
            await msg.edit(f"❌ Error: `{e}`")

    register_command("System", "portcheck", "Check if port is open", [])

    # ═══════════════════════════════════════════════════════════════
    #  UTIL (10 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("whoami", prefixes=".") & filters.me)
    async def whoami_cmd(client, message):
        me = await client.get_me()
        text = f"👤 **Who Am I**\n\n"
        text += f"📛 **Name:** {me.first_name}"
        if me.last_name:
            text += f" {me.last_name}"
        text += "\n"
        if me.username:
            text += f"🌐 **Username:** @{me.username}\n"
        text += f"🆔 **ID:** `{me.id}`\n"
        text += f"📱 **Phone:** `{me.phone_number or 'Hidden'}`\n"
        if me.dc_id:
            text += f"📡 **DC:** `{me.dc_id}`\n"
        text += f"🤖 **Bot:** `{me.is_bot}`\n"
        text += f"💻 **OS User:** `{os.getenv('USER', os.getenv('USERNAME', 'unknown'))}`"
        await message.edit(text)

    register_command("System", "whoami", "Show your identity info", [])

    @app.on_message(filters.command("date", prefixes=".") & filters.me)
    async def date_cmd(client, message):
        now = datetime.datetime.now()
        text = (
            f"📅 **Date & Time**\n\n"
            f"📆 **Date:** `{now.strftime('%Y-%m-%d')}`\n"
            f"⏰ **Time:** `{now.strftime('%H:%M:%S')}`\n"
            f"📆 **Day:** `{now.strftime('%A')}`\n"
            f"📝 **Full:** `{now.strftime('%B %d, %Y %I:%M:%S %p')}`\n"
            f"🕐 **UTC:** `{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}`\n"
            f"⏱ **Timestamp:** `{int(now.timestamp())}`"
        )
        await message.edit(text)

    register_command("System", "date", "Show current date and time", [])

    @app.on_message(filters.command(["calendar", "cal"], prefixes=".") & filters.me)
    async def calendar_cmd(client, message):
        args = message.text.split(None, 2)
        now = datetime.datetime.now()
        try:
            year = int(args[1]) if len(args) > 1 else now.year
            month = int(args[2]) if len(args) > 2 else now.month
        except ValueError:
            await message.edit("❌ Invalid year/month.")
            return
        cal = calendar.month(year, month)
        await message.edit(f"📅 **{calendar.month_name[month]} {year}:**\n```\n{cal}\n```")

    register_command("System", "calendar", "Show calendar month", ["cal"])

    @app.on_message(filters.command(["timezone", "tz"], prefixes=".") & filters.me)
    async def timezone_cmd(client, message):
        args = message.text.split(None, 1)
        now = datetime.datetime.now()
        utc_now = datetime.datetime.utcnow()
        offset = now - utc_now
        total_seconds = int(offset.total_seconds())
        h, m = divmod(abs(total_seconds) // 60, 60)
        sign = "+" if total_seconds >= 0 else "-"
        tz_name = time.tzname[0] if time.tzname[0] else "Local"
        text = (
            f"🕐 **Timezone Info**\n\n"
            f"📌 **TZ:** `{tz_name}`\n"
            f"⏱ **Offset:** `UTC{sign}{h:02d}:{m:02d}`\n"
            f"🕐 **Local:** `{now.strftime('%Y-%m-%d %H:%M:%S')}`\n"
            f"🌐 **UTC:** `{utc_now.strftime('%Y-%m-%d %H:%M:%S')}`"
        )
        if len(args) > 1:
            try:
                import zoneinfo
                tz = zoneinfo.ZoneInfo(args[1])
                tz_time = datetime.datetime.now(tz=tz)
                text += f"\n📍 **{args[1]}:** `{tz_time.strftime('%Y-%m-%d %H:%M:%S')}`"
            except Exception:
                text += f"\n❌ Unknown timezone: `{args[1]}`"
        await message.edit(text)

    register_command("System", "timezone", "Show timezone info", ["tz"])

    _timers = {}

    @app.on_message(filters.command("countdown_timer", prefixes=".") & filters.me)
    async def countdown_timer_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.countdown_timer <seconds>`")
            return
        try:
            seconds = int(args[1])
        except ValueError:
            await message.edit("❌ Seconds must be a number.")
            return
        msg = await message.edit(f"⏳ **Countdown: {seconds}s**")
        timer_id = f"timer_{int(time.time())}"
        _timers[timer_id] = True
        for i in range(seconds, 0, -1):
            if timer_id not in _timers:
                break
            try:
                await msg.edit(f"⏳ **Countdown: {i}s**")
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
            await asyncio.sleep(1)
        if timer_id in _timers:
            _timers.pop(timer_id)
            try:
                await msg.edit("⏰ **Time's up!**")
            except Exception:
                pass

    register_command("System", "countdown_timer", "Start a countdown timer", [])

    @app.on_message(filters.command("stopwatch2", prefixes=".") & filters.me)
    async def stopwatch2_cmd(client, message):
        msg = await message.edit("⏱ **Stopwatch: 0.0s** — Use `.stopwatch2 stop` to stop")
        start = time.time()
        timer_id = f"sw_{int(start)}"
        _timers[timer_id] = True
        while timer_id in _timers:
            elapsed = time.time() - start
            try:
                await msg.edit(f"⏱ **Stopwatch: {elapsed:.1f}s**")
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
            except Exception:
                break
            await asyncio.sleep(1)
        elapsed = time.time() - start
        try:
            await msg.edit(f"⏱ **Stopwatch stopped: {elapsed:.1f}s**")
        except Exception:
            pass

    register_command("System", "stopwatch2", "Start a stopwatch", [])

    @app.on_message(filters.command("alarm", prefixes=".") & filters.me)
    async def alarm_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.alarm <HH:MM> <message>`")
            return
        time_str = args[1]
        alarm_msg = args[2]
        try:
            h, m = map(int, time_str.split(":"))
        except ValueError:
            await message.edit("❌ Time format: HH:MM")
            return
        now = datetime.datetime.now()
        alarm_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if alarm_time <= now:
            alarm_time += datetime.timedelta(days=1)
        delay = (alarm_time - now).total_seconds()
        await message.edit(f"⏰ **Alarm set for `{time_str}`** — `{alarm_msg}` (in {int(delay)}s)")

        async def _alarm():
            await asyncio.sleep(delay)
            try:
                await client.send_message(message.chat.id, f"⏰ **ALARM!**\n📌 {alarm_msg}")
            except Exception:
                pass

        asyncio.ensure_future(_alarm())

    register_command("System", "alarm", "Set an alarm", [])

    @app.on_message(filters.command("reminder", prefixes=".") & filters.me)
    async def reminder_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.reminder <seconds> <message>`")
            return
        try:
            seconds = int(args[1])
        except ValueError:
            await message.edit("❌ Seconds must be a number.")
            return
        reminder_text = args[2]
        await message.edit(f"📝 **Reminder set:** `{reminder_text}` in `{seconds}s`")

        async def _remind():
            await asyncio.sleep(seconds)
            try:
                await client.send_message(message.chat.id, f"📝 **Reminder:**\n📌 {reminder_text}")
            except Exception:
                pass

        asyncio.ensure_future(_remind())

    register_command("System", "reminder", "Set a reminder", [])

    _todos = {}

    @app.on_message(filters.command("todo", prefixes=".") & filters.me)
    async def todo_cmd(client, message):
        chat_id = message.chat.id
        args = message.text.split(None, 1)
        if chat_id not in _todos:
            _todos[chat_id] = []
        if len(args) < 2:
            if not _todos[chat_id]:
                await message.edit("📋 **Todo list is empty.** Use `.todo <item>` to add.")
            else:
                text = "📋 **Todo List:**\n\n"
                for i, item in enumerate(_todos[chat_id], 1):
                    text += f"  {i}. {item}\n"
                text += "\n💡 `.todo <item>` to add | `.todo del <num>` to remove"
                await message.edit(text)
            return
        action = args[1]
        if action.lower().startswith("del") or action.lower().startswith("rm"):
            parts = action.split(None, 1)
            try:
                idx = int(parts[1]) - 1
                if 0 <= idx < len(_todos[chat_id]):
                    removed = _todos[chat_id].pop(idx)
                    await message.edit(f"✅ **Removed:** `{removed}`")
                else:
                    await message.edit("❌ Invalid item number.")
            except (ValueError, IndexError):
                await message.edit("❌ **Usage:** `.todo del <number>`")
        elif action.lower() == "clear":
            _todos[chat_id].clear()
            await message.edit("🧹 **Todo list cleared.**")
        else:
            _todos[chat_id].append(action)
            await message.edit(f"✅ **Added:** `{action}`")

    register_command("System", "todo", "Todo list manager", [])

    _notes = {}

    @app.on_message(filters.command("note", prefixes=".") & filters.me)
    async def note_cmd(client, message):
        chat_id = message.chat.id
        args = message.text.split(None, 2)
        if chat_id not in _notes:
            _notes[chat_id] = {}
        if len(args) < 2:
            if not _notes[chat_id]:
                await message.edit("📝 **No notes.** Use `.note save <name> <text>` to add.")
            else:
                text = "📝 **Notes:**\n\n"
                for name in sorted(_notes[chat_id].keys()):
                    content = _notes[chat_id][name][:50]
                    text += f"  📌 **{name}:** {content}\n"
                text += "\n💡 `.note get <name>` | `.note del <name>`"
                await message.edit(text)
            return
        action = args[1].lower()
        if action == "save":
            if len(args) < 3:
                await message.edit("❌ **Usage:** `.note save <name> <text>`")
                return
            parts = args[2].split(None, 1)
            if len(parts) < 2:
                await message.edit("❌ **Usage:** `.note save <name> <text>`")
                return
            name, text = parts[0], parts[1]
            _notes[chat_id][name] = text
            await message.edit(f"✅ **Note saved:** `{name}`")
        elif action == "get":
            if len(args) < 3:
                await message.edit("❌ **Usage:** `.note get <name>`")
                return
            name = args[2]
            if name in _notes[chat_id]:
                await message.edit(f"📝 **Note: {name}**\n\n{_notes[chat_id][name]}")
            else:
                await message.edit(f"❌ Note `{name}` not found.")
        elif action in ("del", "rm", "delete"):
            if len(args) < 3:
                await message.edit("❌ **Usage:** `.note del <name>`")
                return
            name = args[2]
            if name in _notes[chat_id]:
                del _notes[chat_id][name]
                await message.edit(f"✅ **Note deleted:** `{name}`")
            else:
                await message.edit(f"❌ Note `{name}` not found.")
        elif action == "clear":
            _notes[chat_id].clear()
            await message.edit("🧹 **All notes cleared.**")
        else:
            await message.edit("❌ **Usage:** `.note <save|get|del|clear>`")

    register_command("System", "note", "Note manager (save/get/del)", [])
