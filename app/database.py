# database for users

import shelve
import re
import requests


# database that saves the users profile and their agenda

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
            interviewList = []
            data[user] = {'name': name, 'password': password, 'machines': book, 'interview': interviewList}
    except KeyError:
        return "KeyError"

    data.close()


def bookMachine(user, clientName, machineType, date, hourStart, minuteStart, ampmStart, slot, info):
#    try:
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
                        'date': date,
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
#    except:
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
            print(db[user]['name'], "this is an old account in the database")
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
        mhour = 24
    else:
        mhour = int(hour)
    return mhour * 100 + int(minute)


# this will work as long as we keep slot lengths limited to 45
def endTime(timeStart, slot):
    rem = timeStart % 100 + int(slot)
    while rem > 60:
        timeStart += 100    # add an hour
        rem -= 60           # adjust minutes
    return timeStart + rem


def usrInterviewQA(user, company, yourself, goals, why, want, expecting, strweak, leave, describe, situation, position,
                   decision, questions):
    try:
        # open the database
        data = shelve.open('acct.db', writeback=True)
        # set the list to the user's existing list if it exists
        interviewList = data[user]['interview']

        if not interviewList:
            num = 100
        else:
            num = interviewList[-1]['id'] + 1

        print ("NUM: ", num)

        # store the agenda information in a dict
        interview = {'id': num,
                     'company': company,
                     'yourself': yourself,
                     'goals': goals,
                     'why': why,
                     'want': want,
                     'expecting': expecting,
                     'strweak': strweak,
                     'leave': leave,
                     'describe': describe,
                     'situation': situation,
                     'position': position,
                     'decision': decision,
                     'questions': questions}

        print interview
        # append to the agenada list
        interviewList.append(interview)
        # update it in the database
        data[user]['interview'] = interviewList

        data.close()
        print "interview successful"
        return "Created successfully"
    except:
        print "interview failure"
        return "Failed to create"


def getMBooking(user):
    data = shelve.open('acct.db', writeback=True)
    book = data[user]['machines']
    print book

    data.close()
    return book


def getInterview(user):
    data = shelve.open('acct.db', writeback=True)
    interviewList = data[user]['interview']
    print interviewList

    data.close()
    return interviewList
