import os
import time
import json
import requests
import feedparser

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN environment variable not set.")

data_file = "rss_data.json"
try:
    with open(data_file, "r") as f:
        data = json.load(f)
except:
    data = {}

CHANNELS = {
    "post_mussic": ["-1001241867627"],
    "painting": ["-1001241867627"],
    "ennium": ["-1001241867627"],
    "OneBeautifulShot": ["-1001241867627"]
}

def save_data():
    with open(data_file, "w") as f:
        json.dump(data, f)

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": False,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=15)
    except:
        pass

def format_entry(entry):
    title = entry.get("title", "")
    link = entry.get("link", "")
    summary = entry.get("summary", "")
    return f"{title}\n\n{summary}\n\n{link}"

def get_latest_id(feed):
    if not feed.entries:
        return None
    e = feed.entries[0]
    return e.get("id") or e.get("link")

while True:
    try:
        for channel, groups in CHANNELS.items():
            rss_url = f"https://rsshub.app/telegram/channel/{channel}"
            feed = feedparser.parse(rss_url)

            if not feed.entries:
                continue

            latest_entry = feed.entries[0]
            latest_id = get_latest_id(feed)

            if channel not in data:
                data[channel] = latest_id
                save_data()
                continue

            if latest_id != data[channel]:
                data[channel] = latest_id
                save_data()

                text = format_entry(latest_entry)

                for group in groups:
                    send_message(group, text)

        time.sleep(60)

    except:
        time.sleep(30)
