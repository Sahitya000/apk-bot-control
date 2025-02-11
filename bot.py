from telebot import TeleBot

TOKEN = "your-telegram-bot-token"
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm your bot.")

bot.polling()
