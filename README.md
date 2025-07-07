# Discord Message Deleter (`disdelete.py`)

A simple Python script to delete a user's messages from a Discord server within a date range — using a user token.

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
git clone https://github.com/Osayuk1/discord-mass-deleter
cd discord-mass-deleter
```

2. Run the script:
```bash
python disdelete.py
```

3. You will be prompted to enter:
- Your **Discord user token**
- The **Guild ID** (server)
- The **User ID** whose messages you want to delete
- A **Start and End date** in format `YYYY-MM-DD`

### Example:
```
Token:      your-user-token-here
Guild ID:   123456789012345678
User ID:    987654321098765432
Start date: 2025-07-01
End date:   2025-07-06
```

## 📁 Output

All deleted message IDs and contents will be logged to:
```
deleted_messages_log.json
```

---

## ⚠️ Warnings & Disclaimer

> By using this tool, you agree that:
- You are responsible for your own actions.
- This tool uses a **user token**, not a bot token — and that may violate [Discord's Terms of Service](https://discord.com/terms).
- Using a user token for automated actions can lead to **account suspension or termination**.
- You should only use this on **your own account** and in servers where you have permission to manage messages.

> Additionally:
- This tool **respects rate limits** and pauses if hit (429 status).
- It **does not bypass** Discord protections. If Discord blocks deletions, the tool will fail for those messages.
- Use in **small batches** to reduce risk of detection.

🛑 Use at your own risk.  
✅ For educational and personal use only.

---

## 📎 GitHub

Repo: [https://github.com/Osayuk1/discord-mass-deleter](https://github.com/Osayuk1/discord-mass-deleter)
