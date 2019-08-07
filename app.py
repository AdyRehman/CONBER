from flask import Flask, render_template, Response, flash, redirect, request, session, abort
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd
import io

############################routing#################
app = Flask(__name__)

df2 = pd.read_csv("./static/call_record_data.csv")
def create_revenue_by_call_timing_figure():
    tempdf = df2.copy()
    tempdf.columns = [column.replace(" ", "_") for column in tempdf.columns]
    timingList = tempdf.Call_Timing.unique()
    timingListValues = []
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'purple']
    for val in timingList:
        tempdf2 = tempdf
        queryResult = tempdf2.query("Call_Timing == '" + val + "'", inplace=False)
        totalCharge = queryResult['Charge'].sum()
        timingListValues.append(totalCharge)
    # Plot
    fig = plt.figure()
    plt.rcdefaults()
    plt.pie(timingListValues, labels=timingList, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    fig.tight_layout()
    return fig


def create_distribution_by_region_figure():
    tempdf = df2.copy()
    tempdf.columns = [column.replace(" ", "_") for column in tempdf.columns]
    regionList = tempdf.Origin_Region.unique()
    countValues = []
    for val in regionList:
        tempdf2 = tempdf
        queryResult = tempdf2.query("Origin_Region == '" + val + "'", inplace=False)
        count = len(queryResult)
        countValues.append(count)
    # Plot
    fig = plt.figure()
    plt.rcdefaults()
    plt.barh(regionList, countValues, align='center', alpha=0.5)
    plt.ylabel('Region')
    plt.xlabel('User Quantity')
    plt.title('User Distribution by Region')
    plt.tight_layout()
    return fig


def create_revenue_by_region_figure():
    tempdf = df2.copy()
    tempdf.columns = [column.replace(" ", "_") for column in tempdf.columns]
    regionList = tempdf.Origin_Region.unique()
    regionListValues = []
    for val in regionList:
        tempdf2 = tempdf
        queryResult = tempdf2.query("Origin_Region == '" + val + "'", inplace=False)
        totalCharge = queryResult['Charge'].sum()
        regionListValues.append(totalCharge)
    # Plot
    fig = plt.figure()
    plt.rcdefaults()
    plt.barh(regionList, regionListValues, align='center', alpha=0.5)
    plt.ylabel('Region')
    plt.xlabel('Revenue')
    plt.title('Revenue by Region')
    plt.tight_layout()
    return fig





############################initial_login/starting#######################
@app.route('/')
def initialLogin():
    print('initial login')
    session['logged_in'] = False
    return render_template('login.html', loginErrorStatus='false', title='Login')
def login(loginErrorStatus,user_type):
    if not session.get('logged_in'):
        print('incorrect user or pass')
        return render_template('login.html', loginErrorStatus=loginErrorStatus, title='Login Admin')
    elif(session.get('logged_in') and user_type == 'admin'):
        print('loading admin home')
        return render_template('home_admin.html', loginErrorStatus=loginErrorStatus, title='Home')
    elif(session.get('logged_in') and user_type == 'standard') :
        print('loading standard home')
        return render_template('home.html', loginErrorStatus=loginErrorStatus, title='Home')



#############################login authentication##########################
@app.route('/login', methods = ['GET', 'POST'])
def do_standard_login():
    df = pd.read_csv("./static/users.csv")
    user = str(request.form['username'])
    password = str(request.form['password'])
    status = False
    user_type = False
    for u in df['username']:
        if u == user:
            status = df['password'][df[df['username'] == user].index.values.astype(int)] == password
            user_type = df['type'][df[df['username'] == user].index.values.astype(int)] == 'admin'
            user_type = user_type.tolist()[0]
            status = status.tolist()
            status = status[0]
            print(user_type,' admin')
            print(status, ' in record')

    if (user_type):
        print('going to admin login')
        session['logged_in'] = True
        loginErrorStatus = False
        return login(loginErrorStatus, 'admin')
    if (status):
        session['logged_in'] = True
        loginErrorStatus=False
        return login(loginErrorStatus, 'standard')
    else:
        loginErrorStatus='true'
        return login(loginErrorStatus,'none')


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
###############################home ################################
@app.route("/home")
def home():
    if(session['logged_in']):
        return render_template('home.html', title='Home')
    else:
        return render_template('login.html', title='Login')

####################################### about #####################
@app.route("/about")
def about():
    return render_template('about.html', title='Login')

################################call records basic stats##############
@app.route('/callRecords_basic_stats')
def callRecords_basic_stats():
    tempdf = df2.copy()
    tempdf.columns = [column.replace(" ", "_") for column in tempdf.columns]
    totalAverageCallTime = tempdf['Duration'].mean()
    tdf2 = tempdf.groupby('Call_Type').count()
    quantMMS = tdf2.iloc[0][0]
    quantText = tdf2.iloc[1][0]
    quantVoice = tdf2.iloc[2][0]
    quantWeb = tdf2.iloc[3][0]
    durationMax = tempdf['Duration'].max()
    durationMin = tempdf['Duration'].min()
    totalRevenue = tempdf['Charge'].sum()
    return render_template('callRecords_basic_stats.html', totalAverageCallTime=totalAverageCallTime,
                           quantText=quantText, quantMMS=quantMMS, quantWeb=quantWeb, quantVoice=quantVoice,
                           durationMax=durationMax, durationMin=durationMin, totalRevenue=totalRevenue)

###################################### revenue by call timing ####################
@app.route("/revenue_by_call_timing")
def revenue_by_call_timing():
    return render_template('revenue_by_call_timing.html', title='Report')


@app.route('/revenue_by_call_timing_img.png')
def revenue_by_call_timing_img():
    fig = create_revenue_by_call_timing_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



####################################### revenue by region ########################
@app.route("/revenue_by_region")
def revenue_by_region():
    return render_template('revenue_by_region.html', title='Report')

@app.route('/revenue_by_region_img.png')
def revenue_by_region_img():
    fig = create_revenue_by_region_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


####################################### revenue by customers #####################
@app.route("/revenue_by_customer")
def revenue_by_customer():
    tempdf = df2.copy()
    tempdf.columns = [column.replace(" ", "_") for column in tempdf.columns]
    customerList = tempdf.Origin_Customer_ID.unique()
    customerList.sort()
    stringOutputList = []
    for val in customerList:
        tempdf2 = tempdf.copy()
        queryResult = tempdf2.query("Origin_Customer_ID == " + str(val), inplace=False)
        totalCharge = queryResult['Charge'].sum()
        tString = "Customer ID " + str(val) + ": " + str(totalCharge)
        stringOutputList.append(tString)
    return render_template('revenue_by_customer.html', stringOutputList=stringOutputList, title='Report')

####################################### notable customers #####################
@app.route("/notable_customers")
def notable_customers():
    tempdf = df2.copy()
    tempdf.columns = [column.replace(" ", "_") for column in tempdf.columns]
    customerList = tempdf.Origin_Customer_ID.unique()
    totalChargeList = []
    for val in customerList:
        tempdf2 = tempdf.copy()
        queryResult = tempdf2.query("Origin_Customer_ID == " + str(val), inplace=False)
        totalCharge = queryResult['Charge'].sum()
        totalChargeList.append(totalCharge)

    tempDict = {'Customers': customerList, 'Total_Charge': totalChargeList}
    tempdf3 = pd.DataFrame(tempDict)
    tempdf3 = tempdf3.sort_values(by=['Total_Charge'], ascending=False)
    top10df = tempdf3.head(10)
    bottom10df = tempdf3.tail(10)
    bottom10df = bottom10df.sort_values(by=['Total_Charge'])

    dfTop10CustomerList = list(top10df['Customers'])
    dfTop10TotalChargeList = list(top10df['Total_Charge'])
    highOutputList = []
    for i in range(len(dfTop10CustomerList)):
        highOutputList.append(
            "Customer ID: " + str(dfTop10CustomerList[i]) + "  Total Revenue: " + str(dfTop10TotalChargeList[i]))

    dfBottom10CustomerList = list(bottom10df['Customers'])
    dfBottom10TotalChargeList = list(bottom10df['Total_Charge'])
    lowOutputList = []
    for i in range(len(dfBottom10CustomerList)):
        lowOutputList.append(
            "Customer ID: " + str(dfBottom10CustomerList[i]) + "  Total Revenue: " + str(dfBottom10TotalChargeList[i]))

    return render_template('notable_customers.html', highOutputList=highOutputList, lowOutputList=lowOutputList,title='Report')

app.secret_key = 'super secret key'
if __name__ == '__main__':
    app.debug = True
    app.run()
