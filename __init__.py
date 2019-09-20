import time
import subprocess
from collections import deque
import re
import json
from flask import jsonify
from random import *
from flask import Flask, render_template, flash, request, url_for, redirect, make_response, session, g
import sqlite3 as sql
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

'''
@app.route('/')
def homepage():
    return render_template('pages/index.html')
    '''

@app.route('/')
def login():
    return render_template('page/login.html')


@app.route('/registerUser', methods=['POST'])
def registerUser():
    return render_template('page/register.html')


@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        mail = request.form['delete']
        with sql.connect("/var/www/FlaskApp/FlaskApp/database.db") as con:
              query = 'DELETE FROM Users WHERE email=?'
              cur = con.cursor()
              print('email')
              print(mail)
              cur.execute(query, (mail,))
              cur.execute("select * from Users")
              data = cur.fetchall()
              print(data)
              return render_template('page/admin1.html', data = data)




@app.route('/userdisplay',  methods=['POST'])
def userdisplay():
            with sql.connect("/var/www/FlaskApp/FlaskApp/database.db") as con:
                cur = con.cursor()
                cur.execute("select * from Users")
                data = cur.fetchall()
                return render_template('page/admin1.html', data = data)


@app.route('/editdb',  methods=['POST'])
def editdb():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd1 = request.form['pwd1']
        pwd2 = request.form['pwd2']

        if pwd1 == pwd2:
            with sql.connect("/var/www/FlaskApp/FlaskApp/database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Users SET name = ?, pwd = ? where email = ?",(name, pwd1, email, ))
                con.commit()
                msg = "User Info edited successfully"
                print(msg)
        else:
            msg = "Password doesnot match, re-enter the details"

        return render_template('page/admin1.html', ms=msg)


@app.route('/register',  methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd1 = request.form['pwd1']
        pwd2 = request.form['pwd2']

        if pwd1 == pwd2:
            try:
                with sql.connect("/var/www/FlaskApp/FlaskApp/database.db") as con:
                    cur = con.cursor()

                    cur.execute("INSERT INTO Users (name, role, email, pwd) VALUES (?,?,?,?)",(name,'user', email, pwd1))

                    con.commit()
                    msg = "User Registered, Please login"

            except:
                con.rollback()
                msg = "Email exists, enter a new mail id"

            finally:
                return render_template('page/login.html', msg=msg)
                con.close()
        else:
            msg = "Password doesnot match, re-enter the details"
            return render_template('page/register.html', msg=msg)


@app.route('/aregister',  methods=['GET','POST'])
def aregister():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pwd1 = request.form['pwd1']
        pwd2 = request.form['pwd2']

        if pwd1 == pwd2:
            try:
                with sql.connect("/var/www/FlaskApp/FlaskApp/database.db") as con:
                    cur = con.cursor()

                    cur.execute("INSERT INTO Users (name, email, pwd) VALUES (?,?,?)",(name, email, pwd1))

                    con.commit()
                    msg = "User successfully registered !"

            except:
                con.rollback()
                print(con)
                msg = "Email exists, enter a new mail id"

            finally:
                return render_template('page/admin1.html', msg=msg)
                con.close()
        else:
            msg = "Password doesnot match, re-enter the details"
            return render_template('page/admin1.html', msg=msg)


@app.route('/login',  methods=['GET', 'POST'])
def loginsuccess():
    if request.method == 'POST':
        session.pop('email', None)
        email = request.form['email']
        pwd = request.form['pwd']

        print(email)
        print(pwd)

        con = sql.connect("/var/www/FlaskApp/FlaskApp/database.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select pwd, name from Users where email = ?", (email,))
        data = cur.fetchone()

        if data is None:
            msg = "User not registered with these credentials, Please register"
            return render_template('page/login.html', msg=msg)
        else:
            if pwd == data[0]:
                session['email']  = email
                msg = "Login successful"
                return redirect(url_for('index', msg = msg, name = data[1]))
            else:
                msg = "Password Incorrect"
                return render_template('page/login.html', msg=msg)
    return render_template('page/login.html')

@app.route('/index')
def index():
    if g.email:
        msg = request.args['msg']
        name = request.args['name']
        return render_template('page/admin.html', msg = msg, name = name)
    return redirect(url_for('loginsuccess'))

@app.before_request
def before_request():
    g.user = None
    if 'email' in session:
        g.email = session['email']

@app.route('/getsession')
def getsession():
    if 'email' in session:
        return session['email']

    return 'Not logged in!'

@app.route('/dropsession')
def dropsession():
    session.pop('email', None)
    return 'Dropped!'

@app.route('/home', methods=['POST'])
def home():
    return render_template('page/admin1.html')


@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    status=subprocess.check_output(['cat','/sys/class/net/enp0s25/carrier'])
    if  int(status) == 1:
        return json.dumps('link detected : Yes')
    else:
        return json.dumps('link detected : No')


@app.route('/signUp', methods=['POST'])
def signUp():
    status=subprocess.check_output(['cat','/sys/class/net/enp0s25/carrier'])
    if  int(status) == 1:
        return json.dumps('link detected : Yes')
    else:
        return json.dumps('link detected : No')


@app.route('/send', methods=["GET","POST"])
def send():
    if request.method == 'POST':
        ct = time.strftime("%c")
        dest_mac = request.form['dest-mac-input']
        dest_ip = request.form['dest-ip-input']
        pat_inp= request.form['pattern-input']
        src_mac = request.form['source-mac-input']
        src_ip = request.form['source-ip-input']
        mtu_inp = request.form['mtu-input']
        option = request.form['file_name']

        if option == 'option1':
            line = 'your file name is ' + ct +'.txt'
            with open('/var/www/FlaskApp/FlaskApp/files/'+ ct +'.txt', 'w') as myFile:
                myFile.write('Destination Mac:'+ dest_mac + '\n' + 'Source Mac:'+ src_mac + '\n' + 'Destination IP:' + dest_ip + '\n' + 'Source IP:' + src_ip + '\n' + 'Pattern-input:' + pat_inp + '\n' + 'MTU:'+ mtu_inp)

        if option == 'option2':
            user_fname = request.form['user_file']
            line = 'your file name is ' + user_fname +'.txt'
            with open('/var/www/FlaskApp/FlaskApp/files/'+ user_fname +'.txt', 'w') as myFile:
                myFile.write('Destination Mac:'+ dest_mac + '\n' + 'Source Mac:'+ src_mac + '\n' + 'Destination IP:' + dest_ip + '\n' + 'Source IP:' + src_ip + '\n' + 'Pattern-input:' + pat_inp + '\n' + 'MTU:'+ mtu_inp)

        return render_template('page/index1.html',  time = line)



@app.route('/graph', methods=["GET","POST"])
def line():
    if request.method == 'POST':
        return render_template('page/line.html')


@app.route('/live-data',  methods=["POST"])
def live_data():
    r1=subprocess.check_output(['cat','/sys/class/net/enp0s25/statistics/rx_packets'])
    t1=subprocess.check_output(['cat','/sys/class/net/enp0s25/statistics/tx_packets'])
    data = [int(r1), int(t1), uniform(20,200)]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


@app.route('/bar', methods=["GET","POST"])
def bar():
    if request.method == 'POST':
        return render_template('page/bar.html')

'''
@app.route('/')
def homepage():
    return render_template('pa/index.html')

@app.route('/live-data',  methods=["POST"])
def live_data():
    r1=subprocess.check_output(['cat','/sys/class/net/enp0s25/statistics/rx_packets'])
    t1=subprocess.check_output(['cat','/sys/class/net/enp0s25/statistics/tx_packets'])
    data = [int(r1), int(t1), uniform(20,200)]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response
'''

if __name__ == "__main__":
    app.debug = True
    app.run()
