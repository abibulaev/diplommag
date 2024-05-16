from app import app
from flask import render_template

@app.route('/',methods=['GET', 'POST'])
def main():
    return render_template("main.html")

@app.route('/tasktable',methods=['GET', 'POST'])
def tasktable():
    return render_template("tasktable.html")

@app.route('/epictable',methods=['GET', 'POST'])
def epictaable():
    return render_template("epic.html")

@app.route('/team',methods=['GET', 'POST'])
def team():
    return render_template("team.html")
@app.route("/addtask", methods=['GET','POST'])
def addtask():
    return render_template("addtask.html")

@app.route("/taskcard", methods=['GET','POST'])
def taskcard():
    return render_template("taskcard.html")

@app.route("/epiccard", methods=['GET','POST'])
def epiccard():
    return render_template("epiccard.html")

@app.route("/addepic", methods=['GET','POST'])
def addepic():
    return render_template("addepic.html")