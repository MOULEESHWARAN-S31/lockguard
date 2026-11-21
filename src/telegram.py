
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram configuration missing in .env")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=15
        )

        result = response.json()

        if result.get("ok"):
            print("Telegram notification sent successfully!")
            return True

        print("Telegram API error:", result.get("description"))
        return False

    except requests.RequestException as error:
        print("Telegram connection error:", error)
        return False
