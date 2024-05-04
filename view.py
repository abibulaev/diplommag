from app import app
from flask import render_template

@app.route('/',methods=['GET', 'POST'])
def main():
    return render_template("main.html")

@app.route('/tasktable',methods=['GET', 'POST'])
def tasktable():
    return render_template("tasktable.html")