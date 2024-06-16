from app import app, login_manager, TELEGRAM_AUTH_URL, bot
from flask import render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
from models.model import *
from flask_login import login_user, logout_user
from flask_login import current_user, login_required, logout_user


login_manager.login_view = 'login'

user_data = {}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template("landing.html")

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        if (password == confirm_password) and username and email:
             passw = generate_password_hash(password)
             user = User(username=username, email=email, password_hash=passw)
             db.session.add(user)
             db.session.commit()
             return(redirect(url_for('login')))
    return render_template("registr.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if email and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))

    return render_template("log_in.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('main.html', user = current_user)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    return render_template('add_project.html', user = current_user)

@app.route('/team', methods=['GET', 'POST'])
@login_required
def team():
    return render_template('team.html', user = current_user)

@app.route('/epictable', methods=['GET', 'POST'])
@login_required
def epiccard():
    return render_template('epiccard.html', user = current_user)

@app.route('/tasktable', methods=['GET', 'POST'])
@login_required
def tasktable():
    return render_template('tasktable.html', user = current_user)

@app.route('/addepic', methods=['GET', 'POST'])
@login_required
def addepic():
    return render_template('addepic.html', user = current_user)

@app.route('/addtask', methods=['GET', 'POST'])
@login_required
def addtask():
    return render_template('addtask.html', user = current_user)

@app.route('/taskcard', methods=['GET', 'POST'])
@login_required
def taskcard():
    return render_template('taskcard.html', user = current_user)

@app.route('/project', methods=['GET', 'POST'])
@login_required
def project():
    return render_template('project.html', user = current_user)

