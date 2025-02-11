from telebot import TeleBot

TOKEN = "7770495311:AAGNqugyhBStza5wnBj95GRbFnAxaNNY9X0"
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm your bot.")

bot.polling()
