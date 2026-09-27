#!/usr/bin/env python3
"""Userbot that keeps feeding @plitkarnya_debate_bot anonymous messages.

Loop per iteration: send TEXT -> bot answers "Повідомлення надіслано"
-> click "Надіслати повідомлення ще раз" -> bot waits for the next text.

    .venv/bin/python userbot.py        # forever
    MAX=3 .venv/bin/python userbot.py  # bounded run

Config in .env: API_ID, API_HASH, BOT, TEXT, DELAY, MAX.
"""
import asyncio
import os
import random

from telethon import TelegramClient
from telethon.errors import FloodWaitError

from homoglyphs import unique

# ponytail: .env loader, 1 line, no python-dotenv
for _l in open(".env").read().splitlines():
    if "=" in _l:
        _k, _v = _l.split("=", 1)
        os.environ.setdefault(_k, _v)

BOT = os.environ.get("BOT", "@plitkarnya_debate_bot")
TEXT = os.environ.get("TEXT", "Паша підсуди")
DELAY = float(os.environ.get("DELAY", 4))  # seconds between messages
CONFIRM = float(os.environ.get("CONFIRM", 1.2))  # wait for bot to confirm before click
MAX = int(os.environ.get("MAX", 0))  # 0 = no limit
AGAIN = "Надіслати повідомлення ще раз"
START = "Написати повідомлення"

client = TelegramClient("userbot", int(os.environ["API_ID"]), os.environ["API_HASH"])


async def click(bot, label, timeout=CONFIRM):
    """Poll for `label` and click it the instant it appears. False on timeout.

    ponytail: 0.3s poll beats a fixed sleep — acts as soon as the bot replies.
    """
    deadline = asyncio.get_event_loop().time() + timeout
    while asyncio.get_event_loop().time() < deadline:
        async for msg in client.iter_messages(bot, limit=3):
            if any(b.text == label for row in msg.buttons or [] for b in row):
                await msg.click(text=label)
                return True
        await asyncio.sleep(0.3)
    return False


async def main():
    bot = await client.get_entity(BOT)
    seen = set()
    sent = 0
    while not MAX or sent < MAX:
        try:
            await client.send_message(bot, unique(TEXT, seen))
            sent += 1
            if not await click(bot, AGAIN):
                # lost the flow (restart, error) -> walk in from /start
                await client.send_message(bot, "/start")
                await click(bot, START)
        except FloodWaitError as e:
            print(f"flood wait {e.seconds}s", flush=True)
            await asyncio.sleep(e.seconds + 5)
            continue
        print(f"sent {sent}", flush=True)
        # ponytail: fixed delay + jitter, far under TG's ~1 msg/s per chat.
        # Adaptive pacing only if a FloodWait ever actually shows up.
        await asyncio.sleep(DELAY + random.uniform(0, DELAY / 2))


with client:
    client.loop.run_until_complete(main())
