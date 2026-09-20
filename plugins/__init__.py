"""
KyrenUB - Plugin System
========================
Dynamic plugin loader that auto-discovers and registers commands.

Includes duplicate-command protection: Pyrogram fires *every* handler that
matches a message, so if two plugins own the same command the user gets two
replies. The loader wraps ``app.on_message`` and keeps the first registered
owner of each command (plugins load in alphabetical order), skipping later
duplicates while logging them.
"""

import os
import importlib
import traceback
import functools
from typing import Dict, List, Any

CMD_LIST: Dict[str, List[Dict[str, Any]]] = {}


def register_command(category: str, name: str, help_text: str, aliases: List[str] = None):
    """Add a command to the global registry."""
    if category not in CMD_LIST:
        CMD_LIST[category] = []
    CMD_LIST[category].append({
        "name": name,
        "aliases": aliases or [],
        "help": help_text,
    })


def _extract_commands(flt):
    """Best-effort extraction of command names from a Pyrogram filter.

    Handles bare ``filters.command(...)`` and logical filters such as
    ``filters.command(...) & filters.me`` (whose ``base`` is the
    CommandFilter). Returns a set of command names or ``None``.
    """
    if flt is None:
        return None
    try:
        cmds = getattr(flt, "commands", None)
    except Exception:
        cmds = None
    if cmds:
        return set(cmds)
    for attr in ("base", "other"):
        try:
            sub = getattr(flt, attr, None)
        except Exception:
            sub = None
        if sub is not None:
            found = _extract_commands(sub)
            if found:
                return found
    return None


def _safe_command(func):
    """Wrap a command handler so missing/invalid arguments don't crash it.

    ``message.command[N]`` with too few args raises IndexError and
    ``int(message.command[N])`` raises ValueError; both are turned into a
    friendly usage reply instead of an unhandled exception.
    """

    @functools.wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except (IndexError, ValueError):
            try:
                cmd = message.command[0] if getattr(message, "command", None) else "command"
            except Exception:
                cmd = "command"
            try:
                await message.reply(
                    f"⚠️ `.{cmd}` ke liye arguments missing/invalid hain.\n"
                    f"Sahi usage ke liye `.help` dekho."
                )
            except Exception:
                pass

    return wrapper


class _DedupApp:
    """Proxy around a Pyrogram client that de-duplicates command handlers.

    Non-command handlers and all other attributes are forwarded to the real
    client unchanged.
    """

    def __init__(self, app):
        self._app = app
        self._claimed = set()
        self.skipped = []

    def __getattr__(self, name):
        return getattr(self._app, name)

    def on_message(self, filters=None, group=0, **kwargs):
        names = _extract_commands(filters)
        if names:
            clash = names & self._claimed
            if clash:
                self.skipped.append(sorted(clash))

                def _skip(func):
                    return func

                return _skip
            self._claimed |= names
            real_deco = self._app.on_message(filters, group, **kwargs)

            def _deco(func):
                return real_deco(_safe_command(func))

            return _deco
        return self._app.on_message(filters, group, **kwargs)


def load_plugins(app):
    """Scan the plugins/ directory and register all commands."""
    plugins_dir = os.path.dirname(os.path.abspath(__file__))
    loaded = 0
    failed = 0

    plugin_files = sorted(
        f for f in os.listdir(plugins_dir)
        if f.endswith(".py") and f != "__init__.py" and not f.startswith("_")
    )

    proxy = _DedupApp(app)

    for filename in plugin_files:
        module_name = f"plugins.{filename[:-3]}"
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "register"):
                module.register(proxy)
                loaded += 1
                print(f"[Plugins] Loaded: {module_name}")
            else:
                print(f"[Plugins] Skipped (no register()): {module_name}")
        except Exception as e:
            failed += 1
            print(f"[Plugins] Failed: {module_name} - {e}")
            traceback.print_exc()

    print(f"[Plugins] Loaded {loaded} plugin(s), {failed} failed.")

    if proxy.skipped:
        print(f"[Plugins] Skipped {len(proxy.skipped)} duplicate command handler(s) (first wins):")
        for clash in proxy.skipped:
            print(f"  {', '.join('.' + c for c in clash)}")

    # ── Duplicate command detection (registry view) ─────────────
    _seen = {}
    _dups = {}
    for _cat, _cmds in CMD_LIST.items():
        for _c in _cmds:
            _n = _c["name"]
            if _n in _seen:
                _dups.setdefault(_n, [_seen[_n]]).append(_cat)
            else:
                _seen[_n] = _cat
    if _dups:
        print(f"[Plugins] WARNING: {len(_dups)} duplicate command name(s) across categories:")
        for _n, _cats in sorted(_dups.items()):
            print(f"  .{_n} -> {', '.join(_cats)}")

    total = sum(len(v) for v in CMD_LIST.values())
    print(f"[Plugins] Total commands registered: {total}")
    for cat, cmds in sorted(CMD_LIST.items()):
        print(f"  {cat}: {len(cmds)} commands")

    return _dups