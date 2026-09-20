"""
KyrenUB - Text Plugin
======================
134 commands for text transformation, Unicode fonts, decorations,
encryption, analysis, manipulation, and misc text fun.
"""


def register(app):
    from pyrogram import filters
    from pyrogram.errors import FloodWait
    from plugins import register_command
    import asyncio
    import random
    import re
    import base64
    import urllib.parse
    import html
    import textwrap
    import string
    import collections

    # ═══════════════════════════════════════════════════════════════
    #  SHARED HELPERS & MAPPINGS
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

    # ── Unicode font mappings (Math Alphanumeric Symbols) ──
    _FONT_BOLD = {
        'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠',
        'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧',
        'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮',
        'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
        'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆',
        'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
        'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
        'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
        '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒',
        '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗',
    }
    _FONT_ITALIC = {
        'a': '𝑎', 'b': '𝑏', 'c': '𝑐', 'd': '𝑑', 'e': '𝑒', 'f': '𝑓', 'g': '𝑔',
        'h': 'ℎ', 'i': '𝑖', 'j': '𝑗', 'k': '𝑘', 'l': '𝑙', 'm': '𝑚', 'n': '𝑛',
        'o': '𝑜', 'p': '𝑝', 'q': '𝑞', 'r': '𝑟', 's': '𝑠', 't': '𝑡', 'u': '𝑢',
        'v': '𝑣', 'w': '𝑤', 'x': '𝑥', 'y': '𝑦', 'z': '𝑧',
        'A': '𝐴', 'B': '𝐵', 'C': '𝐶', 'D': '𝐷', 'E': '𝐸', 'F': '𝐹', 'G': '𝐺',
        'H': '𝐻', 'I': '𝐼', 'J': '𝐽', 'K': '𝐾', 'L': '𝐿', 'M': '𝑀', 'N': '𝑁',
        'O': '𝑂', 'P': '𝑃', 'Q': '𝑄', 'R': '𝑅', 'S': '𝑆', 'T': '𝑇', 'U': '𝑈',
        'V': '𝑉', 'W': '𝑊', 'X': '𝑋', 'Y': '𝑌', 'Z': '𝑍',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_BOLD_ITALIC = {
        'a': '𝒂', 'b': '𝒃', 'c': '𝒄', 'd': '𝒅', 'e': '𝒆', 'f': '𝒇', 'g': '𝒈',
        'h': '𝒉', 'i': '𝒊', 'j': '𝒋', 'k': '𝒌', 'l': '𝒍', 'm': '𝒎', 'n': '𝒏',
        'o': '𝒐', 'p': '𝒑', 'q': '𝒒', 'r': '𝒓', 's': '𝒔', 't': '𝒕', 'u': '𝒖',
        'v': '𝒗', 'w': '𝒘', 'x': '𝒙', 'y': '𝒚', 'z': '𝒛',
        'A': '𝑨', 'B': '𝑩', 'C': '𝑪', 'D': '𝑫', 'E': '𝑬', 'F': '𝑭', 'G': '𝑮',
        'H': '𝑯', 'I': '𝑰', 'J': '𝑱', 'K': '𝑲', 'L': '𝑳', 'M': '𝑴', 'N': '𝑵',
        'O': '𝑶', 'P': '𝑷', 'Q': '𝑸', 'R': '𝑹', 'S': '𝑺', 'T': '𝑻', 'U': '𝑼',
        'V': '𝑽', 'W': '𝑾', 'X': '𝑿', 'Y': '𝒀', 'Z': '𝒁',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_FRAKTUR = {
        'a': '𝔞', 'b': '𝔟', 'c': '𝔠', 'd': '𝔡', 'e': '𝔢', 'f': '𝔣', 'g': '𝔤',
        'h': '𝔥', 'i': '𝔦', 'j': '𝔧', 'k': '𝔨', 'l': '𝔩', 'm': '𝔪', 'n': '𝔫',
        'o': '𝔬', 'p': '𝔭', 'q': '𝔮', 'r': '𝔯', 's': '𝔰', 't': '𝔱', 'u': '𝔲',
        'v': '𝔳', 'w': '𝔴', 'x': '𝔵', 'y': '𝔶', 'z': '𝔷',
        'A': '𝔄', 'B': '𝔅', 'C': 'ℭ', 'D': '𝔇', 'E': '𝔈', 'F': '𝔉', 'G': '𝔊',
        'H': 'ℌ', 'I': 'ℑ', 'J': '𝔍', 'K': '𝔎', 'L': '𝔏', 'M': '𝔐', 'N': '𝔑',
        'O': '𝔒', 'P': '𝔓', 'Q': '𝔔', 'R': 'ℜ', 'S': '𝔖', 'T': '𝔗', 'U': '𝔘',
        'V': '𝔙', 'W': '𝔚', 'X': '𝔛', 'Y': '𝔜', 'Z': 'ℨ',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_BOLD_FRAKTUR = {
        'a': '𝖆', 'b': '𝖇', 'c': '𝖈', 'd': '𝖉', 'e': '𝖊', 'f': '𝖋', 'g': '𝖌',
        'h': '𝖍', 'i': '𝖎', 'j': '𝖏', 'k': '𝖐', 'l': '𝖑', 'm': '𝖒', 'n': '𝖓',
        'o': '𝖔', 'p': '𝖕', 'q': '𝖖', 'r': '𝖗', 's': '𝖘', 't': '𝖙', 'u': '𝖚',
        'v': '𝖛', 'w': '𝖜', 'x': '𝖝', 'y': '𝖞', 'z': '𝖟',
        'A': '𝕬', 'B': '𝕭', 'C': '𝕮', 'D': '𝕯', 'E': '𝕰', 'F': '𝕱', 'G': '𝕲',
        'H': '𝕳', 'I': '𝕴', 'J': '𝕵', 'K': '𝕶', 'L': '𝕷', 'M': '𝕸', 'N': '𝕹',
        'O': '𝕺', 'P': '𝕻', 'Q': '𝕼', 'R': '𝕽', 'S': '𝕾', 'T': '𝕿', 'U': '𝖀',
        'V': '𝖁', 'W': '𝖂', 'X': '𝖃', 'Y': '𝖄', 'Z': '𝖅',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_SCRIPT = {
        'a': '𝒶', 'b': '𝒷', 'c': '𝒸', 'd': '𝒹', 'e': 'ℯ', 'f': '𝒻', 'g': 'ℊ',
        'h': 'ℋ', 'i': '𝒾', 'j': '𝒿', 'k': '𝓀', 'l': '𝓁', 'm': '𝓂', 'n': '𝓃',
        'o': 'ℴ', 'p': '𝓅', 'q': '𝓆', 'r': '𝓇', 's': '𝓈', 't': '𝓉', 'u': '𝓊',
        'v': '𝓋', 'w': '𝓌', 'x': '𝓍', 'y': '𝓎', 'z': '𝓏',
        'A': '𝒜', 'B': 'ℬ', 'C': '𝒞', 'D': '𝒟', 'E': 'ℰ', 'F': 'ℱ', 'G': '𝒢',
        'H': 'ℋ', 'I': 'ℐ', 'J': '𝒥', 'K': '𝒦', 'L': 'ℒ', 'M': 'ℳ', 'N': '𝒩',
        'O': '𝒪', 'P': '𝒫', 'Q': '𝒬', 'R': 'ℛ', 'S': '𝒮', 'T': '𝒯', 'U': '𝒰',
        'V': '𝒱', 'W': '𝒲', 'X': '𝒳', 'Y': '𝒴', 'Z': '𝒵',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_BOLD_SCRIPT = {
        'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮', 'f': '𝓯', 'g': '𝓰',
        'h': '𝓱', 'i': '𝓲', 'j': '𝓳', 'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷',
        'o': '𝓸', 'p': '𝓹', 'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽', 'u': '𝓾',
        'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃',
        'A': '𝓐', 'B': '𝓑', 'C': '𝓒', 'D': '𝓓', 'E': '𝓔', 'F': '𝓕', 'G': '𝓖',
        'H': '𝓗', 'I': '𝓘', 'J': '𝓙', 'K': '𝓚', 'L': '𝓛', 'M': '𝓜', 'N': '𝓝',
        'O': '𝓞', 'P': '𝓟', 'Q': '𝓠', 'R': '𝓡', 'S': '𝓢', 'T': '𝓣', 'U': '𝓤',
        'V': '𝓥', 'W': '𝓦', 'X': '𝓧', 'Y': '𝓨', 'Z': '𝓩',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_DOUBLESTRUCK = {
        'a': '𝕒', 'b': '𝕓', 'c': '𝕔', 'd': '𝕕', 'e': '𝕖', 'f': '𝕗', 'g': '𝕘',
        'h': '𝕙', 'i': '𝕚', 'j': '𝕛', 'k': '𝕜', 'l': '𝕝', 'm': '𝕞', 'n': '𝕟',
        'o': '𝕠', 'p': '𝕡', 'q': '𝕢', 'r': '𝕣', 's': '𝕤', 't': '𝕥', 'u': '𝕦',
        'v': '𝕧', 'w': '𝕨', 'x': '𝕩', 'y': '𝕪', 'z': '𝕫',
        'A': '𝔸', 'B': '𝔹', 'C': 'ℂ', 'D': '𝔻', 'E': '𝔼', 'F': '𝔽', 'G': '𝔾',
        'H': 'ℍ', 'I': '𝕀', 'J': '𝕁', 'K': '𝕂', 'L': '𝕃', 'M': '𝕄', 'N': 'ℕ',
        'O': '𝕆', 'P': 'ℙ', 'Q': 'ℚ', 'R': 'ℝ', 'S': '𝕊', 'T': '𝕋', 'U': '𝕌',
        'V': '𝕍', 'W': '𝕎', 'X': '𝕏', 'Y': '𝕐', 'Z': 'ℤ',
        '0': '𝟘', '1': '𝟙', '2': '𝟚', '3': '𝟛', '4': '𝟜',
        '5': '𝟝', '6': '𝟞', '7': '𝟟', '8': '𝟠', '9': '𝟡',
    }
    _FONT_MONOSPACE = {
        'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏', 'g': '𝚐',
        'h': '𝚑', 'i': '𝚒', 'j': '𝚓', 'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗',
        'o': '𝚘', 'p': '𝚙', 'q': '𝚚', 'r': '𝚛', 's': '𝚜', 't': '𝚝', 'u': '𝚞',
        'v': '𝚟', 'w': '𝚠', 'x': '𝚡', 'y': '𝚢', 'z': '𝚣',
        'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶',
        'H': '𝙷', 'I': '𝙸', 'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽',
        'O': '𝙾', 'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄',
        'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉',
        '0': '𝟶', '1': '𝟷', '2': '𝟸', '3': '𝟹', '4': '𝟺',
        '5': '𝟻', '6': '𝟼', '7': '𝟽', '8': '𝟾', '9': '𝟿',
    }
    _FONT_SANS = {
        'a': '𝖺', 'b': '𝖻', 'c': '𝖼', 'd': '𝖽', 'e': '𝖾', 'f': '𝖿', 'g': '𝗀',
        'h': '𝗁', 'i': '𝗂', 'j': '𝗃', 'k': '𝗄', 'l': '𝗅', 'm': '𝗆', 'n': '𝗇',
        'o': '𝗈', 'p': '𝗉', 'q': '𝗊', 'r': '𝗋', 's': '𝗌', 't': '𝗍', 'u': '𝗎',
        'v': '𝗏', 'w': '𝗐', 'x': '𝗑', 'y': '𝗒', 'z': '𝗓',
        'A': '𝖠', 'B': '𝖡', 'C': '𝖢', 'D': '𝖣', 'E': '𝖤', 'F': '𝖥', 'G': '𝖦',
        'H': '𝖧', 'I': '𝖨', 'J': '𝖩', 'K': '𝖪', 'L': '𝖫', 'M': '𝖬', 'N': '𝖭',
        'O': '𝖮', 'P': '𝖯', 'Q': '𝖰', 'R': '𝖱', 'S': '𝖲', 'T': '𝖳', 'U': '𝖴',
        'V': '𝖵', 'W': '𝖶', 'X': '𝖷', 'Y': '𝖸', 'Z': '𝖹',
        '0': '𝟢', '1': '𝟣', '2': '𝟤', '3': '𝟥', '4': '𝟦',
        '5': '𝟧', '6': '𝟨', '7': '𝟩', '8': '𝟪', '9': '𝟫',
    }
    _FONT_SANS_BOLD = {
        'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴',
        'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻',
        'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂',
        'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
        'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚',
        'H': '𝗛', 'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡',
        'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨',
        'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭',
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰',
        '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵',
    }
    _FONT_SANS_ITALIC = {
        'a': '𝘢', 'b': '𝘣', 'c': '𝘤', 'd': '𝘥', 'e': '𝘦', 'f': '𝘧', 'g': '𝘨',
        'h': '𝘩', 'i': '𝘪', 'j': '𝘫', 'k': '𝘬', 'l': '𝘭', 'm': '𝘮', 'n': '𝘯',
        'o': '𝘰', 'p': '𝘱', 'q': '𝘲', 'r': '𝘳', 's': '𝘴', 't': '𝘵', 'u': '𝘶',
        'v': '𝘷', 'w': '𝘸', 'x': '𝘹', 'y': '𝘺', 'z': '𝘻',
        'A': '𝘈', 'B': '𝘉', 'C': '𝘊', 'D': '𝘋', 'E': '𝘌', 'F': '𝘍', 'G': '𝘎',
        'H': '𝘏', 'I': '𝘐', 'J': '𝘑', 'K': '𝘒', 'L': '𝘓', 'M': '𝘔', 'N': '𝘕',
        'O': '𝘖', 'P': '𝘗', 'Q': '𝘘', 'R': '𝘙', 'S': '𝘚', 'T': '𝘛', 'U': '𝘜',
        'V': '𝘝', 'W': '𝘞', 'X': '𝘟', 'Y': '𝘠', 'Z': '𝘡',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_SANS_BOLD_ITALIC = {
        'a': '𝙖', 'b': '𝙗', 'c': '𝙘', 'd': '𝙙', 'e': '𝙚', 'f': '𝙛', 'g': '𝙜',
        'h': '𝙝', 'i': '𝙞', 'j': '𝙟', 'k': '𝙠', 'l': '𝙡', 'm': '𝙢', 'n': '𝙣',
        'o': '𝙤', 'p': '𝙥', 'q': '𝙦', 'r': '𝙧', 's': '𝙨', 't': '𝙩', 'u': '𝙪',
        'v': '𝙫', 'w': '𝙬', 'x': '𝙭', 'y': '𝙮', 'z': '𝙯',
        'A': '𝘼', 'B': '𝘽', 'C': '𝘾', 'D': '𝘿', 'E': '𝙀', 'F': '𝙁', 'G': '𝙂',
        'H': '𝙃', 'I': '𝙄', 'J': '𝙅', 'K': '𝙆', 'L': '𝙇', 'M': '𝙈', 'N': '𝙉',
        'O': '𝙊', 'P': '𝙋', 'Q': '𝙌', 'R': '𝙍', 'S': '𝙎', 'T': '𝙏', 'U': '𝙐',
        'V': '𝙑', 'W': '𝙒', 'X': '𝙓', 'Y': '𝙔', 'Z': '𝙕',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_CIRCLE = {
        'a': 'ⓐ', 'b': 'ⓑ', 'c': 'ⓒ', 'd': 'ⓓ', 'e': 'ⓔ', 'f': 'ⓕ', 'g': 'ⓖ',
        'h': 'ⓗ', 'i': 'ⓘ', 'j': 'ⓙ', 'k': 'ⓚ', 'l': 'ⓛ', 'm': 'ⓜ', 'n': 'ⓝ',
        'o': 'ⓞ', 'p': 'ⓟ', 'q': 'ⓠ', 'r': 'ⓡ', 's': 'ⓢ', 't': 'ⓣ', 'u': 'ⓤ',
        'v': 'ⓥ', 'w': 'ⓦ', 'x': 'ⓧ', 'y': 'ⓨ', 'z': 'ⓩ',
        'A': 'Ⓐ', 'B': 'Ⓑ', 'C': 'Ⓒ', 'D': 'Ⓓ', 'E': 'Ⓔ', 'F': 'Ⓕ', 'G': 'Ⓖ',
        'H': 'Ⓗ', 'I': 'Ⓘ', 'J': 'Ⓙ', 'K': 'Ⓚ', 'L': 'Ⓛ', 'M': 'Ⓜ', 'N': 'Ⓝ',
        'O': 'Ⓞ', 'P': 'Ⓟ', 'Q': 'Ⓠ', 'R': 'Ⓡ', 'S': 'Ⓢ', 'T': 'Ⓣ', 'U': 'Ⓤ',
        'V': 'Ⓥ', 'W': 'Ⓦ', 'X': 'Ⓧ', 'Y': 'Ⓨ', 'Z': 'Ⓩ',
        '0': '⓪', '1': '①', '2': '②', '3': '③', '4': '④',
        '5': '⑤', '6': '⑥', '7': '⑦', '8': '⑧', '9': '⑨',
    }
    _FONT_SQUARE = {
        'a': '🄰', 'b': '🄱', 'c': '🄲', 'd': '🄳', 'e': '🄴', 'f': '🄵', 'g': '🄶',
        'h': '🄷', 'i': '🄸', 'j': '🄹', 'k': '🄺', 'l': '🄻', 'm': '🄼', 'n': '🄽',
        'o': '🄾', 'p': '🄿', 'q': '🅀', 'r': '🅁', 's': '🅂', 't': '🅃', 'u': '🅄',
        'v': '🅅', 'w': '🅆', 'x': '🅇', 'y': '🅈', 'z': '🅉',
        'A': '🄰', 'B': '🄱', 'C': '🄲', 'D': '🄳', 'E': '🄴', 'F': '🄵', 'G': '🄶',
        'H': '🄷', 'I': '🄸', 'J': '🄹', 'K': '🄺', 'L': '🄻', 'M': '🄼', 'N': '🄽',
        'O': '🄾', 'P': '🄿', 'Q': '🅀', 'R': '🅁', 'S': '🅂', 'T': '🅃', 'U': '🅄',
        'V': '🅅', 'W': '🅆', 'X': '🅇', 'Y': '🅈', 'Z': '🅉',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_NEGATIVE = {
        'a': '🅰', 'b': '🅱', 'c': '🅲', 'd': '🅳', 'e': '🅴', 'f': '🅵', 'g': '🅶',
        'h': '🅷', 'i': '🅸', 'j': '🅹', 'k': '🅺', 'l': '🅻', 'm': '🅼', 'n': '🅽',
        'o': '🅾', 'p': '🅿', 'q': '🆀', 'r': '🆁', 's': '🆂', 't': '🆃', 'u': '🆄',
        'v': '🆅', 'w': '🆆', 'x': '🆇', 'y': '🆈', 'z': '🆉',
        'A': '🅰', 'B': '🅱', 'C': '🅲', 'D': '🅳', 'E': '🅴', 'F': '🅵', 'G': '🅶',
        'H': '🅷', 'I': '🅸', 'J': '🅹', 'K': '🅺', 'L': '🅻', 'M': '🅼', 'N': '🅽',
        'O': '🅾', 'P': '🅿', 'Q': '🆀', 'R': '🆁', 'S': '🆂', 'T': '🆃', 'U': '🆄',
        'V': '🆅', 'W': '🆆', 'X': '🆇', 'Y': '🆈', 'Z': '🆉',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_FULLWIDTH = {
        'a': 'ａ', 'b': 'ｂ', 'c': 'ｃ', 'd': 'ｄ', 'e': 'ｅ', 'f': 'ｆ', 'g': 'ｇ',
        'h': 'ｈ', 'i': 'ｉ', 'j': 'ｊ', 'k': 'ｋ', 'l': 'ｌ', 'm': 'ｍ', 'n': 'ｎ',
        'o': 'ｏ', 'p': 'ｐ', 'q': 'ｑ', 'r': 'ｒ', 's': 'ｓ', 't': 'ｔ', 'u': 'ｕ',
        'v': 'ｖ', 'w': 'ｗ', 'x': 'ｘ', 'y': 'ｙ', 'z': 'ｚ',
        'A': 'Ａ', 'B': 'Ｂ', 'C': 'Ｃ', 'D': 'Ｄ', 'E': 'Ｅ', 'F': 'Ｆ', 'G': 'Ｇ',
        'H': 'Ｈ', 'I': 'Ｉ', 'J': 'Ｊ', 'K': 'Ｋ', 'L': 'Ｌ', 'M': 'Ｍ', 'N': 'Ｎ',
        'O': 'Ｏ', 'P': 'Ｐ', 'Q': 'Ｑ', 'R': 'Ｒ', 'S': 'Ｓ', 'T': 'Ｔ', 'U': 'Ｕ',
        'V': 'Ｖ', 'W': 'Ｗ', 'X': 'Ｘ', 'Y': 'Ｙ', 'Z': 'Ｚ',
        '0': '０', '1': '１', '2': '２', '3': '３', '4': '４',
        '5': '５', '6': '６', '7': '７', '8': '８', '9': '９',
    }
    _FONT_SMALL = {
        'a': 'ᵃ', 'b': 'ᵇ', 'c': 'ᶜ', 'd': 'ᵈ', 'e': 'ᵉ', 'f': 'ᶠ', 'g': 'ᵍ',
        'h': 'ʰ', 'i': 'ⁱ', 'j': 'ʲ', 'k': 'ᵏ', 'l': 'ˡ', 'm': 'ᵐ', 'n': 'ⁿ',
        'o': 'ᵒ', 'p': 'ᵖ', 'q': 'ᑫ', 'r': 'ʳ', 's': 'ˢ', 't': 'ᵗ', 'u': 'ᵘ',
        'v': 'ᵛ', 'w': 'ʷ', 'x': 'ˣ', 'y': 'ʸ', 'z': 'ᶻ',
        'A': 'ᴬ', 'B': 'ᴮ', 'C': 'ᶜ', 'D': 'ᴰ', 'E': 'ᴱ', 'F': 'ᶠ', 'G': 'ᴳ',
        'H': 'ᴴ', 'I': 'ᴵ', 'J': 'ᴶ', 'K': 'ᴷ', 'L': 'ᴸ', 'M': 'ᴹ', 'N': 'ᴺ',
        'O': 'ᴼ', 'P': 'ᴾ', 'Q': 'ᑫ', 'R': 'ᴿ', 'S': 'ˢ', 'T': 'ᵀ', 'U': 'ᵁ',
        'V': 'ⱽ', 'W': 'ᵂ', 'X': 'ˣ', 'Y': 'ʸ', 'Z': 'ᶻ',
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
    }
    _FONT_FANCY = {
        'a': 'α', 'b': 'в', 'c': '¢', 'd': '∂', 'e': 'є', 'f': 'ƒ', 'g': 'g',
        'h': 'н', 'i': 'ι', 'j': 'נ', 'k': 'к', 'l': 'ℓ', 'm': 'м', 'n': 'η',
        'o': 'σ', 'p': 'ρ', 'q': 'q', 'r': 'я', 's': 'ѕ', 't': 'т', 'u': 'υ',
        'v': 'ν', 'w': 'ω', 'x': 'χ', 'y': 'у', 'z': 'z',
        'A': 'Α', 'B': 'β', 'C': '¢', 'D': '∂', 'E': 'є', 'F': 'ƒ', 'G': 'g',
        'H': 'н', 'I': 'ι', 'J': 'נ', 'K': 'к', 'L': 'ℓ', 'M': 'м', 'N': 'η',
        'O': 'σ', 'P': 'ρ', 'Q': 'q', 'R': 'я', 'S': 'ѕ', 'T': 'т', 'U': 'υ',
        'V': 'ν', 'W': 'ω', 'X': 'χ', 'Y': 'у', 'Z': 'z',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_BOXED = {
        'a': '🄰', 'b': '🄱', 'c': '🄲', 'd': '🄳', 'e': '🄴', 'f': '🄵', 'g': '🄶',
        'h': '🄷', 'i': '🄸', 'j': '🄹', 'k': '🄺', 'l': '🄻', 'm': '🄼', 'n': '🄽',
        'o': '🄾', 'p': '🄿', 'q': '🅀', 'r': '🅁', 's': '🅂', 't': '🅃', 'u': '🅄',
        'v': '🅅', 'w': '🅆', 'x': '🅇', 'y': '🅈', 'z': '🅉',
        'A': '🄰', 'B': '🄱', 'C': '🄲', 'D': '🄳', 'E': '🄴', 'F': '🄵', 'G': '🄶',
        'H': '🄷', 'I': '🄸', 'J': '🄹', 'K': '🄺', 'L': '🄻', 'M': '🄼', 'N': '🄽',
        'O': '🄾', 'P': '🄿', 'Q': '🅀', 'R': '🅁', 'S': '🅂', 'T': '🅃', 'U': '🅄',
        'V': '🅅', 'W': '🅆', 'X': '🅇', 'Y': '🅈', 'Z': '🅉',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_CROSSED = {
        'a': 'a̶', 'b': 'b̶', 'c': 'c̶', 'd': 'd̶', 'e': 'e̶', 'f': 'f̶', 'g': 'g̶',
        'h': 'h̶', 'i': 'i̶', 'j': 'j̶', 'k': 'k̶', 'l': 'l̶', 'm': 'm̶', 'n': 'n̶',
        'o': 'o̶', 'p': 'p̶', 'q': 'q̶', 'r': 'r̶', 's': 's̶', 't': 't̶', 'u': 'u̶',
        'v': 'v̶', 'w': 'w̶', 'x': 'x̶', 'y': 'y̶', 'z': 'z̶',
        'A': 'A̶', 'B': 'B̶', 'C': 'C̶', 'D': 'D̶', 'E': 'E̶', 'F': 'F̶', 'G': 'G̶',
        'H': 'H̶', 'I': 'I̶', 'J': 'J̶', 'K': 'K̶', 'L': 'L̶', 'M': 'M̶', 'N': 'N̶',
        'O': 'O̶', 'P': 'P̶', 'Q': 'Q̶', 'R': 'R̶', 'S': 'S̶', 'T': 'T̶', 'U': 'U̶',
        'V': 'V̶', 'W': 'W̶', 'X': 'X̶', 'Y': 'Y̶', 'Z': 'Z̶',
        '0': '0̶', '1': '1̶', '2': '2̶', '3': '3̶', '4': '4̶',
        '5': '5̶', '6': '6̶', '7': '7̶', '8': '8̶', '9': '9̶',
    }
    _FONT_UNDERLINED = {
        'a': 'a̳', 'b': 'b̳', 'c': 'c̳', 'd': 'd̳', 'e': 'e̳', 'f': 'f̳', 'g': 'g̳',
        'h': 'h̳', 'i': 'i̳', 'j': 'j̳', 'k': 'k̳', 'l': 'l̳', 'm': 'm̳', 'n': 'n̳',
        'o': 'o̳', 'p': 'p̳', 'q': 'q̳', 'r': 'r̳', 's': 's̳', 't': 't̳', 'u': 'u̳',
        'v': 'v̳', 'w': 'w̳', 'x': 'x̳', 'y': 'y̳', 'z': 'z̳',
        'A': 'A̳', 'B': 'B̳', 'C': 'C̳', 'D': 'D̳', 'E': 'E̳', 'F': 'F̳', 'G': 'G̳',
        'H': 'H̳', 'I': 'I̳', 'J': 'J̳', 'K': 'K̳', 'L': 'L̳', 'M': 'M̳', 'N': 'N̳',
        'O': 'O̳', 'P': 'P̳', 'Q': 'Q̳', 'R': 'R̳', 'S': 'S̳', 'T': 'T̳', 'U': 'U̳',
        'V': 'V̳', 'W': 'W̳', 'X': 'X̳', 'Y': 'Y̳', 'Z': 'Z̳',
        '0': '0̳', '1': '1̳', '2': '2̳', '3': '3̳', '4': '4̳',
        '5': '5̳', '6': '6̳', '7': '7̳', '8': '8̳', '9': '9̳',
    }
    _FONT_STARRIGHT = {
        'a': 'a⋆', 'b': 'b⋆', 'c': 'c⋆', 'd': 'd⋆', 'e': 'e⋆', 'f': 'f⋆', 'g': 'g⋆',
        'h': 'h⋆', 'i': 'i⋆', 'j': 'j⋆', 'k': 'k⋆', 'l': 'l⋆', 'm': 'm⋆', 'n': 'n⋆',
        'o': 'o⋆', 'p': 'p⋆', 'q': 'q⋆', 'r': 'r⋆', 's': 's⋆', 't': 't⋆', 'u': 'u⋆',
        'v': 'v⋆', 'w': 'w⋆', 'x': 'x⋆', 'y': 'y⋆', 'z': 'z⋆',
        'A': 'A⋆', 'B': 'B⋆', 'C': 'C⋆', 'D': 'D⋆', 'E': 'E⋆', 'F': 'F⋆', 'G': 'G⋆',
        'H': 'H⋆', 'I': 'I⋆', 'J': 'J⋆', 'K': 'K⋆', 'L': 'L⋆', 'M': 'M⋆', 'N': 'N⋆',
        'O': 'O⋆', 'P': 'P⋆', 'Q': 'Q⋆', 'R': 'R⋆', 'S': 'S⋆', 'T': 'T⋆', 'U': 'U⋆',
        'V': 'V⋆', 'W': 'W⋆', 'X': 'X⋆', 'Y': 'Y⋆', 'Z': 'Z⋆',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_STARLEFT = {
        'a': '⋆a', 'b': '⋆b', 'c': '⋆c', 'd': '⋆d', 'e': '⋆e', 'f': '⋆f', 'g': '⋆g',
        'h': '⋆h', 'i': '⋆i', 'j': '⋆j', 'k': '⋆k', 'l': '⋆l', 'm': '⋆m', 'n': '⋆n',
        'o': '⋆o', 'p': '⋆p', 'q': '⋆q', 'r': '⋆r', 's': '⋆s', 't': '⋆t', 'u': '⋆u',
        'v': '⋆v', 'w': '⋆w', 'x': '⋆x', 'y': '⋆y', 'z': '⋆z',
        'A': '⋆A', 'B': '⋆B', 'C': '⋆C', 'D': '⋆D', 'E': '⋆E', 'F': '⋆F', 'G': '⋆G',
        'H': '⋆H', 'I': '⋆I', 'J': '⋆J', 'K': '⋆K', 'L': '⋆L', 'M': '⋆M', 'N': '⋆N',
        'O': '⋆O', 'P': '⋆P', 'Q': '⋆Q', 'R': '⋆R', 'S': '⋆S', 'T': '⋆T', 'U': '⋆U',
        'V': '⋆V', 'W': '⋆W', 'X': '⋆X', 'Y': '⋆Y', 'Z': '⋆Z',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }
    _FONT_SPARKLE = {
        'a': 'a✧', 'b': 'b✧', 'c': 'c✧', 'd': 'd✧', 'e': 'e✧', 'f': 'f✧', 'g': 'g✧',
        'h': 'h✧', 'i': 'i✧', 'j': 'j✧', 'k': 'k✧', 'l': 'l✧', 'm': 'm✧', 'n': 'n✧',
        'o': 'o✧', 'p': 'p✧', 'q': 'q✧', 'r': 'r✧', 's': 's✧', 't': 't✧', 'u': 'u✧',
        'v': 'v✧', 'w': 'w✧', 'x': 'x✧', 'y': 'y✧', 'z': 'z✧',
        'A': 'A✧', 'B': 'B✧', 'C': 'C✧', 'D': 'D✧', 'E': 'E✧', 'F': 'F✧', 'G': 'G✧',
        'H': 'H✧', 'I': 'I✧', 'J': 'J✧', 'K': 'K✧', 'L': 'L✧', 'M': 'M✧', 'N': 'N✧',
        'O': 'O✧', 'P': 'P✧', 'Q': 'Q✧', 'R': 'R✧', 'S': 'S✧', 'T': 'T✧', 'U': 'U✧',
        'V': 'V✧', 'W': 'W✧', 'X': 'X✧', 'Y': 'Y✧', 'Z': 'Z✧',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }

    def _apply_font(text, mapping):
        result = []
        for ch in text:
            result.append(mapping.get(ch, ch))
        return "".join(result)

    def _get_text(message):
        """Get text from args or reply."""
        args = message.text.split(None, 1)
        if len(args) > 1:
            return args[1]
        if message.reply_to_message:
            return message.reply_to_message.text or message.reply_to_message.caption or ""
        return None

    # ═══════════════════════════════════════════════════════════════
    #  CASE (10 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("upper", prefixes=".") & filters.me)
    async def upper_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.upper <text>` or reply")
            return
        await message.edit(f"🔠 **UPPER:**\n{text.upper()}")

    register_command("Text", "upper", "Convert text to UPPERCASE", [])

    @app.on_message(filters.command("lower", prefixes=".") & filters.me)
    async def lower_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.lower <text>` or reply")
            return
        await message.edit(f"🔡 **lower:**\n{text.lower()}")

    register_command("Text", "lower", "Convert text to lowercase", [])

    @app.on_message(filters.command("title", prefixes=".") & filters.me)
    async def title_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.title <text>` or reply")
            return
        await message.edit(f"📝 **Title:**\n{text.title()}")

    register_command("Text", "title", "Convert text to Title Case", [])

    @app.on_message(filters.command("capitalize", prefixes=".") & filters.me)
    async def capitalize_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.capitalize <text>` or reply")
            return
        await message.edit(f"✏️ **Capitalized:**\n{text.capitalize()}")

    register_command("Text", "capitalize", "Capitalize first letter", [])

    @app.on_message(filters.command("swapcase", prefixes=".") & filters.me)
    async def swapcase_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.swapcase <text>` or reply")
            return
        await message.edit(f"🔄 **SwapCase:**\n{text.swapcase()}")

    register_command("Text", "swapcase", "Swap case of each character", [])

    @app.on_message(filters.command("sentence", prefixes=".") & filters.me)
    async def sentence_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.sentence <text>` or reply")
            return
        result = ". ".join(s.strip().capitalize() for s in text.split("."))
        await message.edit(f"📝 **Sentence case:**\n{result}")

    register_command("Text", "sentence", "Convert to sentence case", [])

    @app.on_message(filters.command("inverse_case", prefixes=".") & filters.me)
    async def inverse_case_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.inverse_case <text>` or reply")
            return
        await message.edit(f"🔄 **Inverse Case:**\n{text.swapcase()}")

    register_command("Text", "inverse_case", "Inverse case of text", [])

    @app.on_message(filters.command("toggle_case", prefixes=".") & filters.me)
    async def toggle_case_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.toggle_case <text>` or reply")
            return
        await message.edit(f"🔄 **Toggle Case:**\n{text.swapcase()}")

    register_command("Text", "toggle_case", "Toggle case of text", [])

    @app.on_message(filters.command("proper", prefixes=".") & filters.me)
    async def proper_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.proper <text>` or reply")
            return
        result = " ".join(w.capitalize() for w in text.split())
        await message.edit(f"✨ **Proper:**\n{result}")

    register_command("Text", "proper", "Proper case each word", [])

    @app.on_message(filters.command("capitalize_all", prefixes=".") & filters.me)
    async def capitalize_all_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.capitalize_all <text>` or reply")
            return
        result = " ".join(w.capitalize() for w in text.split())
        await message.edit(f"✏️ **Capitalize All:**\n{result}")

    register_command("Text", "capitalize_all", "Capitalize first letter of every word", [])

    # ═══════════════════════════════════════════════════════════════
    #  UNICODE FONTS (25 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("bold", prefixes=".") & filters.me)
    async def bold_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.bold <text>`")
            return
        await message.edit(_apply_font(text, _FONT_BOLD))

    register_command("Text", "bold", "Bold Unicode font", [])

    @app.on_message(filters.command("italic", prefixes=".") & filters.me)
    async def italic_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.italic <text>`")
            return
        await message.edit(_apply_font(text, _FONT_ITALIC))

    register_command("Text", "italic", "Italic Unicode font", [])

    @app.on_message(filters.command("bolditalic", prefixes=".") & filters.me)
    async def bolditalic_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.bolditalic <text>`")
            return
        await message.edit(_apply_font(text, _FONT_BOLD_ITALIC))

    register_command("Text", "bolditalic", "Bold Italic Unicode font", [])

    @app.on_message(filters.command("fraktur", prefixes=".") & filters.me)
    async def fraktur_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.fraktur <text>`")
            return
        await message.edit(_apply_font(text, _FONT_FRAKTUR))

    register_command("Text", "fraktur", "Fraktur Unicode font", [])

    @app.on_message(filters.command("boldfraktur", prefixes=".") & filters.me)
    async def boldfraktur_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.boldfraktur <text>`")
            return
        await message.edit(_apply_font(text, _FONT_BOLD_FRAKTUR))

    register_command("Text", "boldfraktur", "Bold Fraktur Unicode font", [])

    @app.on_message(filters.command("script", prefixes=".") & filters.me)
    async def script_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.script <text>`")
            return
        await message.edit(_apply_font(text, _FONT_SCRIPT))

    register_command("Text", "script", "Script Unicode font", [])

    @app.on_message(filters.command("boldscript", prefixes=".") & filters.me)
    async def boldscript_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.boldscript <text>`")
            return
        await message.edit(_apply_font(text, _FONT_BOLD_SCRIPT))

    register_command("Text", "boldscript", "Bold Script Unicode font", [])

    @app.on_message(filters.command("doublestruck", prefixes=".") & filters.me)
    async def doublestruck_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.doublestruck <text>`")
            return
        await message.edit(_apply_font(text, _FONT_DOUBLESTRUCK))

    register_command("Text", "doublestruck", "Double-struck Unicode font", [])

    @app.on_message(filters.command("monospace", prefixes=".") & filters.me)
    async def monospace_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.monospace <text>`")
            return
        await message.edit(_apply_font(text, _FONT_MONOSPACE))

    register_command("Text", "monospace", "Monospace Unicode font", [])

    @app.on_message(filters.command("sans", prefixes=".") & filters.me)
    async def sans_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.sans <text>`")
            return
        await message.edit(_apply_font(text, _FONT_SANS))

    register_command("Text", "sans", "Sans-serif Unicode font", [])

    @app.on_message(filters.command("sansbold", prefixes=".") & filters.me)
    async def sansbold_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.sansbold <text>`")
            return
        await message.edit(_apply_font(text, _FONT_SANS_BOLD))

    register_command("Text", "sansbold", "Sans Bold Unicode font", [])

    @app.on_message(filters.command("sansitalic", prefixes=".") & filters.me)
    async def sansitalic_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.sansitalic <text>`")
            return
        await message.edit(_apply_font(text, _FONT_SANS_ITALIC))

    register_command("Text", "sansitalic", "Sans Italic Unicode font", [])

    @app.on_message(filters.command("sansbolditalic", prefixes=".") & filters.me)
    async def sansbolditalic_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.sansbolditalic <text>`")
            return
        await message.edit(_apply_font(text, _FONT_SANS_BOLD_ITALIC))

    register_command("Text", "sansbolditalic", "Sans Bold Italic Unicode font", [])

    @app.on_message(filters.command("circle", prefixes=".") & filters.me)
    async def circle_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.circle <text>`")
            return
        await message.edit(_apply_font(text, _FONT_CIRCLE))

    register_command("Text", "circle", "Circled Unicode font", [])

    @app.on_message(filters.command("square", prefixes=".") & filters.me)
    async def square_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.square <text>`")
            return
        await message.edit(_apply_font(text, _FONT_SQUARE))

    register_command("Text", "square", "Squared Unicode font", [])

    @app.on_message(filters.command("negative", prefixes=".") & filters.me)
    async def negative_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.negative <text>`")
            return
        await message.edit(_apply_font(text, _FONT_NEGATIVE))

    register_command("Text", "negative", "Negative squared Unicode font", [])

    @app.on_message(filters.command("fullwidth", prefixes=".") & filters.me)
    async def fullwidth_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.fullwidth <text>`")
            return
        await message.edit(_apply_font(text, _FONT_FULLWIDTH))

    register_command("Text", "fullwidth", "Fullwidth Unicode font", [])

    @app.on_message(filters.command("small", prefixes=".") & filters.me)
    async def small_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.small <text>`")
            return
        await message.edit(_apply_font(text, _FONT_SMALL))

    register_command("Text", "small", "Small/superscript Unicode font", [])

    @app.on_message(filters.command("fancy", prefixes=".") & filters.me)
    async def fancy_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.fancy <text>`")
            return
        await message.edit(_apply_font(text, _FONT_FANCY))

    register_command("Text", "fancy", "Fancy Unicode font", [])

    @app.on_message(filters.command("boxed", prefixes=".") & filters.me)
    async def boxed_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.boxed <text>`")
            return
        await message.edit(_apply_font(text, _FONT_BOXED))

    register_command("Text", "boxed", "Boxed Unicode font", [])

    @app.on_message(filters.command("crossed", prefixes=".") & filters.me)
    async def crossed_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.crossed <text>`")
            return
        await message.edit(_apply_font(text, _FONT_CROSSED))

    register_command("Text", "crossed", "Crossed-out Unicode font", [])

    @app.on_message(filters.command("underlined", prefixes=".") & filters.me)
    async def underlined_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.underlined <text>`")
            return
        await message.edit(_apply_font(text, _FONT_UNDERLINED))

    register_command("Text", "underlined", "Underlined Unicode font", [])

    @app.on_message(filters.command("starright", prefixes=".") & filters.me)
    async def starright_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.starright <text>`")
            return
        await message.edit(_apply_font(text, _FONT_STARRIGHT))

    register_command("Text", "starright", "Star right decoration font", [])

    @app.on_message(filters.command("starleft", prefixes=".") & filters.me)
    async def starleft_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.starleft <text>`")
            return
        await message.edit(_apply_font(text, _FONT_STARLEFT))

    register_command("Text", "starleft", "Star left decoration font", [])

    @app.on_message(filters.command("sparkle", prefixes=".") & filters.me)
    async def sparkle_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.sparkle <text>`")
            return
        await message.edit(_apply_font(text, _FONT_SPARKLE))

    register_command("Text", "sparkle", "Sparkle decoration font", [])

    # ═══════════════════════════════════════════════════════════════
    #  DECORATIONS (20 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command(["vaporwave", "vapor"], prefixes=".") & filters.me)
    async def vaporwave_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.vaporwave <text>`")
            return
        result = " ".join(text) + "  " + " ".join(text)
        await message.edit(f"🌊 {result}")

    register_command("Text", "vaporwave", "Vaporwave style text", ["vapor"])

    @app.on_message(filters.command("aesthetic", prefixes=".") & filters.me)
    async def aesthetic_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.aesthetic <text>`")
            return
        result = " ".join(text)
        await message.edit(result)

    register_command("Text", "aesthetic", "Aesthetic spaced text", [])

    @app.on_message(filters.command("clap", prefixes=".") & filters.me)
    async def clap_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.clap <text>`")
            return
        result = " 👏 ".join(text.split())
        await message.edit(f"{result} 👏")

    register_command("Text", "clap", "Add clap emojis between words", [])

    @app.on_message(filters.command("space", prefixes=".") & filters.me)
    async def space_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.space <text>`")
            return
        result = "   ".join(text.split())
        await message.edit(result)

    register_command("Text", "space", "Triple space between words", [])

    @app.on_message(filters.command(["reverse", "rev"], prefixes=".") & filters.me)
    async def reverse_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.reverse <text>`")
            return
        await message.edit(f"🔄 **Reversed:**\n{text[::-1]}")

    register_command("Text", "reverse", "Reverse text", ["rev"])

    @app.on_message(filters.command("mock", prefixes=".") & filters.me)
    async def mock_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.mock <text>`")
            return
        result = "".join(
            c.upper() if i % 2 else c.lower() for i, c in enumerate(text)
        )
        await message.edit(result)

    register_command("Text", "mock", "MoCkInG sPoNgEbOb text", [])

    @app.on_message(filters.command("uwu", prefixes=".") & filters.me)
    async def uwu_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.uwu <text>`")
            return
        result = text.replace("r", "w").replace("l", "w").replace("R", "W").replace("L", "W")
        result = result.replace("no", "nu").replace("No", "Nu")
        result += " uwu"
        await message.edit(result)

    register_command("Text", "uwu", "UwU-fy text", [])

    @app.on_message(filters.command("owo", prefixes=".") & filters.me)
    async def owo_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.owo <text>`")
            return
        result = text.replace("r", "w").replace("l", "w").replace("R", "W").replace("L", "W")
        result += " owo"
        await message.edit(result)

    register_command("Text", "owo", "OwO-fy text", [])

    @app.on_message(filters.command("zalgo", prefixes=".") & filters.me)
    async def zalgo_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.zalgo <text>`")
            return
        zalgo_chars = [chr(c) for c in range(0x0300, 0x036F)]
        result = []
        for ch in text:
            result.append(ch)
            for _ in range(random.randint(1, 5)):
                result.append(random.choice(zalgo_chars))
        await message.edit("".join(result))

    register_command("Text", "zalgo", "Add Zalgo combining characters", [])

    @app.on_message(filters.command("strike", prefixes=".") & filters.me)
    async def strike_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.strike <text>`")
            return
        result = "".join(f"{ch}\u0336" for ch in text)
        await message.edit(result)

    register_command("Text", "strike", "Strikethrough text", [])

    @app.on_message(filters.command("underline", prefixes=".") & filters.me)
    async def underline_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.underline <text>`")
            return
        result = "".join(f"{ch}\u0332" for ch in text)
        await message.edit(result)

    register_command("Text", "underline", "Underline text", [])

    @app.on_message(filters.command("doubleline", prefixes=".") & filters.me)
    async def doubleline_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.doubleline <text>`")
            return
        result = "".join(f"{ch}\u0333" for ch in text)
        await message.edit(result)

    register_command("Text", "doubleline", "Double underline text", [])

    @app.on_message(filters.command("slash", prefixes=".") & filters.me)
    async def slash_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.slash <text>`")
            return
        result = "".join(f"{ch}\u0337" for ch in text)
        await message.edit(result)

    register_command("Text", "slash", "Slash through text", [])

    @app.on_message(filters.command("dot", prefixes=".") & filters.me)
    async def dot_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.dot <text>`")
            return
        result = "".join(f"{ch}\u0307" for ch in text)
        await message.edit(result)

    register_command("Text", "dot", "Dot above each character", [])

    @app.on_message(filters.command("star", prefixes=".") & filters.me)
    async def star_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.star <text>`")
            return
        result = "".join(f"{ch}\u0309" for ch in text)
        await message.edit(result)

    register_command("Text", "star", "Star above each character", [])

    @app.on_message(filters.command("dash", prefixes=".") & filters.me)
    async def dash_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.dash <text>`")
            return
        result = text.replace(" ", "-")
        await message.edit(result)

    register_command("Text", "dash", "Replace spaces with dashes", [])

    @app.on_message(filters.command("wave", prefixes=".") & filters.me)
    async def wave_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.wave <text>`")
            return
        result = text.replace(" ", " 〰 ")
        await message.edit(result)

    register_command("Text", "wave", "Wave decoration between words", [])

    @app.on_message(filters.command("arrow", prefixes=".") & filters.me)
    async def arrow_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.arrow <text>`")
            return
        result = " ➜ ".join(text.split())
        await message.edit(result)

    register_command("Text", "arrow", "Arrow between words", [])

    @app.on_message(filters.command("bullet", prefixes=".") & filters.me)
    async def bullet_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.bullet <text>`")
            return
        result = " • ".join(text.split())
        await message.edit(result)

    register_command("Text", "bullet", "Bullet between words", [])

    @app.on_message(filters.command("heart", prefixes=".") & filters.me)
    async def heart_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.heart <text>`")
            return
        result = " ❤️ ".join(text.split())
        await message.edit(result)

    register_command("Text", "heart", "Heart between words", [])

    # ═══════════════════════════════════════════════════════════════
    #  ENCRYPTION (29 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("caesar_e", prefixes=".") & filters.me)
    async def caesar_e_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.caesar_e <shift> <text>`")
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

    register_command("Text", "caesar_e", "Caesar cipher encrypt", [])

    @app.on_message(filters.command("caesar_d", prefixes=".") & filters.me)
    async def caesar_d_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.caesar_d <shift> <text>`")
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

    register_command("Text", "caesar_d", "Caesar cipher decrypt", [])

    @app.on_message(filters.command("atbash_e", prefixes=".") & filters.me)
    async def atbash_e_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.atbash_e <text>`")
            return
        result = []
        for c in text:
            if c.isalpha():
                base = ord("A") if c.isupper() else ord("a")
                result.append(chr(base + (25 - (ord(c) - base))))
            else:
                result.append(c)
        await message.edit(f"🔒 **Atbash:**\n`{''.join(result)}`")

    register_command("Text", "atbash_e", "Atbash cipher encrypt", [])

    @app.on_message(filters.command("atbash_d", prefixes=".") & filters.me)
    async def atbash_d_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.atbash_d <text>`")
            return
        result = []
        for c in text:
            if c.isalpha():
                base = ord("A") if c.isupper() else ord("a")
                result.append(chr(base + (25 - (ord(c) - base))))
            else:
                result.append(c)
        await message.edit(f"🔓 **Atbash:**\n`{''.join(result)}`")

    register_command("Text", "atbash_d", "Atbash cipher decrypt", [])

    @app.on_message(filters.command("rot13", prefixes=".") & filters.me)
    async def rot13_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.rot13 <text>`")
            return
        result = text.translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
        ))
        await message.edit(f"🔄 **ROT13:**\n`{result}`")

    register_command("Text", "rot13", "ROT13 encode/decode", [])

    @app.on_message(filters.command("rot47", prefixes=".") & filters.me)
    async def rot47_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.rot47 <text>`")
            return
        result = []
        for c in text:
            n = ord(c)
            if 33 <= n <= 126:
                result.append(chr(33 + (n - 33 + 47) % 94))
            else:
                result.append(c)
        await message.edit(f"🔄 **ROT47:**\n`{''.join(result)}`")

    register_command("Text", "rot47", "ROT47 encode/decode", [])

    @app.on_message(filters.command("vigenere_e", prefixes=".") & filters.me)
    async def vigenere_e_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.vigenere_e <key> <text>`")
            return
        key = args[1].upper()
        text = args[2]
        result = []
        ki = 0
        for c in text:
            if c.isalpha():
                base = ord("A") if c.isupper() else ord("a")
                shift = ord(key[ki % len(key)]) - ord("A")
                result.append(chr(base + (ord(c) - base + shift) % 26))
                ki += 1
            else:
                result.append(c)
        await message.edit(f"🔒 **Vigenère (key={key}):**\n`{''.join(result)}`")

    register_command("Text", "vigenere_e", "Vigenère cipher encrypt", [])

    @app.on_message(filters.command("vigenere_d", prefixes=".") & filters.me)
    async def vigenere_d_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.vigenere_d <key> <text>`")
            return
        key = args[1].upper()
        text = args[2]
        result = []
        ki = 0
        for c in text:
            if c.isalpha():
                base = ord("A") if c.isupper() else ord("a")
                shift = ord(key[ki % len(key)]) - ord("A")
                result.append(chr(base + (ord(c) - base - shift) % 26))
                ki += 1
            else:
                result.append(c)
        await message.edit(f"🔓 **Vigenère (key={key}):**\n`{''.join(result)}`")

    register_command("Text", "vigenere_d", "Vigenère cipher decrypt", [])

    @app.on_message(filters.command("base64_e", prefixes=".") & filters.me)
    async def base64_e_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.base64_e <text>`")
            return
        encoded = base64.b64encode(text.encode()).decode()
        await message.edit(f"🔒 **Base64 Encoded:**\n`{encoded}`")

    register_command("Text", "base64_e", "Base64 encode", [])

    @app.on_message(filters.command("base64_d", prefixes=".") & filters.me)
    async def base64_d_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.base64_d <encoded>`")
            return
        try:
            decoded = base64.b64decode(text.strip()).decode(errors="replace")
            await message.edit(f"🔓 **Base64 Decoded:**\n`{decoded}`")
        except Exception as e:
            await message.edit(f"❌ **Decode error:** `{e}`")

    register_command("Text", "base64_d", "Base64 decode", [])

    @app.on_message(filters.command("base32_e", prefixes=".") & filters.me)
    async def base32_e_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.base32_e <text>`")
            return
        encoded = base64.b32encode(text.encode()).decode()
        await message.edit(f"🔒 **Base32 Encoded:**\n`{encoded}`")

    register_command("Text", "base32_e", "Base32 encode", [])

    @app.on_message(filters.command("base32_d", prefixes=".") & filters.me)
    async def base32_d_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.base32_d <encoded>`")
            return
        try:
            decoded = base64.b32decode(text.strip()).decode(errors="replace")
            await message.edit(f"🔓 **Base32 Decoded:**\n`{decoded}`")
        except Exception as e:
            await message.edit(f"❌ **Decode error:** `{e}`")

    register_command("Text", "base32_d", "Base32 decode", [])

    @app.on_message(filters.command("hex_e", prefixes=".") & filters.me)
    async def hex_e_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.hex_e <text>`")
            return
        encoded = text.encode().hex()
        await message.edit(f"🔒 **Hex Encoded:**\n`{encoded}`")

    register_command("Text", "hex_e", "Hex encode", [])

    @app.on_message(filters.command("hex_d", prefixes=".") & filters.me)
    async def hex_d_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.hex_d <hex_string>`")
            return
        try:
            decoded = bytes.fromhex(text.strip()).decode(errors="replace")
            await message.edit(f"🔓 **Hex Decoded:**\n`{decoded}`")
        except ValueError:
            await message.edit("❌ Invalid hex string.")

    register_command("Text", "hex_d", "Hex decode", [])

    @app.on_message(filters.command("binary_e", prefixes=".") & filters.me)
    async def binary_e_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.binary_e <text>`")
            return
        encoded = " ".join(format(ord(c), "08b") for c in text)
        await message.edit(f"🔒 **Binary Encoded:**\n`{encoded}`")

    register_command("Text", "binary_e", "Binary encode", [])

    @app.on_message(filters.command("binary_d", prefixes=".") & filters.me)
    async def binary_d_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.binary_d <binary>`")
            return
        try:
            chunks = text.strip().split()
            decoded = "".join(chr(int(b, 2)) for b in chunks)
            await message.edit(f"🔓 **Binary Decoded:**\n`{decoded}`")
        except (ValueError, OverflowError):
            await message.edit("❌ Invalid binary values.")

    register_command("Text", "binary_d", "Binary decode", [])

    @app.on_message(filters.command("morse_e", prefixes=".") & filters.me)
    async def morse_e_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.morse_e <text>`")
            return
        encoded = []
        for c in text.upper():
            if c in _MORSE:
                encoded.append(_MORSE[c])
            else:
                encoded.append("?")
        await message.edit(f"📡 **Morse:**\n`{' '.join(encoded)}`")

    register_command("Text", "morse_e", "Morse code encode", [])

    @app.on_message(filters.command("morse_d", prefixes=".") & filters.me)
    async def morse_d_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.morse_d <morse>`")
            return
        parts = text.strip().split()
        decoded = []
        for p in parts:
            if p == "/":
                decoded.append(" ")
            elif p in _MORSE_REV:
                decoded.append(_MORSE_REV[p])
            else:
                decoded.append("?")
        await message.edit(f"📡 **Decoded:**\n`{''.join(decoded)}`")

    register_command("Text", "morse_d", "Morse code decode", [])

    @app.on_message(filters.command("ascii_e", prefixes=".") & filters.me)
    async def ascii_e_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.ascii_e <text>`")
            return
        encoded = " ".join(str(ord(c)) for c in text)
        await message.edit(f"🔒 **ASCII:**\n`{encoded}`")

    register_command("Text", "ascii_e", "Encode text to ASCII codes", [])

    @app.on_message(filters.command("ascii_d", prefixes=".") & filters.me)
    async def ascii_d_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.ascii_d <codes>`")
            return
        try:
            codes = text.strip().split()
            decoded = "".join(chr(int(c)) for c in codes)
            await message.edit(f"🔓 **Decoded:**\n`{decoded}`")
        except (ValueError, OverflowError):
            await message.edit("❌ Invalid ASCII codes.")

    register_command("Text", "ascii_d", "Decode ASCII codes to text", [])

    @app.on_message(filters.command("url_e", prefixes=".") & filters.me)
    async def url_e_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.url_e <text>`")
            return
        await message.edit(f"🔒 **URL Encoded:**\n`{urllib.parse.quote(text)}`")

    register_command("Text", "url_e", "URL encode", [])

    @app.on_message(filters.command("url_d", prefixes=".") & filters.me)
    async def url_d_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.url_d <encoded>`")
            return
        await message.edit(f"🔓 **URL Decoded:**\n`{urllib.parse.unquote(text)}`")

    register_command("Text", "url_d", "URL decode", [])

    @app.on_message(filters.command("html_e", prefixes=".") & filters.me)
    async def html_e_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.html_e <text>`")
            return
        await message.edit(f"🔒 **HTML Encoded:**\n`{html.escape(text)}`")

    register_command("Text", "html_e", "HTML encode", [])

    @app.on_message(filters.command("html_d", prefixes=".") & filters.me)
    async def html_d_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.html_d <encoded>`")
            return
        await message.edit(f"🔓 **HTML Decoded:**\n`{html.unescape(text)}`")

    register_command("Text", "html_d", "HTML decode", [])

    @app.on_message(filters.command("reverse_cipher", prefixes=".") & filters.me)
    async def reverse_cipher_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.reverse_cipher <text>`")
            return
        await message.edit(f"🔄 **Reverse Cipher:**\n`{text[::-1]}`")

    register_command("Text", "reverse_cipher", "Reverse text as cipher", [])

    @app.on_message(filters.command("railfence_e", prefixes=".") & filters.me)
    async def railfence_e_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.railfence_e <rails> <text>`")
            return
        try:
            rails = int(args[1])
            text = args[2]
            if rails < 2:
                await message.edit("❌ Need at least 2 rails.")
                return
            fence = [[] for _ in range(rails)]
            rail = 0
            direction = 1
            for ch in text:
                fence[rail].append(ch)
                if rail == 0:
                    direction = 1
                elif rail == rails - 1:
                    direction = -1
                rail += direction
            result = "".join("".join(r) for r in fence)
            await message.edit(f"🔒 **Rail Fence ({rails} rails):**\n`{result}`")
        except ValueError:
            await message.edit("❌ Rails must be a number.")

    register_command("Text", "railfence_e", "Rail fence cipher encrypt", [])

    @app.on_message(filters.command("railfence_d", prefixes=".") & filters.me)
    async def railfence_d_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.railfence_d <rails> <text>`")
            return
        try:
            rails = int(args[1])
            text = args[2]
            if rails < 2:
                await message.edit("❌ Need at least 2 rails.")
                return
            n = len(text)
            pattern = list(range(rails)) + list(range(rails - 2, 0, -1))
            indices = sorted(range(n), key=lambda i: pattern[i % len(pattern)])
            result = [""] * n
            for i, c in zip(indices, text):
                result[i] = c
            await message.edit(f"🔓 **Rail Fence Decoded:**\n`{''.join(result)}`")
        except ValueError:
            await message.edit("❌ Rails must be a number.")

    register_command("Text", "railfence_d", "Rail fence cipher decrypt", [])

    @app.on_message(filters.command("xor_e", prefixes=".") & filters.me)
    async def xor_e_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.xor_e <key> <text>`")
            return
        key = args[1]
        text = args[2]
        result = []
        for i, c in enumerate(text):
            result.append(chr(ord(c) ^ ord(key[i % len(key)])))
        encoded = "".join(result).encode().hex()
        await message.edit(f"🔒 **XOR (key={key}):**\n`{encoded}`")

    register_command("Text", "xor_e", "XOR cipher encrypt", [])

    @app.on_message(filters.command("xor_d", prefixes=".") & filters.me)
    async def xor_d_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.xor_d <key> <hex>`")
            return
        key = args[1]
        try:
            data = bytes.fromhex(args[2].strip()).decode()
            result = []
            for i, c in enumerate(data):
                result.append(chr(ord(c) ^ ord(key[i % len(key)])))
            await message.edit(f"🔓 **XOR Decoded:**\n`{''.join(result)}`")
        except ValueError:
            await message.edit("❌ Invalid hex input.")

    register_command("Text", "xor_d", "XOR cipher decrypt", [])

    # ═══════════════════════════════════════════════════════════════
    #  ANALYSIS (15 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("wordcount", prefixes=".") & filters.me)
    async def wordcount_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.wordcount <text>`")
            return
        count = len(text.split())
        await message.edit(f"📊 **Word Count:** `{count}`")

    register_command("Text", "wordcount", "Count words in text", [])

    @app.on_message(filters.command("charcount", prefixes=".") & filters.me)
    async def charcount_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.charcount <text>`")
            return
        await message.edit(f"📊 **Character Count:** `{len(text)}` (with spaces), `{len(text.replace(' ', ''))}` (without)")

    register_command("Text", "charcount", "Count characters in text", [])

    @app.on_message(filters.command("linecount", prefixes=".") & filters.me)
    async def linecount_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.linecount <text>`")
            return
        count = len(text.splitlines()) or 1
        await message.edit(f"📊 **Line Count:** `{count}`")

    register_command("Text", "linecount", "Count lines in text", [])

    @app.on_message(filters.command("sentencecount", prefixes=".") & filters.me)
    async def sentencecount_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.sentencecount <text>`")
            return
        count = len(re.split(r'[.!?]+', text))
        if text.rstrip()[-1:] not in '.!?':
            count -= 1
        count = max(count, 1)
        await message.edit(f"📊 **Sentence Count:** `{count}`")

    register_command("Text", "sentencecount", "Count sentences in text", [])

    @app.on_message(filters.command("readability", prefixes=".") & filters.me)
    async def readability_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.readability <text>`")
            return
        words = text.split()
        word_count = len(words)
        if word_count == 0:
            await message.edit("❌ No words found.")
            return
        sentences = max(len(re.split(r'[.!?]+', text)), 1)
        syllables = sum(max(1, len(re.findall(r'[aeiouyAEIOUY]+', w))) for w in words)
        if sentences == 0:
            sentences = 1
        flesch = 206.835 - 1.015 * (word_count / sentences) - 84.6 * (syllables / word_count)
        await message.edit(f"📊 **Readability (Flesch):** `{flesch:.1f}`\n📖 {'Easy' if flesch > 60 else 'Moderate' if flesch > 30 else 'Difficult'}")

    register_command("Text", "readability", "Flesch readability score", [])

    @app.on_message(filters.command("avg_word_len", prefixes=".") & filters.me)
    async def avg_word_len_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.avg_word_len <text>`")
            return
        words = text.split()
        if not words:
            await message.edit("❌ No words found.")
            return
        avg = sum(len(w) for w in words) / len(words)
        await message.edit(f"📊 **Average Word Length:** `{avg:.2f}` chars")

    register_command("Text", "avg_word_len", "Average word length", [])

    @app.on_message(filters.command("most_common", prefixes=".") & filters.me)
    async def most_common_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.most_common <text>`")
            return
        words = text.lower().split()
        if not words:
            await message.edit("❌ No words found.")
            return
        counter = collections.Counter(words)
        top = counter.most_common(5)
        result = "\n".join(f"  • `{w}`: {c}" for w, c in top)
        await message.edit(f"📊 **Most Common Words:**\n{result}")

    register_command("Text", "most_common", "Most common words", [])

    @app.on_message(filters.command("least_common", prefixes=".") & filters.me)
    async def least_common_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.least_common <text>`")
            return
        words = text.lower().split()
        if not words:
            await message.edit("❌ No words found.")
            return
        counter = collections.Counter(words)
        bottom = counter.most_common()[:-6:-1]
        result = "\n".join(f"  • `{w}`: {c}" for w, c in bottom)
        await message.edit(f"📊 **Least Common Words:**\n{result}")

    register_command("Text", "least_common", "Least common words", [])

    @app.on_message(filters.command("vowelcount", prefixes=".") & filters.me)
    async def vowelcount_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.vowelcount <text>`")
            return
        count = sum(1 for c in text.lower() if c in "aeiou")
        await message.edit(f"📊 **Vowel Count:** `{count}`")

    register_command("Text", "vowelcount", "Count vowels in text", [])

    @app.on_message(filters.command("consonantcount", prefixes=".") & filters.me)
    async def consonantcount_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.consonantcount <text>`")
            return
        count = sum(1 for c in text.lower() if c.isalpha() and c not in "aeiou")
        await message.edit(f"📊 **Consonant Count:** `{count}`")

    register_command("Text", "consonantcount", "Count consonants in text", [])

    @app.on_message(filters.command("digitcount", prefixes=".") & filters.me)
    async def digitcount_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.digitcount <text>`")
            return
        count = sum(1 for c in text if c.isdigit())
        await message.edit(f"📊 **Digit Count:** `{count}`")

    register_command("Text", "digitcount", "Count digits in text", [])

    @app.on_message(filters.command("specialcount", prefixes=".") & filters.me)
    async def specialcount_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.specialcount <text>`")
            return
        count = sum(1 for c in text if not c.isalnum() and not c.isspace())
        await message.edit(f"📊 **Special Char Count:** `{count}`")

    register_command("Text", "specialcount", "Count special characters", [])

    @app.on_message(filters.command("palindrome_check", prefixes=".") & filters.me)
    async def palindrome_check_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.palindrome_check <text>`")
            return
        cleaned = "".join(c.lower() for c in text if c.isalnum())
        is_pal = cleaned == cleaned[::-1]
        emoji = "✅" if is_pal else "❌"
        await message.edit(f"{emoji} **Palindrome:** `{is_pal}`")

    register_command("Text", "palindrome_check", "Check if text is a palindrome", [])

    @app.on_message(filters.command("anagram_check", prefixes=".") & filters.me)
    async def anagram_check_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.anagram_check <word1> <word2>`")
            return
        w1 = "".join(c.lower() for c in args[1] if c.isalnum())
        w2 = "".join(c.lower() for c in args[2] if c.isalnum())
        is_ana = sorted(w1) == sorted(w2)
        emoji = "✅" if is_ana else "❌"
        await message.edit(f"{emoji} **Anagram:** `{is_ana}`")

    register_command("Text", "anagram_check", "Check if two words are anagrams", [])

    @app.on_message(filters.command("pangram_check", prefixes=".") & filters.me)
    async def pangram_check_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.pangram_check <text>`")
            return
        letters = set(c.lower() for c in text if c.isalpha())
        is_pan = len(letters) == 26
        emoji = "✅" if is_pan else "❌"
        missing = set(string.ascii_lowercase) - letters
        result = f"{emoji} **Pangram:** `{is_pan}`"
        if not is_pan and missing:
            result += f"\n📝 **Missing:** `{''.join(sorted(missing))}`"
        await message.edit(result)

    register_command("Text", "pangram_check", "Check if text is a pangram", [])

    # ═══════════════════════════════════════════════════════════════
    #  MANIPULATION (22 commands)
    # ═══════════════════════════════════════════════════════════════

    @app.on_message(filters.command("repeat", prefixes=".") & filters.me)
    async def repeat_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.repeat <count> <text>`")
            return
        try:
            count = int(args[1])
            if count < 1 or count > 50:
                await message.edit("❌ Count must be 1-50.")
                return
        except ValueError:
            await message.edit("❌ Count must be a number.")
            return
        result = (args[2] + " ") * count
        await message.edit(result.strip())

    register_command("Text", "repeat", "Repeat text N times", [])

    @app.on_message(filters.command("remove_spaces", prefixes=".") & filters.me)
    async def remove_spaces_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.remove_spaces <text>`")
            return
        await message.edit(f"✂️ **No spaces:**\n{text.replace(' ', '')}")

    register_command("Text", "remove_spaces", "Remove all spaces", [])

    @app.on_message(filters.command("remove_digits", prefixes=".") & filters.me)
    async def remove_digits_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.remove_digits <text>`")
            return
        await message.edit(f"✂️ **No digits:**\n{''.join(c for c in text if not c.isdigit())}")

    register_command("Text", "remove_digits", "Remove all digits", [])

    @app.on_message(filters.command("remove_special", prefixes=".") & filters.me)
    async def remove_special_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.remove_special <text>`")
            return
        await message.edit(f"✂️ **No special:**\n{''.join(c for c in text if c.isalnum() or c.isspace())}")

    register_command("Text", "remove_special", "Remove special characters", [])

    @app.on_message(filters.command("remove_vowels", prefixes=".") & filters.me)
    async def remove_vowels_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.remove_vowels <text>`")
            return
        await message.edit(f"✂️ **No vowels:**\n{''.join(c for c in text if c.lower() not in 'aeiou' or not c.isalpha())}")

    register_command("Text", "remove_vowels", "Remove all vowels", [])

    @app.on_message(filters.command("remove_consonants", prefixes=".") & filters.me)
    async def remove_consonants_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.remove_consonants <text>`")
            return
        await message.edit(f"✂️ **No consonants:**\n{''.join(c for c in text if c.lower() in 'aeiou' or not c.isalpha())}")

    register_command("Text", "remove_consonants", "Remove all consonants", [])

    @app.on_message(filters.command("only_alpha", prefixes=".") & filters.me)
    async def only_alpha_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.only_alpha <text>`")
            return
        await message.edit(f"✂️ **Alpha only:**\n{''.join(c for c in text if c.isalpha() or c.isspace())}")

    register_command("Text", "only_alpha", "Keep only alphabetic chars", [])

    @app.on_message(filters.command("only_digits", prefixes=".") & filters.me)
    async def only_digits_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.only_digits <text>`")
            return
        await message.edit(f"✂️ **Digits only:**\n{''.join(c for c in text if c.isdigit())}")

    register_command("Text", "only_digits", "Keep only digits", [])

    @app.on_message(filters.command("only_upper", prefixes=".") & filters.me)
    async def only_upper_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.only_upper <text>`")
            return
        await message.edit(f"✂️ **Uppercase only:**\n{''.join(c for c in text if c.isupper() or c.isspace())}")

    register_command("Text", "only_upper", "Keep only uppercase chars", [])

    @app.on_message(filters.command("only_lower", prefixes=".") & filters.me)
    async def only_lower_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.only_lower <text>`")
            return
        await message.edit(f"✂️ **Lowercase only:**\n{''.join(c for c in text if c.islower() or c.isspace())}")

    register_command("Text", "only_lower", "Keep only lowercase chars", [])

    @app.on_message(filters.command("replace", prefixes=".") & filters.me)
    async def replace_cmd(client, message):
        args = message.text.split(None, 3)
        if len(args) < 4:
            await message.edit("❌ **Usage:** `.replace <old> <new> <text>`")
            return
        old, new, text = args[1], args[2], args[3]
        await message.edit(f"🔄 **Replaced:**\n{text.replace(old, new)}")

    register_command("Text", "replace", "Replace text", [])

    @app.on_message(filters.command("insert", prefixes=".") & filters.me)
    async def insert_cmd(client, message):
        args = message.text.split(None, 3)
        if len(args) < 4:
            await message.edit("❌ **Usage:** `.insert <position> <text_to_insert> <text>`")
            return
        try:
            pos = int(args[1])
            insert_text = args[2]
            text = args[3]
            result = text[:pos] + insert_text + text[pos:]
            await message.edit(f"✏️ **Inserted:**\n{result}")
        except (ValueError, IndexError):
            await message.edit("❌ Invalid position.")

    register_command("Text", "insert", "Insert text at position", [])

    @app.on_message(filters.command("pad", prefixes=".") & filters.me)
    async def pad_cmd(client, message):
        args = message.text.split(None, 3)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.pad <width> <text>` [char]")
            return
        try:
            width = int(args[1])
            text = args[2]
            char = args[3] if len(args) > 3 else " "
            result = text.center(width, char[0] if char else " ")
            await message.edit(f"📏 **Padded:**\n`{result}`")
        except ValueError:
            await message.edit("❌ Width must be a number.")

    register_command("Text", "pad", "Pad text to width", [])

    @app.on_message(filters.command("center", prefixes=".") & filters.me)
    async def center_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.center <width> <text>`")
            return
        try:
            width = int(args[1])
            text = args[2]
            await message.edit(f"📐 **Centered:**\n`{text.center(width)}`")
        except ValueError:
            await message.edit("❌ Width must be a number.")

    register_command("Text", "center", "Center text in width", [])

    @app.on_message(filters.command("left_justify", prefixes=".") & filters.me)
    async def left_justify_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.left_justify <width> <text>`")
            return
        try:
            width = int(args[1])
            text = args[2]
            await message.edit(f"📐 **Left Justified:**\n`{text.ljust(width)}`")
        except ValueError:
            await message.edit("❌ Width must be a number.")

    register_command("Text", "left_justify", "Left justify text", [])

    @app.on_message(filters.command("right_justify", prefixes=".") & filters.me)
    async def right_justify_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.right_justify <width> <text>`")
            return
        try:
            width = int(args[1])
            text = args[2]
            await message.edit(f"📐 **Right Justified:**\n`{text.rjust(width)}`")
        except ValueError:
            await message.edit("❌ Width must be a number.")

    register_command("Text", "right_justify", "Right justify text", [])

    @app.on_message(filters.command("wrap", prefixes=".") & filters.me)
    async def wrap_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.wrap <width> <text>`")
            return
        try:
            width = int(args[1])
            text = args[2]
            result = textwrap.fill(text, width=width)
            await message.edit(f"📝 **Wrapped:**\n```\n{result}\n```")
        except ValueError:
            await message.edit("❌ Width must be a number.")

    register_command("Text", "wrap", "Wrap text to width", [])

    @app.on_message(filters.command("truncate", prefixes=".") & filters.me)
    async def truncate_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.edit("❌ **Usage:** `.truncate <length> <text>`")
            return
        try:
            length = int(args[1])
            text = args[2]
            result = text[:length] + ("..." if len(text) > length else "")
            await message.edit(f"✂️ **Truncated:**\n{result}")
        except ValueError:
            await message.edit("❌ Length must be a number.")

    register_command("Text", "truncate", "Truncate text to length", [])

    @app.on_message(filters.command("indent", prefixes=".") & filters.me)
    async def indent_cmd(client, message):
        args = message.text.split(None, 2)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.indent <text>` [prefix]")
            return
        text = args[1]
        prefix = args[2] if len(args) > 2 else "    "
        result = textwrap.indent(text, prefix)
        await message.edit(f"📝 **Indented:**\n```\n{result}\n```")

    register_command("Text", "indent", "Indent text lines", [])

    @app.on_message(filters.command("dedent", prefixes=".") & filters.me)
    async def dedent_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.dedent <text>`")
            return
        result = textwrap.dedent(text)
        await message.edit(f"📝 **Dedented:**\n```\n{result}\n```")

    register_command("Text", "dedent", "Remove common leading whitespace", [])

    @app.on_message(filters.command("bulletize", prefixes=".") & filters.me)
    async def bulletize_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.bulletize <text>`")
            return
        lines = text.splitlines()
        result = "\n".join(f"• {line.strip()}" for line in lines if line.strip())
        await message.edit(result)

    register_command("Text", "bulletize", "Add bullet points to lines", [])

    @app.on_message(filters.command("numberize", prefixes=".") & filters.me)
    async def numberize_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.numberize <text>`")
            return
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        result = "\n".join(f"{i+1}. {line}" for i, line in enumerate(lines))
        await message.edit(result)

    register_command("Text", "numberize", "Add number list to lines", [])

    # ═══════════════════════════════════════════════════════════════
    #  OTHER (13 commands)
    # ═══════════════════════════════════════════════════════════════

    _LOREM_WORDS = [
        "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing",
        "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore",
        "et", "dolore", "magna", "aliqua", "enim", "ad", "minim", "veniam",
        "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi",
        "aliquip", "ex", "ea", "commodo", "consequat", "duis", "aute", "irure",
    ]

    @app.on_message(filters.command("lorem", prefixes=".") & filters.me)
    async def lorem_cmd(client, message):
        args = message.text.split(None, 1)
        count = int(args[1]) if len(args) > 1 else 20
        words = [random.choice(_LOREM_WORDS) for _ in range(count)]
        result = " ".join(words)
        result = result.capitalize() + "."
        await message.edit(f"📜 **Lorem Ipsum:**\n{result}")

    register_command("Text", "lorem", "Generate lorem ipsum text", [])

    @app.on_message(filters.command("randomword", prefixes=".") & filters.me)
    async def randomword_cmd(client, message):
        word = random.choice(_LOREM_WORDS)
        await message.edit(f"🎲 **Random Word:** `{word}`")

    register_command("Text", "randomword", "Get a random word", [])

    @app.on_message(filters.command("randomsentence", prefixes=".") & filters.me)
    async def randomsentence_cmd(client, message):
        length = random.randint(5, 12)
        words = [random.choice(_LOREM_WORDS) for _ in range(length)]
        result = " ".join(words).capitalize() + "."
        await message.edit(f"🎲 **Random Sentence:**\n{result}")

    register_command("Text", "randomsentence", "Generate a random sentence", [])

    @app.on_message(filters.command("randomparagraph", prefixes=".") & filters.me)
    async def randomparagraph_cmd(client, message):
        sentences = random.randint(3, 6)
        parts = []
        for _ in range(sentences):
            length = random.randint(5, 12)
            words = [random.choice(_LOREM_WORDS) for _ in range(length)]
            parts.append(" ".join(words).capitalize() + ".")
        await message.edit(f"🎲 **Random Paragraph:**\n{' '.join(parts)}")

    register_command("Text", "randomparagraph", "Generate a random paragraph", [])

    @app.on_message(filters.command("haiku", prefixes=".") & filters.me)
    async def haiku_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.haiku <topic>`")
            return
        topic = args[1]
        haiku_text = (
            f"{topic} whispers soft\n"
            f"Gentle breeze through the tall trees\n"
            f"Peace in every breath"
        )
        await message.edit(f"🎋 **Haiku:**\n{haiku_text}")

    register_command("Text", "haiku", "Generate a haiku about a topic", [])

    @app.on_message(filters.command("limerick", prefixes=".") & filters.me)
    async def limerick_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.limerick <name>`")
            return
        name = args[1]
        limerick = (
            f"There once was a person named {name},\n"
            f"Whose texting was never the same,\n"
            f"They typed with such flair,\n"
            f"That folks would just stare,\n"
            f"And marvel at linguistic game."
        )
        await message.edit(f"🎭 **Limerick:**\n{limerick}")

    register_command("Text", "limerick", "Generate a limerick with a name", [])

    @app.on_message(filters.command("acrostic", prefixes=".") & filters.me)
    async def acrostic_cmd(client, message):
        args = message.text.split(None, 1)
        if len(args) < 2:
            await message.edit("❌ **Usage:** `.acrostic <word>`")
            return
        word = args[1].upper()
        fill_words = _LOREM_WORDS
        lines = []
        for ch in word:
            if ch.isalpha():
                w = random.choice([w for w in fill_words if w.startswith(ch.lower())] or fill_words)
                lines.append(f"{ch} - {w.capitalize()}")
            else:
                lines.append(f"{ch}")
        await message.edit(f"📝 **Acrostic:**\n" + "\n".join(lines))

    register_command("Text", "acrostic", "Generate an acrostic poem", [])

    @app.on_message(filters.command("anagram", prefixes=".") & filters.me)
    async def anagram_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.anagram <text>`")
            return
        chars = list(text)
        random.shuffle(chars)
        await message.edit(f"🔄 **Anagram:**\n{''.join(chars)}")

    register_command("Text", "anagram", "Generate an anagram", [])

    @app.on_message(filters.command("scramble", prefixes=".") & filters.me)
    async def scramble_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.scramble <text>`")
            return
        words = text.split()
        result = []
        for w in words:
            if len(w) > 3:
                middle = list(w[1:-1])
                random.shuffle(middle)
                result.append(w[0] + "".join(middle) + w[-1])
            else:
                result.append(w)
        await message.edit(f"🔀 **Scrambled:**\n{' '.join(result)}")

    register_command("Text", "scramble", "Scramble middle letters of words", [])

    @app.on_message(filters.command("piglatin", prefixes=".") & filters.me)
    async def piglatin_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.piglatin <text>`")
            return
        vowels = "aeiouAEIOU"
        result = []
        for word in text.split():
            if word[0] in vowels:
                result.append(word + "yay")
            else:
                i = 0
                while i < len(word) and word[i] not in vowels:
                    i += 1
                result.append(word[i:] + word[:i] + "ay")
        await message.edit(f"🐷 **Pig Latin:**\n{' '.join(result)}")

    register_command("Text", "piglatin", "Convert to Pig Latin", [])

    @app.on_message(filters.command("oppish", prefixes=".") & filters.me)
    async def oppish_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.oppish <text>`")
            return
        vowels = "aeiouAEIOU"
        result = []
        for word in text.split():
            new = ""
            for c in word:
                new += c
                if c.lower() in vowels:
                    new += "op"
            result.append(new)
        await message.edit(f"🗣 **Oppish:**\n{' '.join(result)}")

    register_command("Text", "oppish", "Convert to Oppish", [])

    @app.on_message(filters.command("gibberish", prefixes=".") & filters.me)
    async def gibberish_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.gibberish <text>`")
            return
        result = []
        for word in text.split():
            if len(word) > 2:
                chars = list(word)
                for i in range(1, len(chars) - 1):
                    if random.random() > 0.5:
                        j = random.randint(1, len(chars) - 2)
                        chars[i], chars[j] = chars[j], chars[i]
                result.append("".join(chars))
            else:
                result.append(word)
        await message.edit(f"🤪 **Gibberish:**\n{' '.join(result)}")

    register_command("Text", "gibberish", "Make text gibberish", [])

    @app.on_message(filters.command("leet", prefixes=".") & filters.me)
    async def leet_cmd(client, message):
        text = _get_text(message)
        if not text:
            await message.edit("❌ **Usage:** `.leet <text>`")
            return
        _leet_map = {
            'a': '4', 'b': '8', 'e': '3', 'g': '9', 'i': '1', 'l': '1',
            'o': '0', 's': '5', 't': '7', 'z': '2',
            'A': '4', 'B': '8', 'E': '3', 'G': '9', 'I': '1', 'L': '1',
            'O': '0', 'S': '5', 'T': '7', 'Z': '2',
        }
        result = "".join(_leet_map.get(c, c) for c in text)
        await message.edit(f"💻 **L33T:**\n{result}")

    register_command("Text", "leet", "Convert to leet speak", [])
