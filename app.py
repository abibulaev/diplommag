from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import telebot
from telebot import types


app = Flask(__name__, static_folder='static')
app.config.from_object(Configuration)

db = SQLAlchemy(app)

login_manager = LoginManager(app)

#Telegram
bot = telebot.TeleBot(Configuration.BOT_TOKEN)

TELEGRAM_AUTH_URL = 'https://telegram.me/KipushkaBot?start=auth'