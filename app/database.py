#database for users

import shelve
import re
import requests

#database that saves the users profile and their info

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
			data[user] = {'name' : name, 'password' : password, 'machines' : book, 'onePlan' : plan}
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

		#store the information in a dict
		machines = {'id' : num,
				  'clientName' : clientName,
			  	  'machineType' : machineType,
				  'date' : date,
				  'timeStart' : timeStart,
			  	  'timeEnd' : timeEnd,
			      'slot' : slot,
			  	  'info' : info}

		print machines
		
		book.append(machines)
		#update it in the database
		data[user]['machines'] = book

		data.close()
		print "booking successful"
		return "Created successfully"
	except:
		print "booking failure"
		return "Failed to create"

def workoutPlan(user, month, day, year, areas, machines, types, slot, info):
	try:
		#open the database
		data = shelve.open('acct.db', writeback = True)
		#set the list to the user's existing list if it exists
		plan = data[user]['plan']

		if not plan:
			num = 1
		else:
			num = plan[-1]['id'] + 1

		print ("NUM: ", num)

		
		onePlan = {'id' : num,
				  'month' : month,
				  'day' : day,
			  	  'year' : year,
				  'areas' : areas,
				  'machines' : machines,
				  'types' : types,
			  	  'slot' : slot,
			      'info' : info}

		print onePlan
		
		plan.append(onePlan)
		#update it in the database
		data[user]['onePlan'] = plan

		data.close()
		print "plan successful"
		return "Created successfully"
	except:
		print "plan failure"
		return "Failed to create"




def getMBooking(user):
	data = shelve.open('acct.db', writeback = True)
	book = data[user]['machines']
	print book

	data.close()
	return book

def getPlan(user):
        data = shelve.open('acct.db', writeback = True)
        plan = data[user]['onePlan']
        print plan

        data.close()
        return plan
