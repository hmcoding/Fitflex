# database for users

import shelve
import re
import requests


# database that saves the users profile and their info

def userAcct(name, user, password):
    print("connected")
    try:
        print("trying")
        data = shelve.open('acct.db', writeback=True)
        # if this user is not a new user, fail
        if user in data:
            data.close()
            print('failure')
            return "failure"
        # else create the password and user
        else:
            print("IN DB")
            # data = {user : [{'name' : name, 'password' : password}]}
            book = []
            plan = []
	    bookTrainer = []
            data[user] = {'name': name, 'password': password, 'machines': book, 'onePlan': plan, 'trainers': bookTrainer}
    except KeyError:
        return "KeyError"

    data.close()


def bookMachine(user, clientName, machineType, date, hourStart, minuteStart, ampmStart, slot, info):
    try:
        print("starting try")
        # get our times calculated
        timeStart = time12to24(hourStart, minuteStart, ampmStart)
        print("timeStart = ", timeStart)
        timeEnd = endTime(timeStart, slot)
        print("timeEnd = ", timeEnd)

        # open the database
        data = shelve.open('acct.db', writeback=True)

        # check if the date and time is valid
        if not machineOpen(timeStart, timeEnd, data, machineType):
            print("booking failed: unavailable date/time")
            return "Invalid Booking Time"
        else:
            # set the list to the user's existing list if it exists
            book = data[user]['machines']

            if not book:
                num = 1
            else:
                num = book[-1]['id'] + 1

            print ("NUM: ", num)

            # store the agenda information in a dict
            machines = {'id': num,
                        'clientName': clientName,
                        'machineType': machineType,
                        'date': str(date),
                        'timeStart': timeStart,
                        'timeEnd': timeEnd,
                        'slot': slot,
                        'info': info}

            print machines
            # append to the agenada list
            book.append(machines)
            # update it in the database
            data[user]['machines'] = book

            data.close()
            print "booking successful"
            return "Created successfully"

    except:
        print "booking failure"
        return "Failed to create"


def bookTrainer(user, gymGoerName, trainerName, bookDate, hourStartTime, minuteStartTime, ampmStartTime, slotTrainer, infoForTrainer):
	try:
		# open the database
		data = shelve.open('acct.db', writeback=True)
		# set the list to the user's existing list if it exists
		bookTrainer = data[user]['trainers']

		if not bookTrainer:
			num = 1
		else:
			num = bookTrainer[-1]['id'] + 1

		print ("NUM: ", num)

		# store the information in a dict
		trainers = {'id': num,
					'gymGoerName': gymGoerName,
					'trainerName': trainerName,
					'bookDate': bookDate,
					'hourStartTime': hourStartTime,
					'minuteStartTime': minuteStartTime,
					'ampmStartTime': ampmStartTime,
					'slotTrainer': slotTrainer,
					'infoForTrainer': infoForTrainer}

		print trainers

		bookTrainer.append(trainers)
		# update it in the database
		data[user]['trainers'] = bookTrainer

		data.close()
		print "booking successful"
		return "Created successfully"
	except:
		print "booking failure"
		return "Failed to create"


def machineOpen(timeStart, timeEnd, db, machineType):
    for user in db:
        try:
            myMachines = db[user]['machines']
            #print db[user]['name']
            for booking in myMachines:
                tmpStart = int(booking.get('timeStart'))
                tmpEnd = int(booking.get('timeEnd'))
                #print booking
                if booking['machineType'] == machineType and timesOverlap(timeStart, timeEnd, tmpStart, tmpEnd):
                    return False
        except:
            print(db[user]['name'], " this is an old account in the database")
    return True


def timesOverlap(start1, end1, start2, end2):
    if (start2 < start1 < end2) or (start2 < end1 < end2)\
            or (start1 < start2 < end1) or (start1 < end2 < end2)\
            or (start1 == start2) or (end1 == end2):
        return True
    else:
        return False


# we won't allow anyone to have a slot that hits 12 am
def validSlot(timeStart, slot):
    return endTime(timeStart, slot) < 2400


def time12to24(hour, minute, amPm):
    if amPm == "PM" and int(hour) != 12:
        mhour = int(hour) + 12
    elif amPm == "AM" and int(hour) == 12:
        mhour = 0
    else:
        mhour = int(hour)
    return mhour * 100 + int(minute)


def time24to12(time24):
    time24 = int(time24)
    hour = time24 / 100
    minute = time24 % 100
    amPm = "AM"
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour -= 12
        amPm = "PM"
    elif hour == 12:
        amPm = "PM"
    if minute < 10:
        minute = "0" + str(minute)
    return str(hour) + ":" + str(minute) + amPm


# this will work as long as we keep slot lengths limited to 45
def endTime(timeStart, slot):
    rem = timeStart % 100 + int(slot)
    while rem > 60:
        timeStart += 100    # add an hour
        rem -= 60           # adjust minutes
    return timeStart + rem


def workoutPlan(user, month, day, year, areas, machines, types, slot, info):
    try:
        # open the database
        data = shelve.open('acct.db', writeback=True)
        # set the list to the user's existing list if it exists
        plan = data[user]['onePlan']

        if not plan:
            num = 1
        else:
            num = plan[-1]['id'] + 1

        print ("NUM: ", num)

        onePlan = {'id': num,
                   'month': month,
                   'day': day,
                   'year': year,
                   'areas': areas,
                   'machines': machines,
                   'types': types,
                   'slot': slot,
                   'info': info}

        print onePlan

        plan.append(onePlan)
        # update it in the database
        data[user]['onePlan'] = plan

        data.close()
        print "plan successful"
        return "Created successfully"
    except:
        print "plan failure"
        return "Failed to create"


# Returns map of schedule availability,
# claimed by name or an empty string for unclaimed.
# This doesn't check for duplicate bookings in the db,
# but error handling is done in insertion into the db.
def getBookingsOfDay(month, day, year, machine):
    date = str(month) + "/" + str(day) + "/" + str(year)
    db = shelve.open('acct.db', writeback=True)

    # construct map of times and users
    m = {}
    for i in range(24):
        m[time24to12(str(i)+"00")] = ""
        m[time24to12(str(i)+"15")] = ""
        m[time24to12(str(i)+"30")] = ""
        m[time24to12(str(i)+"45")] = ""

    print m

    print "looking for " + machine
    # fill in map
    for user in db:
        try:
            for booking in db[user]['machines']:
                try:
                    if booking['machineType'] == machine:
                        #print booking['machineType'] + " == " + machine
                        try:
                            if booking['date'] == date:
                                #print booking['date'] + " == " + date
                                #print "clientName: " + booking['clientName']
                                # TODO: change booking['clientName'] to user['name'] if we remove the ability to choose booking name
                                fillBookingRange(booking['timeStart'], booking['timeEnd'], m, booking['clientName'])
                        except:
                            print "fillBookingRange failed"
                except:
                    print "lookup of booking['machineType'] failed"
        except:
            print(db[user]['name'], " this is an old account in the database")

    db.close()
    return m


# claims a range in a schedule for a given name
# error checking is in booking insertion
def fillBookingRange(start, end, m, name):
    curr = int(start)
    mend = int(end)
    while curr < mend:
        m[time24to12(curr)] = name
        curr += 15
        if curr % 100 == 60:
            curr -= 60
            curr += 100


def getMBooking(user):
    data = shelve.open('acct.db', writeback=True)
    book = data[user]['machines']
    print book

    data.close()
    return book


def getPlan(user):
    data = shelve.open('acct.db', writeback=True)
    plan = data[user]['onePlan']
    print plan

    data.close()
    return plan

def getTrainer(user):
    data = shelve.open('acct.db', writeback=True)
    plan = data[user]['trainers']
    print bookTrainer

    data.close()
    return bookTrainer
