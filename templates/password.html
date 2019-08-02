from flask import Flask, render_template, Response, flash, redirect, request, session, abort
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
import string
#import matplotlib.pyplot as plt
import numpy as np
import random
import io

############################routing#################
app = Flask(__name__)



############################initial_login/starting#######################
@app.route('/')
def initialLogin():
    print('first')
    session['logged_in'] = False
    return render_template('login.html', loginErrorStatus='false', title='Login')
def login(loginErrorStatus):
    if not session.get('logged_in'):
        print('second if')
        return render_template('login.html', loginErrorStatus=loginErrorStatus, title='Login')
    else:
        print('second else')
        return render_template('home.html', loginErrorStatus=loginErrorStatus, title='Home')


#############################login authentication##########################
@app.route('/login',methods = ['GET', 'POST'])
def do_admin_login():
    print('third')
    print(request.form['password'], request.form['username'])

    df = pd.read_csv("./static/users.csv")
    user = str(request.form['username'])
    password = str(request.form['password'])
    status = False
    for u in df['username']:
        if u == user :
            status = df['password'][df[df['username'] == user].index.values.astype(int)] == password
            print(type(status))
            print(status)
            status = status.tolist()
            print(status)
            status = status[0]
            print(status)
    if (status):
        print('fourth if')
        session['logged_in'] = True
        loginErrorStatus=False
    else:
        print('fourth else')
        loginErrorStatus='true'
    return login(loginErrorStatus)



###################################updating passwords#############################
@app.route('/password',methods = ['GET', 'POST'])
def password():
    user = str(request.form.get("username", False))
    password = str(request.form.get("password", False))
    cpassword = str(request.form.get("cpassword", False))

    print(user,password,cpassword)
    df = pd.read_csv("./static/users.csv")

    for u in df['username']:
        print('in for')
        if u == user:
            print('in if')
            if password == cpassword:
                print('in if if')
                df['password'][df[df['username'] == user].index.values.astype(int)] = password
                df.to_csv('./static/users.csv', index=False)
                loginErrorStatus = False
                return render_template('login.html', loginErrorStatus=loginErrorStatus)
            else:
                print('in if else')
                loginErrorStatus = True
                return render_template('password.html', loginErrorStatus=loginErrorStatus)
    loginErrorStatus = True
    return render_template('password.html', loginErrorStatus=loginErrorStatus)


##################################sign up new user################################
@app.route('/signup',methods = ['GET', 'POST'])
def signup():
    return render_template('signup.html')
@app.route('/signupf',methods = ['GET', 'POST'])
def signupf():
    user = str(request.form.get("username", False))
    password = str(request.form.get("password", False))
    typex = str(request.form.get("type", False))

    print(user,typex,password)
    dfu = pd.read_csv("./static/users.csv")
    dfu = dfu.append({'username': user, 'password': password, 'type': typex}, ignore_index=True)
    dfu.to_csv('./static/users.csv', index=False)
    flash('You were successfully signed up')

    if request.method == 'POST':
        return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/home")
def home():
    if(session['logged_in']):
        return render_template('home.html', title='Home')
    else:
        return render_template('login.html', title='Login')


app.secret_key = 'super secret key'
if __name__ == '__main__':
    app.debug = True
    app.run()
