from flask import Flask, request
import telebot
import config

app = Flask(__name__)
bot = telebot.TeleBot(config.BOT_TOKEN)

@app.route('/' + config.BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
