# writebot

Userbot that sends anonymous messages to `@plitkarnya_debate_bot` on a loop,
each one a unique look-alike variant so the bot's duplicate limit never trips.

## Responsible / authorized use

This tool automates a Telegram *user* account and is built to bypass a bot's
rate-limit and duplicate-message checks. That makes it easy to misuse. Before
running it:

- **Only send to channels/bots you own or are explicitly authorized to test.**
  Use it against your own bot, a test channel, or with the operator's written
  permission — not to flood, brigade, or evade moderation on someone else's
  service.
- **No harassment, spam, or abuse.** Do not use it to target a person or group,
  post slurs or threats, or drown out other users. Automated flooding of a
  channel you don't control is abuse regardless of the message content.
- **You are responsible under Telegram's ToS.** Automating a user account to
  spam or dodge anti-abuse limits can get the account **banned**, and may break
  local law. This repo is provided for learning about Telegram automation,
  homoglyph/Unicode handling, and rate-limit behaviour — not for causing harm.

The author does not endorse or take responsibility for misuse. If in doubt
about whether a use is authorized, it isn't — get explicit permission first.

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
