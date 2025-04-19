# alert_manager.py

import requests
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
LINE_NOTIFY_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')

def send_telegram_alert(message, urls=None):
    """Send alert to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    if urls:
        payload['reply_markup'] = {
            "inline_keyboard": [[{"text": f"Book {idx+1}", "url": link}] for idx, link in enumerate(urls)]
        }
    requests.post(url, json=payload)

def send_line_alert(message):
    """Send alert to Line Notify."""
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
    }
    payload = {
        "message": message
    }
    requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
