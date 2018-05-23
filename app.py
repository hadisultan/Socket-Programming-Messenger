import socket 
import thread
import os.path
import uu
import time

messages=[]
messageg=[]
clist = [] # (name, id, stat)
groupl=[] # (name,id)
buf_size = 65536
#Completed so far on client side
#-one to one messages
#-check online


def func(s,x):
	while True:
		try:
			string = s.recv(1024)
			#
		except socket.error as msg:
			print "disconnected!!!"
			break
		print string
		if len(string) > 6:
			#storeeeee
			if string[0:4]=='9999':
				filterser(string)
			elif string[0:4]=='8888':
				print "SERVER: ", string[4:]
			elif string[0:4] == "file":
				print "Yo"
				recvfile(s, string[5:])
			else:
				messages.append(string)

# every message prtocol : "9999 6 fnadnflasnfalfndlandf"
# 

def recvfile(client, filename):
	print "Receiving file"
	data = ''
	while True:
		string = client.recv(1024)
		if(len(string)>=9):
			if (string[len(string)-9:len(string)] == "///end///"):
				data = data + string[:len(string)-9]
				break
		data = data+string
	f = open("temp321.txt", 'wb')
	f.write(data)
	f.close()
	time.sleep(0.1)
	uu.decode('temp321.txt',filename)
	time.sleep(0.1)
	os.remove('temp321.txt')
	print "file: ",filename,"received"
	return

	

def lookg(naam):
	for x in groupl:
		if x[0]== naam:
			return x[1]
	return -1

def makenewgrp(s):
	print "---------------NEW GROUP--------------"
	print "Enter a name for your group:(-1 to exit)"
	grpnaam= str(raw_input())
	if grpnaam=="-1":
		return
	usernaam="0"
	listuser=[]
	while usernaam != "-1":
		print "Enter users to add:(-1 when done)"
		print "Users: " , clist
		print "---------------------------------------"
		usernaam= str(raw_input())
		if usernaam == "-1":
			break
		usernaam = str(lookn(usernaam))
		if usernaam=="-1":
			print "XXXXXXX User not found XXXXXXX"
			continue
		print usernaam ," added"
		listuser.append(usernaam)


	finalstr="9999 4 " + grpnaam
	for x in listuser:
		finalstr=finalstr + " " + x
	s.send(finalstr)
	return



def groupmenu(s):
	
	groupid= -1

	if len(groupl)==0:
		print "You are not in any group.."
		print "Do you want to make a new group? (1=Yes , -1=No)"
		num= int(raw_input())
		if num==1:
			makenewgrp(s)
		return
	print "These are your groups:"
	print groupl
	print "Please enter the group name or press 1 to make a new group(-1 to exit)"
	while True:
		naam = str(raw_input())
		if naam == "1":
			makenewgrp(s)
			return
		if naam=="-1":
			return
		num=lookg(naam)
		groupid=num
		if num==-1:
			print "Incorrect name, please retry: (or -1 to exit):"
		else: 
			break

	print "-------------Group Menu----------------"
	print "-To add a member press 1"
	print "-To delete a member press 2"
	print "-To add an admin press 3"
	print "-To leave the group press 4"
	print "-To leave admin-ship press 5"
	print "-To go back press anything else..."
	print "----------------------------------------"
	print ""

	num = int(raw_input())
	if num==1:
		#add member
		while True:
			print "Enter name to add user or -1 to return: "
			naam= str(raw_input())
			if naam=="-1":
				return
			idn= lookn(naam)
			if idn==-1:
				print "Incorrect name, please retry..."
				continue
			sendstr="9999 3 "+str(groupid)+" 1 " + str(idn)
			s.send(sendstr)
			print "Request sent. Press -1 to exit or anything else to add more"
			naam=str(raw_input())
			if naam=="-1":
				return
	if num==2:
		while True:
			print "Enter name to remove user or -1 to return: "
			naam= str(raw_input())
			if naam=="-1":
				return
			idn= lookn(naam)
			if idn==-1:
				print "Incorrect name, please retry..."
				continue
			sendstr="9999 3 "+str(groupid)+" 2 " + str(idn)
			s.send(sendstr)
			print "Request sent. Press -1 to exit or anything else to remove more"
			naam=str(raw_input())
			if naam=="-1":
				return
		#delete mem
	if num==3:
		while True:
			print "Enter name to make admin or -1 to return: "
			naam= str(raw_input())
			if naam=="-1":
				return
			idn= lookn(naam)
			if idn==-1:
				print "Incorrect name, please retry..."
				continue
			sendstr="9999 3 "+str(groupid)+" 3 " + str(idn)
			s.send(sendstr)
			print "Request sent. Press -1 to exit or anything else to add more admin"
			naam=str(raw_input())
			if naam=="-1":
				return
		#add admin
	if num==4:
	
		sendstr="9999 3 "+str(groupid)+" 4"
		s.send(sendstr)
		print "Request sent. Press -1 to exit or anything else to add more"
		naam=str(raw_input())
		if naam=="-1":
			return
	#leave group
	if num==5:
		while True:
			print "Enter name to remove user or -1 to return: "
			naam= str(raw_input())
			if naam=="-1":
				return
			idn= lookn(naam)
			if idn==-1:
				print "Incorrect name, please retry..."
				continue
			sendstr="9999 3 "+str(groupid)+" 5"
			s.send(sendstr)
			
		#leave admin-ship
	return


def filterser(strn):
		global clist
		global groupl
		strings = strn
		if strings[0:4] == '9999':
		 	#print strings
		 	clist=[]
		 	groupl=[]
		 	mess = strings.split()#split into spaces
		 	#print mess
		 	for x in mess:
		 		if x=="*":
		 			break
		 		if x== "9999":
		 			continue
		 		temp = x.split('_')
		 		naam= temp[0]
		 		ids = temp[1]
		 		stat= temp[2]
		 		clist.append((naam,int(ids),int(stat)))
		 	check = 0
		 	for x in mess:
		 		if x== "9999":
		 			continue
		 		if x=="*":
		 			check=1
		 			continue
		 		if check==0:
		 			continue
		 		#print x
		 		temp = x.split('_')
		 		naam= temp[0]
		 		ids = temp[1]
		 		groupl.append((naam,int(ids)))
		 	return

def lookn(strn): #searches for a user and returns the id
	global clist
	global groupl
	for x in clist:
		if x[0] == strn:
			return x[1]
	for x in groupl:
		if x[0] == strn:
			return x[1]
	return -1
		
def looks(strn): #searchs for an id and returns name
	global clist
	global groupl
	for x in clist:
		if x[1]==strn:
			return x[0]
	for x in groupl:
		if x[1]==strn:
			return x[0]
	return str(strn)

# prints messages only direct messages and not group 
def printmess():
	if len(messages)==0:
		print "No messages to view at the moment..."
		return
	
	print len(messages)
	#print messages
	while len(messages)!=0:
		strings=messages[0]
		var=strings[0:4]
		naam= looks(int(var))
		print "#", naam,">> ",strings[6:]
		messages.remove(strings)
	print "--------All messages received---------"

def printonl():
	global clist
	global groupl
	print 'Online users: '
	for x in clist:
		if x[2]==1:
			print '>>',x[0]

	print 'Offline usrs: '
	for x in clist:
		if x[2]==0:
			print '>>',x[0]

	print '----------------------------------------'
	print 'Groups::'
	print groupl
	print '----------------------------------------'
	print '----------------------------------------'

def sendfile(s):
	# global buf_size
	# printonl()
	
	print "Enter whom to send to:"
	naam = raw_input()
	idn = lookn(str(naam))
	if idn == -1:
		print "incorrect!"
		return
	print "Enter file name:"
	file_name = str(raw_input())
	check = os.path.isfile(str(file_name))
	if check==False:
		print 'incorrect file_name ... returning to main menu'
		return
	#recptid 9 cat.txt
	#9995 9 cat.txt
	mess = str(idn) +" 9 "+file_name
	uu.encode(file_name, 'temp123.txt')
	f = open('temp123.txt', 'rb')
	data = f.read()
	print data
	f.close()
	s.send(mess)
	time.sleep(0.3)
	s.send(data)
	time.sleep(0.1)
	s.send('///end///')
	os.remove('temp123.txt')
	# f= open(file_name,'rb')
	# l=f.read(buf_size)
	# while l:
	# 	s.send(l)
	# 	l=f.read(buf_size)
	# 	time.sleep(0.1)
	# s.send('end')
	# f.close()
	# time.sleep(2)
	print 'sent'
	return

def reqfile(s):
	print "Enter file name:"
	file_name = str(raw_input())
	mess = "8 "+file_name
	s.send(mess)

def Main(): 
	ip='127.0.0.1' 
	port=8000 

	s = socket.socket() 
	s.connect((ip,port))
	print "....#########..."
	print ".##---------##"
	print "#---###-------#"
	print "#---###-------#"
	print "#----####-##--#"
	print "#------#####--#"
	print "###--------####"
	print "- #---#####  --"
	print "-#--## --------"
	print "-####----------"
	print "To exit type -1!"

	#Starting up and connecting with the server
	while True:
		newcon = s.recv(1024)
		if newcon == "Hooray":
			
			break
		print newcon
		if newcon[0:11]=='Your new id':
			s.send('lol')
			continue
		query = raw_input() 
		if query == "-1":
			break
		
		s.send(query)
		
	thread.start_new_thread(func,(s,0))
	#print("connection established")
	while True:
		
		query = raw_input("text to server (Enter -1 to exit and -2 for messages,-3 for online and -4 for groups and -6 for file sending and -7 for filereceiving) => ") 
		if query == "-1":
			break
		if query == "-2":
			printmess()
			continue
		if query == "-3":
			printonl()
			continue
		if query == "-4":
			groupmenu(s)
			continue
		if query == "-5":
			query = raw_input("enter username: ")
			ids = lookn(query)
			if ids == -1:
				print "incorrect username"
				continue
			if ids%5 ==0:
				string= str(ids)+" 1 "
			else:
				string= str(ids)+" 2 "	
			query=""
			print "enter message, press -1 to exit"
			while query != '-1':
				query = raw_input()
				if query == '-1':
					break
				query = string+query
				s.send(query)
			continue
		if query == "-6":
			sendfile(s)
			continue
		if query == "-7":
			reqfile(s)
			continue
		s.send(query)
		
		

	s.close()

if __name__=="__main__":
	Main()
