from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from HelperCode import DBHelper

app = Flask(__name__)

dbhelper = DBHelper.DBHelper(app)


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/showSignup")
def showSignup():
    return render_template("signup.html")

@app.route("/showLogin")
def showLogin():
    return render_template("login.html")

@app.route("/logIn",methods=['POST'])
def logIn():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    dbhelper.validateLogin(_email,_password)
    return json.dumps({'html': '<span>Login details passed</span>'})

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _name and _email and _password:
        return(dbhelper.createUser(_name,_email,_password))

    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})

def runApp():
    app.run()
