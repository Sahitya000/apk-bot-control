import json
import logging
import os
import requests
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher

# Bot token & Webhook URL
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Flask App
app = Flask(__name__)
bot = Bot(token=TOKEN)

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Load Links
def load_links():
    with open("links.json", "r") as f:
        return json.load(f)

# Start command
def start(update, context):
    update.message.reply_text("Welcome! Send me a command.")

# Handle messages
def handle_message(update, context):
    text = update.message.text
    links = load_links()

    if text in links:
        update.message.reply_text(f"Here is your link: {links[text]}")
    else:
        update.message.reply_text("Sorry, no link found.")

# Webhook Route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "OK", 200

# Polling Function
def run_polling():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    dp = Dispatcher(bot, None, use_context=True)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Set webhook
    bot.setWebhook(f"{WEBHOOK_URL}/{TOKEN}")

    # Flask server start karo
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
