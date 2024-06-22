from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import requests


app = Flask(__name__, static_folder='static')
app.config.from_object(Configuration)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)

TELEGRAM_AUTH_URL = 'https://telegram.me/ItPlaner_bot?start=auth'
SEND_URL = f'https://api.telegram.org/bot7488250784:AAFNq46e23WHYBNZvFH0uGh9wPD3MKsRqTY/sendMessage'


def send_notification(chat_id, message):
    telegram_url = SEND_URL
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(telegram_url, json=payload)
    return response

def mass_send_notification(chat_ids, message):
    telegram_url = SEND_URL
    for i in chat_ids:
        payload = {
            'chat_id': i.chat_id,
            'text': message
        }
        response = requests.post(telegram_url, json=payload)
        return response