import telebot
import requests


FLASK_APP_URL = 'http://127.0.0.1:5000'
API_TOKEN = '7488250784:AAFNq46e23WHYBNZvFH0uGh9wPD3MKsRqTY'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    response = requests.post(f'{FLASK_APP_URL}/telegram_auth', json={'chat_id': chat_id})
    if response.status_code == 200:
        bot.send_message(chat_id, "You have been authenticated!")
    else:
        bot.send_message(chat_id, "Authentication failed.")


def send_message(chat_id, text):
    bot.send_message(chat_id, text)

bot.polling(none_stop=True)