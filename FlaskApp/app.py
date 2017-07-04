from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'javabase'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/showSignup")
def showSignup():
    return render_template("signup.html")

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _name and _email and _password:
        _hashed_password = generate_password_hash(_password)
        print(_hashed_password)
        print(len(_hashed_password))
        cursor.callproc('sp_createUser',(_name, _email,_hashed_password))

        data = cursor.fetchall()
        if len(data)==0:
            conn.commit()
            #return json.dumps({'html': '<span>All fields good !!</span>'})
            return json.dumps({'message':'User created successfully'})
        else:
            return json.dumps({'error':str(data[0])})

    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})

if __name__ =="__main__":
    app.run()