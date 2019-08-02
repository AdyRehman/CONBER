from flask import Flask, render_template, Response, flash, redirect, request, session, abort
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
import string
#import matplotlib.pyplot as plt
import numpy as np
import random
import io

usr_pws_typ = [['user1', 'pass1', 'normal'], ['user2', 'pass2', 'normal']]
df = pd.DataFrame(usr_pws_typ, columns=['username', 'password', 'type'])

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
    user = str(request.form['username'])
    password = str(request.form['password'])
    status = False
    for u in df['username']:
        if u == user :
            status = df['password'][df[df['username'] == user].index.values.astype(int)] == password
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
    return render_template('password.html')
##################################sign up new user################################
@app.route('/signup',methods = ['GET', 'POST'])
def signup():
    return render_template('signup.html')

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
