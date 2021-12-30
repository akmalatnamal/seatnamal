import datetime
from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
from datetime import timedelta

app = Flask('lab5ex1')
app.secret_key = 'se_lab'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql_se'
app.config['MYSQL_DB'] = 'namal'

mysql = MySQL(app)
@app.route('/', methods=['POST', 'GET'])
def index():
    msg = ''
    if request.method =="POST":
        userdata = request.form
        fname = userdata['name']
        uname = userdata['uname']
        passw = userdata['pass']
        cpass = userdata['cpass']
        email = userdata['email']
        if passw == cpass:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO users (id, name, uname, pass, email) VALUES (NULL, %s, %s, %s, %s)',(fname, uname, passw, email))
            mysql.connection.commit()
            cur.close()
            return redirect('/login')
        else:
            msg = 'Password does not match!\nPlease try again!'

    return render_template('signup.html', msg=msg)

@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method=='POST':
        data = request.form
        uname = data['uname']
        passw = data['pass']
        cur = mysql.connection.cursor()
        try:
            assert cur.execute('select uname, pass from users where uname=%s and pass=%s', (uname, passw))
        except:
            msg = 'Insertion Error!'
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
    return render_template('login.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    ses = ''
    if session['loggedin'] == True:
        return render_template('dashboard.html', id=session['id'], uname=session['username'])
    else:
        return render_template('login.html')
    # if 'loggedin' not in session:
    #     ses = 'Session timed out, please login again.'
    #     return render_template('login.html', ses=ses)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/formupload', methods=['GET', 'POST'])
def formupload():
    if request.method == 'POST':
        user = session['username']
        file = request.files['photo']
        file.save()
        return redirect('/dashboard')
    render_template('formupload.html')

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=10)
    if app.permanent_session_lifetime <=datetime.timedelta(seconds=0):
        return redirect(url_for('logout'))