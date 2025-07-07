import aiohttp
import asyncio
import json
from dateutil import parser
from datetime import datetime, timezone

log_file = "deleted_messages_log.json"

def time_to_snowflake(dt):
    discord_epoch = 1420070400000
    millis = int(dt.timestamp() * 1000)
    return ((millis - discord_epoch) << 22)

def parse_iso_datetime(timestamp_str):
    try:
        return parser.isoparse(timestamp_str)
    except:
        return None

def is_within_range(timestamp_str, start_time, end_time):
    dt = parse_iso_datetime(timestamp_str)
    return dt and start_time <= dt <= end_time

def log_deletion(channel_id, message_id, content):
    data = {"channel_id": channel_id, "message_id": message_id, "content": content}
    try:
        with open(log_file, "a") as f:
            json.dump(data, f)
            f.write("\n")
    except Exception as e:
        print(f"Log error: {e}")

async def fetch_all_channels(session, headers, guild_id):
    url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
    async with session.get(url, headers=headers) as res:
        if res.status == 200:
            data = await res.json()
            return [ch["id"] for ch in data if ch["type"] in [0, 11, 12, 15, 5]]  # Text, thread, forum
        else:
            print("Failed to fetch channels")
            return []

async def fetch_messages(session, headers, channel_id, before=None):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    params = {"limit": 100}
    if before:
        params["before"] = before
    async with session.get(url, headers=headers, params=params) as res:
        if res.status == 200:
            return await res.json()
        elif res.status == 429:
            try:
                data = await res.json()
                wait = data.get("retry_after", 2)
            except:
                wait = 2
            print(f"Rate limit: waiting {wait}s")
            await asyncio.sleep(wait)
            return await fetch_messages(session, headers, channel_id, before)
        else:
            return []

async def delete_message(session, headers, channel_id, message_id, content):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
    while True:
        async with session.delete(url, headers=headers) as res:
            if res.status in [200, 204]:
                print(f"Deleted: {message_id} | {content}")
                log_deletion(channel_id, message_id, content)
                return
            elif res.status == 429:
                try:
                    data = await res.json()
                    wait = data.get("retry_after", 2)
                except:
                    wait = 2
                print(f"Rate limit: waiting {wait}s")
                await asyncio.sleep(wait)
            else:
                print(f"Failed to delete {message_id} in {channel_id}, status {res.status}")
                return

async def process_channel(session, headers, channel_id, user_id, start_time, end_time, start_snowflake):
    before = str(start_snowflake)
    while True:
        msgs = await fetch_messages(session, headers, channel_id, before)
        if not msgs:
            break

        ranged_msgs = [
            m for m in msgs
            if m.get("author", {}).get("id") == user_id and is_within_range(m.get("timestamp", ""), start_time, end_time)
        ]

        if not ranged_msgs:
            print(f"No matching messages in channel {channel_id}")
        else:
            await asyncio.gather(*[
                delete_message(session, headers, channel_id, m["id"], m.get("content", ""))
                for m in ranged_msgs
            ])

        last_msg_time = msgs[-1].get("timestamp")
        if last_msg_time:
            last_dt = parse_iso_datetime(last_msg_time)
            if last_dt and last_dt < start_time:
                break
        before = msgs[-1]["id"]

async def main():
    token = input("Token: ").strip()
    guild_id = input("Guild ID: ").strip()
    user_id = input("User ID: ").strip()
    
    try:
        start_str = input("Start date (YYYY-MM-DD): ").strip()
        end_str = input("End date (YYYY-MM-DD): ").strip()
        start_time = datetime.strptime(start_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end_time = datetime.strptime(end_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except:
        print("Invalid date format. Use YYYY-MM-DD")
        return

    if start_time > end_time:
        print("Start date must be before end date.")
        return

    headers = {
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        channel_ids = await fetch_all_channels(session, headers, guild_id)
        start_snowflake = time_to_snowflake(end_time)
        for cid in channel_ids:
            await process_channel(session, headers, cid, user_id, start_time, end_time, start_snowflake)

    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
