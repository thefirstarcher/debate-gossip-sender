# writebot

Userbot that sends anonymous messages to `@plitkarnya_debate_bot` on a loop,
each one a unique look-alike variant so the bot's duplicate limit never trips.

## Setup (once)

```sh
python -m venv .venv && .venv/bin/pip install telethon
# fill API_ID / API_HASH in .env  (from https://my.telegram.org)
.venv/bin/python probe.py /start      # first run: interactive login (phone + code)
```

## Run the loop

```sh
.venv/bin/python userbot.py                       # nonstop
MAX=10 .venv/bin/python userbot.py                # stop after 10
TEXT="Інший текст" .venv/bin/python userbot.py    # different message
DELAY=0.5 .venv/bin/python userbot.py             # faster (near TG rate limit)
```

Stop: `Ctrl-C`, or `pkill -f "python userbot.py"`.

## Config (.env)

| var | default | meaning |
|-----|---------|---------|
| `TEXT` | Паша підсуди | message to send |
| `DELAY` | 1.5 | seconds between messages |
| `CONFIRM` | 3 | max wait for bot reply before giving up on a click |
| `MAX` | 0 | stop after N sends (0 = forever) |
