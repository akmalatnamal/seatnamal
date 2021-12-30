from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql_se'
app.config['MYSQL_DB'] = 'lab4ex1'

mysql = MySQL(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['uname']
        password = userDetails['pwd']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO lab4ex1(name, password) VALUES(%s, %s)",(name, password))
        mysql.connection.commit()
        cur.close()
        return 'Success'
    return render_template('index1.html')


@app.route('/posts')
def posts():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM lab4ex1")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('posts.html', userDetails=userDetails)


@app.route('/posts1', methods=['GET', 'POST'])
def posts1():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        title = userDetails['title']
        dt = userDetails['date']
        cont = userDetails['content']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts(title, date, content) VALUES(%s, %s, %s)",(title, dt, cont))
        mysql.connection.commit()
        cur.close()
        return 'Success'
    return render_template('posts1.html')
