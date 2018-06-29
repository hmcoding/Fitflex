#database for users

import shelve
import re
import requests

#database that saves the users profile and their agenda

def userAcct(name, user, password):
	print("connected")
	try:
		print("trying")
		data = shelve.open('acct.db', writeback = True)
		#if this user is not a new user, fail
		if user in data:
			data.close()
			print('failure')
			return "failure"
		#else create the password and user
		else:
			print("IN DB")
			#data = {user : [{'name' : name, 'password' : password}]}
			book = []
			interviewList = []
			data[user] = {'name' : name, 'password' : password, 'machines' : book, 'interview' : interviewList}
	except KeyError:
		return "KeyError"

	data.close()


def bookMachine(user, clientName, machineType, date, timeStart, timeEnd, slot, info):
	try:
		#open the database
		data = shelve.open('acct.db', writeback = True)
		#set the list to the user's existing list if it exists
		book = data[user]['machines']

		if not book:
			num = 1
		else:
			num = book[-1]['id'] + 1

		print ("NUM: ", num)

		#store the agenda information in a dict
		machines = {'id' : num,
				  'clientName' : clientName,
			  	  'machineType' : machineType,
				  'date' : date,
				  'timeStart' : timeStart,
			  	  'timeEnd' : timeEnd,
			      'slot' : slot,
			  	  'info' : info}

		print machines
		#append to the agenada list
		book.append(machines)
		#update it in the database
		data[user]['machines'] = book

		data.close()
		print "booking successful"
		return "Created successfully"
	except:
		print "booking failure"
		return "Failed to create"

def usrInterviewQA(user, company, yourself, goals, why, want, expecting, strweak, leave, describe, situation, position, decision, questions):
	try:
		#open the database
		data = shelve.open('acct.db', writeback = True)
		#set the list to the user's existing list if it exists
		interviewList = data[user]['interview']

		if not interviewList:
			num = 100
		else:
			num = interviewList[-1]['id'] + 1

		print ("NUM: ", num)

		#store the agenda information in a dict
		interview = {'id' : num,
				  'company' : company,
				  'yourself' : yourself,
			  	  'goals' : goals,
				  'why' : why,
				  'want' : want,
				  'expecting' : expecting,
			  	  'strweak' : strweak,
			      'leave' : leave,
			  	  'describe' : describe,
				'situation' : situation,
				'position' : position,
				'decision' : decision,
				'questions' : questions}

		print interview
		#append to the agenada list
		interviewList.append(interview)
		#update it in the database
		data[user]['interview'] = interviewList

		data.close()
		print "interview successful"
		return "Created successfully"
	except:
		print "interview failure"
		return "Failed to create"




def getMBooking(user):
	data = shelve.open('acct.db', writeback = True)
	book = data[user]['machines']
	print book

	data.close()
	return book

def getInterview(user):
        data = shelve.open('acct.db', writeback = True)
        interviewList = data[user]['interview']
        print interviewList

        data.close()
        return interviewList
