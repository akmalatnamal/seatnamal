from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask("lab5ex1")

# Configure database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql_se'
app.config['MYSQL_DB'] = 'lab5ex1'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form
        uname = user['uname']
        name = user['name']
        passw = user['pass']
        cpass = user['cpass']
        dob = user['dob']
        # if passw == cpass:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(usern, name, pass, dob) VALUES(%s, %s, %s, %s)",(uname, name, passw, dob))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
        # else:
    return render_template('register.html')

@app.route('/register', methods=['GET, POST'])
def register(err=None):
    if err !=None:
        return render_template('register.html', err)
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users')
        data = cur.fetchall()
        cur.close()
        userDetails = request.form
        for d in data:
            if d[0] == userDetails['uname'] and d[1] ==userDetails['pass']:
                return 'Congratulations, you are logged in.'
        # logcheck = request.form
    return render_template('login.html')
#
# @app.route('/logged_in')
# def logged_in():
#     return 'Congratulations, you are logged in.'