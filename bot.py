import telebot
import requests
import json
import os
import time
from flask import Flask, request

# Secure environment variables
TOKEN = os.getenv("BOT_TOKEN")  # Bot Token
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # Channel username
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Webhook URL

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# GitHub JSON URLs (Hardcoded, no security risk)
LINKS_URL = "https://raw.githubusercontent.com/Sahitya000/apk-bot-control/main/links.json"
MESSAGES_URL = "https://raw.githubusercontent.com/Sahitya000/apk-bot-control/main/messages.json"

# Function to fetch JSON data from GitHub
def fetch_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return {}

# Load messages from GitHub
messages = fetch_json(MESSAGES_URL)

# Check if user is a subscriber
def is_subscriber(user_id):
    try:
        response = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return response.status in ["member", "administrator", "creator"]
    except Exception:
        return False

# Handle messages
@bot.message_handler(content_types=["text"])
def handle_message(message):
    user_id = message.chat.id
    text = message.text.strip()

    # Load links dynamically
    links_data = fetch_json(LINKS_URL)

    if text in links_data:
        if is_subscriber(user_id):
            bot.send_message(user_id, f"✅ Here is your link:\n{links_data[text]}")
        else:
            bot.send_message(user_id, "❌ Pehle channel subscribe karo, phir link milega!")
    else:
        bot.send_message(user_id, messages.get("invalid_command", "⚠ Invalid command!"))

# Webhook setup
@server.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Polling fallback
def start_polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=3, timeout=20)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)

# Start webhook
if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")  # Secure webhook URL

    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    # Start polling fallback
    start_polling()
