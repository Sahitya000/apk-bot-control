import telebot
import os
import time
from flask import Flask, request

TOKEN = "7770495311:AAGNqugyhBStza5wnBj95GRbFnAxaNNY9X0"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# Webhook setup
@server.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# Start bot polling in case webhook fails
def start_polling():
    while True:
        try:
            bot.polling(none_stop=True, interval=3, timeout=20)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)  # Retry after delay

# Start Webhook
if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)  # Wait before setting webhook
    bot.set_webhook(url=f"https://telegram-apk-bot.onrender.com/7770495311:AAGNqugyhBStza5wnBj95GRbFnAxaNNY9X0")  # Replace with your Render URL
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

    # Polling fallback
    start_polling()
