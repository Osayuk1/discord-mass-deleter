# Discord Message Deleter (`disdelete.py`)

A simple Python script to delete a user's messages from a Discord server within a date range.

## 🔧 Requirements

- Python 3
- `aiohttp`
- `python-dateutil`

### Install:
```bash
pip install -r requirements.txt
```

## 🚀 How to Use

1. Clone the repository:
```bash
git clone https://github.com/your-username/discord-delete-tool
cd discord-delete-tool
```

2. Run the script:
```bash
python disdelete.py
```

3. You will be prompted to enter:
- Your Discord bot token
- The guild (server) ID
- The user ID to delete messages from
- Start and end dates in the format `YYYY-MM-DD`

### Example:
```
Token:      your-bot-token-here
Guild ID:   123456789012345678
User ID:    987654321098765432
Start date: 2025-05-01
End date:   2025-05-10
```

## 📁 Output

All deleted message IDs and contents will be logged to `deleted_messages_log.json`.

## ⚠️ Disclaimer

- This tool is for **educational and personal** use only.
- You must have permission to manage messages in the server.
- Use responsibly — improper use may violate Discord's Terms of Service.
