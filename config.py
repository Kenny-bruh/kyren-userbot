"""
KyrenUB - Configuration Handler
================================
Loads environment variables via python-dotenv.
NO external API keys required.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Central configuration for KyrenUB."""

    API_ID: int = int(os.getenv("API_ID", "0") or "0")
    API_HASH: str = os.getenv("API_HASH", "")
    STRING_SESSION: str = os.getenv("STRING_SESSION", "")

    PREFIX: str = os.getenv("PREFIX", ".")
    LOG_GROUP: int = int(os.getenv("LOG_GROUP", "0") or "0")

    BOT_NAME: str = "ToxicUB"
    BOT_VERSION: str = "2.0.0"
    BOT_REPO: str = "https://github.com/SegsyToxic-95/ToxicUB"
    OWNER_USERNAME: str = os.getenv("OWNER_USERNAME", "@SegsyToxic95")
    SUDO_USERS: list = [
        int(x) for x in (os.getenv("SUDO_USERS", "") or "").split() if x.strip().isdigit()
    ]

    PORT: int = int(os.getenv("PORT", "8080"))

    SPAM_LIMIT: int = 50
    FLOOD_LIMIT: int = 100
    SPAM_DELAY: float = 0.3

    @classmethod
    def validate(cls) -> bool:
        if cls.API_ID == 0 or not cls.API_HASH or not cls.STRING_SESSION:
            return False
        return True

    @classmethod
    def missing_vars(cls) -> list:
        missing = []
        if cls.API_ID == 0:
            missing.append("API_ID")
        if not cls.API_HASH:
            missing.append("API_HASH")
        if not cls.STRING_SESSION:
            missing.append("STRING_SESSION")
        return missing
