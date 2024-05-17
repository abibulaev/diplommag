from flask import Flask, request, redirect, url_for, session
import hashlib
import hmac
import time


app = Flask(__name__)

#app.secret_key = 'YOUR_SECRET_KEY'  # Замените на свой секретный ключ

#BOT_TOKEN = '6908416351:AAEnNj32A2k7NKbFBmVILiz7YNtV1F-3qlY'  # Замените на токен вашего бота

def check_telegram_auth(auth_data):
    check_hash = auth_data['hash']
    auth_data_dict = {k: v for k, v in auth_data.items() if k != 'hash'}
    data_check_arr = [f'{k}={v}' for k, v in sorted(auth_data_dict.items())]
    data_check_string = '\n'.join(data_check_arr)

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if hash != check_hash:
        return False
    if time.time() - int(auth_data['auth_date']) > 86400:  # 1 day
        return False
    return auth_data_dict

#@app.route('/')
#def index():
    user = session.get('user')
    if user:
        return f'Hello, {user["first_name"]} {user["last_name"]}'
    return '''
    <script async src="https://telegram.org/js/telegram-widget.js?7" 
            data-telegram-login="your_bot_username" 
            data-size="large" 
            data-auth-url="/auth/telegram/callback" 
            data-request-access="write"></script>
    '''.replace('your_bot_username', 'KipushkaBot')

#@app.route('/auth/telegram/callback')
#def telegram_auth_callback():
    auth_data = request.args.to_dict()
    user_data = check_telegram_auth(auth_data)
    if user_data:
        session['user'] = user_data
        return redirect(url_for('index'))
    return 'Authorization failed.', 403

#if __name__ == '__main__':
    app.run(debug=True)
