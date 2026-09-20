"""
KyrenUB - Session String Generator
====================================
Interactive CLI script to generate a Pyrogram string session.
Usage: python generate_session.py
"""

import patches  # noqa: F401

import sys
import asyncio
from pyrogram import Client


async def generate():
    print("=" * 50)
    print("   KyrenUB - Session String Generator")
    print("=" * 50)
    print()
    print("Get your API credentials from: https://my.telegram.org/apps")
    print()

    api_id = input("Enter your API_ID: ").strip()
    api_hash = input("Enter your API_HASH: ").strip()

    if not api_id or not api_hash:
        print("[ERROR] API_ID and API_HASH are required!")
        sys.exit(1)

    try:
        api_id = int(api_id)
    except ValueError:
        print("[ERROR] API_ID must be a number!")
        sys.exit(1)

    print()
    print("Starting Pyrogram client...")
    print("You will receive a login code in your Telegram app.")
    print()

    client = Client(
        name=":memory:",
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True,
    )

    await client.start()
    session_string = await client.export_session_string()

    me = await client.get_me()
    print()
    print("=" * 50)
    print("   SESSION GENERATED SUCCESSFULLY!")
    print("=" * 50)
    print()
    print(f"Logged in as: {me.first_name} (@{me.username or 'N/A'}) [ID: {me.id}]")
    print()
    print("Your STRING_SESSION (save this securely!):")
    print()
    print(session_string)
    print()
    print("Keep this session string secret!")
    print("=" * 50)

    await client.stop()


if __name__ == "__main__":
    asyncio.run(generate())
