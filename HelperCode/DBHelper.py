from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash


class DBHelper:

    def __init__(self,app):
        self.mysql = MySQL()
        app.config['MYSQL_DATABASE_USER'] = 'admin'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
        app.config['MYSQL_DATABASE_DB'] = 'javabase'
        app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        self.mysql.init_app(app)

        self.conn = self.mysql.connect()
        self.cursor = self.conn.cursor()


    def createUser(self, _name, _email, _password):
        _hashed_password = generate_password_hash(_password)
        self.cursor.callproc('sp_createUser', (_name, _email, _hashed_password))

        data = self.cursor.fetchall()
        if len(data) == 0:
            self.conn.commit()
            # return json.dumps({'html': '<span>All fields good !!</span>'})
            return json.dumps({'message': 'User created successfully'})
        else:
            return json.dumps({'error': str(data[0])})

    def validateLogin(self, username, password):
        print("Hello")
        login_query = "select * from users where username = "