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

TELEGRAM_AUTH_URL = 'https://telegram.me/KipushkaBot?start=auth'
SEND_URL = f'https://api.telegram.org/bot6908416351:AAEnNj32A2k7NKbFBmVILiz7YNtV1F-3qlY/sendMessage'


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