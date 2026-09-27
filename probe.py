#!/usr/bin/env python3
"""Manual probe: send a command (or click a button) and dump what the bot says.

    python probe.py                 # just read last 5 messages
    python probe.py /start          # send text, then read
    python probe.py -c "Button txt" # click button by text (or by index: -c 0)

Same session/env as userbot.py. First run is interactive (phone + code).
"""
import asyncio
import os
import sys

from telethon import TelegramClient

# ponytail: .env loader, 1 line, no python-dotenv
for _l in open(".env").read().splitlines():
    if "=" in _l:
        _k, _v = _l.split("=", 1)
        os.environ.setdefault(_k, _v)

BOT = os.environ.get("BOT", "@plitkarnya_debate_channel")
client = TelegramClient("userbot", int(os.environ["API_ID"]), os.environ["API_HASH"])


async def main(arg, click):
    bot = await client.get_entity(BOT)
    if click is not None:
        msg = (await client.get_messages(bot, limit=1))[0]
        await msg.click(**({"i": int(click)} if click.isdigit() else {"text": click}))
    elif arg:
        await client.send_message(bot, arg)
    await asyncio.sleep(4)
    for msg in reversed(await client.get_messages(bot, limit=5)):
        who = "me" if msg.out else "bot"
        print(f"--- {who} {msg.date:%H:%M:%S}\n{msg.text}")
        for row in msg.buttons or []:
            print("  [" + "] [".join(b.text for b in row) + "]")


args = sys.argv[1:]
click = args[args.index("-c") + 1] if "-c" in args else None
text = args[0] if args and args[0] != "-c" else None
with client:
    client.loop.run_until_complete(main(text, click))
