"""
KyrenUB - Monkey Patches for Python 3.12+ Compatibility
========================================================
MUST be imported before any other third-party library.
Recreates removed/deprecated stdlib modules that Pyrogram relies on.
"""

import sys
import types
import warnings
import asyncio


# ── Patch `cgi` – removed in Python 3.13 (PEP 594) ──────────
if sys.version_info >= (3, 12):
    try:
        import cgi  # noqa: F401
    except ImportError:
        from email.message import Message as _EmailMessage

        class _CgiModule(types.ModuleType):
            def parse_header(self, string):
                if not string:
                    return "", {}
                msg = _EmailMessage()
                msg["content-type"] = string
                params = msg.get_params(failobj={})
                if isinstance(params, list):
                    main = params[0][0] if params[0] else ""
                    param_dict = {}
                    for pair in params[1:]:
                        if len(pair) >= 2:
                            param_dict[pair[0].lower()] = pair[1]
                    return main, param_dict
                return string, {}

        _cgi = _CgiModule("cgi")
        _cgi.__path__ = []
        _cgi.__package__ = "cgi"
        sys.modules["cgi"] = _cgi


# ── Patch `audioop` – removed in Python 3.13 (PEP 594) ──────
if sys.version_info >= (3, 12):
    try:
        import audioop  # noqa: F401
    except ImportError:

        class _AudioopModule(types.ModuleType):
            error = Exception
            def add(self, f1, f2, w): return f1
            def bias(self, f, w, b): return f
            def byteswap(self, f, w): return f
            def cross(self, f, w): return 0
            def findfactor(self, f, r): return 1.0
            def findfit(self, f, r): return (0, 0.0)
            def findmax(self, f, w): return 0
            def getsample(self, f, w, i): return 0
            def lin2lin(self, f, w, nw): return b"\x00" * (len(f) // w * nw)
            def lin2alaw(self, f, w): return b"\x00" * (len(f) // w)
            def lin2ulaw(self, f, w): return b"\x00" * (len(f) // w)
            def alaw2lin(self, f, w): return b"\x00" * len(f) * w
            def ulaw2lin(self, f, w): return b"\x00" * len(f) * w
            def minmax(self, f, w): return (0, 0)
            def max(self, f, w): return 0
            def min(self, f, w): return 0
            def maxpp(self, f, w): return 0
            def mul(self, f, w, factor): return f
            def ratecv(self, f, w, ch, ir, or_, s, wA=1, wB=0): return (f, (0, 0.0))
            def reverse(self, f, w): return f
            def rms(self, f, w): return 0
            def tomono(self, f, w, lf, rf): return f[: len(f) // 2]
            def tostereo(self, f, w, lf, rf): return f * 2

        _audioop = _AudioopModule("audioop")
        _audioop.__path__ = []
        _audioop.__package__ = "audioop"
        sys.modules["audioop"] = _audioop


# ── Patch `imghdr` – removed in Python 3.13 (PEP 594) ───────
if sys.version_info >= (3, 12):
    try:
        import imghdr  # noqa: F401
    except ImportError:

        class _ImghdrModule(types.ModuleType):
            def what(self, file, h=None):
                if h is None:
                    if hasattr(file, "read"):
                        h = file.read(32)
                    else:
                        with open(file, "rb") as fh:
                            h = fh.read(32)
                if h[:8] == b"\x89PNG\r\n\x1a\n": return "png"
                if h[:2] == b"\xff\xd8": return "jpeg"
                if h[:4] == b"GIF8": return "gif"
                if h[:4] == b"RIFF" and h[8:12] == b"WEBP": return "webp"
                if h[:2] == b"BM": return "bmp"
                return None
            tests = []

        _imghdr = _ImghdrModule("imghdr")
        _imghdr.__path__ = []
        _imghdr.__package__ = "imghdr"
        sys.modules["imghdr"] = _imghdr


# ── Patch asyncio.get_event_loop deprecation ─────────────────
_original_get_event_loop = asyncio.get_event_loop

def _safe_get_event_loop():
    try:
        loop = _original_get_event_loop()
        if loop.is_closed():
            raise RuntimeError("Event loop is closed")
        return loop
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

asyncio.get_event_loop = _safe_get_event_loop

# ── Suppress warnings ────────────────────────────────────────
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pyrogram")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="asyncio")
warnings.filterwarnings("ignore", message=".*get_event_loop.*")
warnings.filterwarnings("ignore", message=".*cgi.*")
warnings.filterwarnings("ignore", message=".*audioop.*")
warnings.filterwarnings("ignore", message=".*imghdr.*")
