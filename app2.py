from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask('lab5ex1')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql_se'
app.config['MYSQL_DB'] = 'lab4ex1'

mysql = MySQL(app)

@app.route('/', methods=['POST','GET'])
def index():
    if request.method=="POST":
        users = request.form
        uname = users['uname']
        passw = users['pass']
        cpass = users['cpass']
        if passw == cpass:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO lab4ex1(name, password) VALUES(%s, %s)', (uname, passw))
            mysql.connection.commit()
            cur.close()
            return redirect('/login')
        else:
            return '<h1>Use the same password for both fields.</h1>'

    return render_template("signup.html")
    # return render_template('table1.html', num1 = num, range = range)

@app.route('/login')
def login():
    return '<h1>Successfully on login page.</h1>'