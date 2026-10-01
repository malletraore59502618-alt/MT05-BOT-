# MT05 BOT

Telegram bot for football match analysis and exact-score math.

## Setup

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set your bot token:

```bash
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN_HERE"
```

3. Run the bot:

```bash
python3 bot.py
```

## Usage

Send a match like:

```text
Real vs Barca
```

Then send the home, draw and away odds one by one.
The bot calculates the implied probability and suggests a short exact-score list.
