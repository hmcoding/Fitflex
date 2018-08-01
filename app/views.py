from app import b_app
from app.database import userAcct, bookMachine, getMBooking, workoutPlan, getPlan, getBookingsOfDay, getTrainerBookingsOfDay, time24to12, bookTrainer, getTrainer
# , usrAgenda, getAgenda, usrInterviewQA, getInterview
import requests
import re
import shelve
from flask import render_template, request, make_response, redirect, url_for

loggedIn = False
currUser = ""
email = ""


# implementation of the added user

@b_app.context_processor
def addUser():
    return dict(acct=currUser)


# Route for the index or home page
@b_app.route('/', methods=['GET', 'POST'])
def home():
    pw = ""
    acct = ""
    err = ""
    print "in register"
    print (request.method)

    # if the user is logged in, do not allow them to go back to register
    print currUser
    if currUser != "":
        return redirect(url_for('index'))

    print(request.method)
    if request.method == 'POST':
        # if the sign in button was pressed
        data = request.form['signSubmit']
        if request.form['signSubmit'] == 'submitted':
            s = shelve.open('acct.db')  # open the database
            # check if the account has been created, where user_key is the email
            try:
                print("trying...")
                if str(request.form.get('user_key')) in s:
                    # check to see if password matches the user's actual password
                    if s[str(request.form.get('user_key'))]['password'] == str(request.form.get('user_password')):
                        loggedIn = True
                        currUser = s[str(request.form.get('user_key'))]['name']
                        email = str(request.form.get('user_key'))
                        return redirect(url_for('index'))
                    # if not failure, display output
                    else:
                        pw = "Invalid credentials. Incorrect password or email."
                        return render_template('register.html', pw=pw)
                else:
                    pw = "User account is not registered."
                    return render_template('register.html', pw=pw)

            except KeyError:
                print "Account not registered"
        elif request.form['signSubmit'] == 'signUpSubmit':
            print("in signup")
            # get the name, acct, password for the user when they sign up
            name = str(request.form.get('username'))
            acct = str(request.form.get('useremail'))
            pw = str(request.form.get('userpass'))
            # store it in the database if successful
            message = userAcct(name, acct, pw)
            # if the database returns a failure
            if message == 'failure':
                err = "Email is already taken. Please try again"
                return render_template("register.html", err=err)
            # check for a valid email format
            elif re.search("@([0-9a-z][0-9a-z-]+.)+[a-z]{2,4}$", acct) is None:
                err = "Please enter a valid email address"
                print "Invalid Email Format"
                return render_template("register.html", err=err)
            elif len(pw) < 7:
                err = "Password is too short (minimum of 7 characters)"
                print "short password"
                return render_template("register.html", err=err)
            # if no error take them to index page
            else:
                err = ""
                loggedIn = True
                global currUser
                currUser = name
                global email
                email = acct
                return redirect(url_for('index'))

    # create the view for register.html
    return render_template('register.html', err=err)


# each line below connects the html page to the views.py page to redirect the links from the home page
@b_app.route('/index.html', methods=['GET', 'POST'])
def index():
    if currUser == "":
        return redirect(url_for('home'))

    # create the view for the index
    return render_template('index.html')


@b_app.route('/machines.html', methods=['GET', 'POST'])
def newbooking():
    if currUser == "":
        return redirect(url_for('home'))

    print "in booking"
    print (request.method)
    info = None

    if request.method == 'POST':
        clientName = request.form.get('clientName')
        machineType = request.form.get('machineType')
        month = request.form.get('month')
        day = request.form.get('day')
        year = request.form.get('year')
        date = str(year) + "-" + str(month) + "-" + str(day)
        #timeStart = request.form.get('timeStart')
        #timeEnd = request.form.get('timeEnd')
        hourStart = request.form.get('hourStart')
        minuteStart = request.form.get('minuteStart')
        ampmStart = request.form.get('ampmStart')
        slot = request.form.get('slot')
        info = request.form.get('info')

        alert = bookMachine(email, clientName, machineType, date, hourStart, minuteStart, ampmStart, slot, info)
        if alert == "Created successfully":
            return redirect(url_for('profile', alert=alert))
        else:
            return render_template('machines.html', alert=alert)

    return render_template('machines.html')


@b_app.route('/machines_availability.html', methods=['GET', 'POST'])
def showBookings():
    if currUser == "":
        return redirect(url_for('home'))

    print "in booking"
    print (request.method)
    info = None

    if request.method == 'POST':
        month = request.form.get('month')
        day = request.form.get('day')
        year = request.form.get('year')
        machine = request.form.get('machineType')
        scheduleMap = getBookingsOfDay(month, day, year, machine)
        print "schedule date: " + str(year) + "-" + str(month) + "-" + str(day)

        # construct lists formatted for html table
        am = []
        tmp = []
        for i in range(0, 12):
            tmp.append(time24to12(str(i) + "00"))
        am.append(tmp)
        tmp = []
        for i in range(0, 12):
            tmp.append(scheduleMap[time24to12(str(i) + "00")])
            tmp.append(scheduleMap[time24to12(str(i) + "15")])
            tmp.append(scheduleMap[time24to12(str(i) + "30")])
            tmp.append(scheduleMap[time24to12(str(i) + "45")])
        am.append(tmp)
        pm = []
        tmp = []
        for i in range(12, 24):
            tmp.append(time24to12(str(i) + "00"))
        pm.append(tmp)
        tmp = []
        for i in range(12, 24):
            tmp.append(scheduleMap[time24to12(str(i) + "00")])
            tmp.append(scheduleMap[time24to12(str(i) + "15")])
            tmp.append(scheduleMap[time24to12(str(i) + "30")])
            tmp.append(scheduleMap[time24to12(str(i) + "45")])
        pm.append(tmp)
        l = [am, pm]

        return render_template('machines_availability.html', mSchedule=l)

    return render_template('machines_availability.html')

'''
@b_app.route('/trainers_availability.html', methods=['GET', 'POST'])
def showTrainerBooking():
    if currUser == "":
        return redirect(url_for('home'))

    print "in booking"
    print (request.method)
    info = None

    if request.method == 'POST':
        tmonth = request.form.get('tmonth')
        tday = request.form.get('tday')
        tyear = request.form.get('tyear')
        tname = request.form.get('trainerName')
        tscheduleMap = getTrainerBookingsOfDay(tmonth, tday, tyear, tname)
        print "schedule date: " + str(tyear) + "-" + str(tmonth) + "-" + str(tday)

        # construct lists formatted for html table
        am = []
        tmp = []
        for i in range(0, 12):
            tmp.append(time24to12(str(i) + "00"))
        am.append(tmp)
        tmp = []
        for i in range(0, 12):
            tmp.append(tscheduleMap[time24to12(str(i) + "00")])
            tmp.append(tscheduleMap[time24to12(str(i) + "30")])
        am.append(tmp)
        pm = []
        tmp = []
        for i in range(12, 24):
            tmp.append(time24to12(str(i) + "00"))
        pm.append(tmp)
        tmp = []
        for i in range(12, 24):
            tmp.append(tscheduleMap[time24to12(str(i) + "00")])
            tmp.append(tscheduleMap[time24to12(str(i) + "30")])
        pm.append(tmp)
        l = [am, pm]

        return render_template('trainers_availability.html', mSchedule=l)

    return render_template('trainers_availability.html')
'''

@b_app.route('/plan.html', methods=['GET', 'POST'])
def newplan():
    if currUser == "":
        return redirect(url_for('home'))

    print "in new plan"
    print (request.method)
    info = None

    if request.method == 'POST':
        	month = request.form.get('month')
        	day = request.form.get('day')
        	year = request.form.get('year')
        	areas = request.form.getlist('areas')
        	machines = request.form.getlist('machines')
        	types = request.form.getlist('types')
        	slot = request.form.get('slot')
        	info = request.form.get('info')

        	palert = workoutPlan(email, month, day, year, areas, machines, types, slot, info)
        	return redirect(url_for('profile', palert=palert))
    return render_template('plan.html')


@b_app.route('/here.html', methods=['GET', 'POST'])
def newinterview():
    if currUser == "":
        return redirect(url_for('home'))

    return render_template('here.html')


@b_app.route('/weekcal.html')
def newdate():
    print currUser
    if currUser == "":
        return redirect(url_for('home'))

    #machines = getMBooking(email)
    return render_template('weekcal.html')


@b_app.route('/trainers.html', methods=['GET', 'POST'])
def newtrainer():
    if currUser == "":
        return redirect(url_for('home'))

    print "in trainers"
    print (request.method)
    info = None

    if request.method == 'POST':
        	gymGoerName = request.form.get('gymGoerName')
        	trainerName = request.form.get('trainerName')
        	bookDate = request.form.get('bookDate')
        	hourStartTime = request.form.get('hourStartTime')
        	minuteStartTime = request.form.get('minuteStartTime')
        	ampmStartTime = request.form.get('ampmStartTime')
        	slotTrainer = request.form.get('slotTrainer')
        	infoForTrainer = request.form.get('infoForTrainer')

        	talert = bookTrainer(email, gymGoerName, trainerName, bookDate, hourStartTime, minuteStartTime, ampmStartTime, slotTrainer, infoForTrainer)

        	return redirect(url_for('profile', talert=talert))

    return render_template('trainers.html')


@b_app.route('/about.html')
def aboutus():
    if currUser == "":
        return redirect(url_for('home'))

    return render_template('about.html')


@b_app.route('/signout.html')
def signout():
    global currUser
    currUser = ""
    if currUser == "":
        return redirect(url_for('home'))

    return render_template('signout.html')


@b_app.route('/profile.html')
def profile():
    print currUser
    if currUser == "":
        return redirect(url_for('home'))

    machines = getMBooking(email)
    onePlan = getPlan(email)
    trainers = getTrainer(email)

    return render_template('profile.html', machines=machines, onePlan=onePlan, trainers=trainers)
