import socket 
import thread
import time
import uu
import os.path

clientlist = [] #objects of client
messagesingle = [] # messages to be sent to individuals
groupslist = []
file_list = [] #[([],file_name)]
buf_size = 65536
files = {}
filestat = 0
# listonl = #(id)
#Completed So far:
#-Setting up a list of users
#-establishing connection
#-Message forwarding
#-Catering the sending of UPDATED user list
#-Creating ID
#-Making sure the online stat is up to date
#-Id generation with multiple of 5 for users 
#

class groups:
	identity=-1
	clntslist=[]
	messages=[]
	name=''
	adminlist = [] 

	def checkadmin(self,ids):
		for x in self.adminlist:
			if x==ids:
				return 1
		return 0
	
	def makeadmin(self, ids):
		for x in self.adminlist:
			if x == ids: 
				print "Already an admin!"
				return
		self.adminlist.append(ids)
		print x, " has been added as an admin."

	def removeadmin(self, ids):
		for x in self.adminlist:
			if x == ids: 
				self.adminlist.remove(x)
				return
		print ids , "Not an admin!"

	def adduser(self, ids, ownids):
		check=0
		for x in self.adminlist:
			if x==ownids:
				check=1
		if check==0:
			print "incorrect admin"
			return
		for x in self.clntslist:
			if x == ids: 
				print "Already a member!"
				return
		
		self.clntslist.append(ids)	
		print ids, " has been added to the group!."
		

	def removeuser(self, ids, ownids):
		check=0
		for x in self.adminlist:
			if x==ownids:
				check=1
		if check==0:
			print "incorrect admin"
			return
		for x in self.clntslist:
			if x == ids:
				self.clntslist.remove(x)
				return
		print ids, " is not in the group."

	def leave(self, ids):
		self.removeadmin(ids)
		for x in self.clntslist:
			if x == ids:
				self.clntslist.remove(x)
				return


	def set(self,inpt,nme, ids):
		self.identity=inpt
		self.name=nme
		self.adminlist.append(ids)

	def check(self,ids):
		for x in self.clntslist:
			if x == ids:
				return 1
		for x in self.adminlist:
			if x== ids:
				return 1
		return 0
		

class clients:
	identity=-1 # 4 digit id 
	name=''
	stat=0
	socketer = []
	def set(self,inpt,nme):
		self.identity=inpt
		self.name=nme
		self.stat=1

	def getstat(self):
		return self.stat

	def discon(self):
		self.stat=0

	def con(self):
		self.stat=1

def lookup(ids): #client
	for x in clientlist:
 		if x.identity == ids:
 			#print "yaar", x.identity
 			return 1, x
	obj=clients()
	return 0, obj

def lookupg(ids):#group
	for x in groupslist:
		if x.identity == ids:
			return 1, x
	obj = groups()
	return 0, obj

def idgeng():#group
	for x in range (9995, 0, -2):
		if x%5 == 0:
			continue
		chk,lol = lookupg(x)
		if chk==0:
			return x


def idgen():#client
	for i in range (9995, 0, -5):
		chk, lol  = lookup(i)
		if chk == 0:
			return i

def printlist():#everything
	global clientlist
	global groupslist
	print "--------------------Users----------------"
	if len(clientlist)==0:
		print"No usrs"
	else:
		for x in clientlist:
			print "Name: ", x.name ,", ID: ", x.identity,", Status: ", x.stat
	
	print "--------------------GROUPS--------------"
	if len(groupslist)==0:
		print "No groups at the moment..."
	else:
		for x in groupslist:
			print "Name: ", x.name, " ID: ",x.identity,"Users: ",x.clntslist," Admin: ",x.adminlist


def newcon(client,addr):
	client.send("Please enter your id: ")
	mesg=client.recv(1024)
	chk,naam=lookup(int(mesg))

	if chk == 1:
		client.send("Hooray")
		sndclntlist(client,naam)
		return naam
	else: 
		client.send("Not found.\n Press 1 to create a new account or press 0 to retry: ")
		msg=client.recv(1024)
		while True:
			if msg=='1' or msg== '0':
				break
			client.send("Try Again.\n Press 1 to create a new account or press 0 to retry: ")
			msg=client.recv(1024)
		if msg=='0':
			newcon(client,addr)
		else:
			obj=clients()
			client.send("Welcome to Whatsapp.\n Please Enter your name: ")
			nm=client.recv(1024)
			new_id= idgen()
			strn= "Your new id is: "
			strn+= str(new_id)
			print new_id
			obj.set(new_id,nm)
			clientlist.append(obj)
			client.send(strn)
			client.recv(1024)
			client.send("Hooray")
			sndclntlist(client,obj)
			return obj

def disconnec(obj):
	for x in clientlist:
 		if x.identity == obj.identity:
 			x.discon()
 			return
	

def looks(msg):
	print msg , " <---------------------------------------------"
	if msg[0]=="8":
		return 8
	if len(msg) < 6:
		print "lpc wtf: ",msg
		return -1

	if msg[0:4]== "9999": #server message
		return 1

	if msg[5]== "1":	#standard message
		return 2

	if msg[5]=="2":	
		return 3

	if msg[5]== "9":
		return 9

	print "5 is: ",msg[5]
	return -1



def editgrp(msg,clint,client):
	wrds = msg.split()
	print wrds
	grpid = int(wrds[2])
	chk , obj = lookupg(grpid)
	if chk == 0:
		print "invalid group."
		return
	if wrds[3]=="4":
		obj.leave(clint.identity)
		return
	#leave group 4
	chk = obj.checkadmin(clint.identity)
	if chk==0:
		print clint.name , " is not an admin of the group ",obj.name
		return
	if wrds[3]=="1":
		naam =wrds[4]
		if len(naam)!=4:
			print "Invalid id to add in group"
			return
		obj.adduser(int(naam),clint.identity)
		return
	#add 1
	if wrds[3]=="2":
		naam =wrds[4]
		if len(naam)!=4:
			print "Invalid id to delete in group"
			return
		obj.removeuser(int(naam),clint.identity)
		return
		
	#delete mem 2
	if wrds[3]=="3":
		naam =wrds[4]
		if len(naam)!=4:
			print "Invalid id to delete in group"
			return
		obj.makeadmin(int(naam))
	#add admin 3
	
	if wrds[3]=="5":
		obj.removeadmin(clint.identity)
	#leave adminship 5

def makenewgrp(msg,clint,client):
	global groupslist
	grpnaam = msg[7:] # gets the start of the group
	print msg
	counter=0
	group_mess = msg.split() #9999,4,name,usersssssss



	ids = idgeng()
	idn = clint.identity
	print ids , ".",group_mess[2], ".", idn
	obj = groups()
	obj.set(ids,group_mess[2],idn)
	for x in group_mess:
		if x == group_mess[2]:
			continue
		if x== "9999":
			continue
		if x== "4":
			continue
		obj.adduser(int(x),idn)
		print "hit", x
	groupslist.append(obj)
	print "New group ", obj.name , " has been made"


def forwardserv(msg,clint,client):
	if msg[5]=="4": #make new group
		makenewgrp(msg,clint,client)
	if msg[5]=="3":
		editgrp(msg,clint,client)

def handler(msg,clint,client):
	num=looks(msg)
	#1 simple message
	if num== -1:
		print "Incorrect message, message dumped: ",msg
		return
	
	if num== 1:
		#1 sever message
		print "Server handling in process..."
		forwardserv(msg,clint,client)
	
	if num== 2:
		forwardmsg(msg,clint,client) # id exist? list to forward ---

	if num== 3:
		print"Group treatment"
		#3 group
		forwardgrp(msg,clint,client)
		#etc
	if num == 9:
		# File
		recvfile(msg, clint, client)
	if num == 8:
		sendfile(msg,clint,client)

def sendfile(msg,clint,client):
	global file_list
	global clientlist
	wrds = msg.split()
	txt_file = wrds[1][:-4] + '.txt'
	check = os.path.isfile(txt_file)
	if check==0:
		client.secnd("8888 invalid filename")
	for x in file_list:
		if wrds[1] == x[1]:
			for y in x[0]:
				if y == clint.identity:
					mess = "file "+wrds[1]
					client.send(mess)
					f = open(txt_file,'rb')
					l = f.read(1024)
					while l:
						client.send(l)
						l=f.read(1024)
					client.send("///end///")
					f.close()
					x[0].remove(y)
					print "file sent to ", str(clint.identity)
					return
	client.send("8888 No file available")
	return
def recvfile(msg,clint,client):
	global clientlist
	global groupslist
	global messagesingle
	global file_list
	wrds = msg.split()
	data = ''
	while True:
		string = client.recv(1024)
		if(len(string)>=9):
			if (string[len(string)-9:len(string)] == "///end///"):
				data = data + string[:len(string)-9]
				break
		data = data+string
	#print data
	file_name = wrds[2]
	txt_file = wrds[2][:-4] + '.txt'
	f = open(txt_file, 'wb')
	f.write(data)
	#file receiving done
	f.close()
	time.sleep(1)
	#uu.decode('temp321.txt', 'lun.pdf')
	idn = int(wrds[0])
	for x in clientlist:
		if x.identity == idn:
			file_list.append(([idn],file_name))
			mss= str(idn)+str(clint.identity)+" <FILE AVAILABLE> "+file_name
			messagesingle.append(mss)
			return
	grpid=-1
	for x in groupslist:
		if x.identity == idn:
			grpid = x.identity
			file_list.append(([],file_name))
			for y in x.clntslist:
				if y==clint.identity:
					continue
				file_list[(len(file_list)-1)][0].append(y)
			for y in x.adminlist:
				if y==clint.identity:
					continue
				file_list[(len(file_list)-1)][0].append(y)
	mss = str(grpid)+">>"+clint.name+">>"+" <FILE AVAILABLE> "+file_name
	for x in file_list[(len(file_list)-1)][0]:
		string = str(x) + mss
		messagesingle.append(mss)
	#sendfile()
	# wrds = msg.split()
	# file_name = wrds[2]
	# f= open(file_name,'wb')
	# l = client.recv(buf_size)
	# while l:
	# 	f.write(l)
	# 	l=client.recv(buf_size)
	# 	if l == "end":
	# 		print "ENDED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	# 		break
	# f.close()
	# idn = int(wrds[0])
	# for x in clientlist:
	# 	if x.identity == idn:
	# 		file_list.append(([idn],file_name))
	# 		mss= str(idn)+str(clint.identity)+" <FILE AVAILABLE> "+file_name
	# 		messagesingle.append(mss)
	# 		return
	# grpid=-1
	# for x in groupslist:
	# 	if x.identity == idn:
	# 		grpid = x.identity
	# 		file_list.append(([],file_name))
	# 		for y in x.clntslist:
	# 			if y==clint.identity:
	# 				continue
	# 			file_list[(len(file_list)-1)][0].append(y)
	# 		for y in x.adminlist:
	# 			if y==clint.identity:
	# 				continue
	# 			file_list[(len(file_list)-1)][0].append(y)
	# mss = str(grpid)+">>"+clint.name+">>"+" <FILE AVAILABLE> "+file_name
	# for x in file_list[(len(file_list)-1)][0]:
	# 	string = str(x) + mss
	# 	messagesingle.append(mss)
	return


def forwardgrp(msg,clint,client):
	num = int(msg[0:4]) # group id
	chk,obj = lookupg(num) 
	if chk==0:
		print"Invalid group, message dumped"
		return
	chk = obj.check(clint.identity)
	if chk ==0 :
		print "Not a member of group so message dumped"
		return
	
	mess= str(obj.identity)+" <" +clint.name+"> " +msg[7:]
	for x in obj.clntslist:
		if x == clint.identity:
			continue
		st=str(x)+mess
		messagesingle.append(st)
	for x in obj.adminlist:
		if x == clint.identity:
			continue
		st=str(x)+mess
		messagesingle.append(st)
	
	return
	 
def forwardmsg(msg,clint,client):
	num = int(msg[0:4])

	pss,obj = lookup(num)

	if pss==0:
		print "incorrect id"
		return
	
	strng= msg[0:4]+ str(clint.identity)+ msg[4:] # receiver , sender
	print "Test:", strng
	messagesingle.append(strng)

	return



def getmess(clnt): ## war gaye bc
	global messagesingle
	lst=[]
	for x in messagesingle:
		if int(x[0:4])==clnt.identity:
			lst.append(x[4:]) # XXXX X blabalablabalbala
			messagesingle.remove(x) 
	return lst




def sndmsg(client,clnt): #thread that keeps sending while the user is connected
	global clientlist
	global filestat
	while True:
		
		lst=getmess(clnt)
		for x in clientlist:
			if x.identity == clnt.identity:
				clnt = x
				# client = x.socket[len(x.socket)-1]
		if clnt.stat == 0:
			return
		if len(lst)!=0 and clnt.stat !=0:
			#print "send"
			while True:
				if filestat == 0:
					break
			for x in lst:
				time.sleep(0.1)
				client.send(x)
				time.sleep(0.1)
			lst=[]
		#sends client list again and again
#clnt is the object and client is the client.send()
def sndclntlist(client,clnt):
	strng="9999"
	for x in clientlist:
 		if x.identity == clnt.identity:
 			continue
 		strng =strng+ " "+ x.name + "_"+ str(x.identity)+"_"+str(x.stat)
 	
 	strng = strng + " * "
 	for x in groupslist:
 		num = x.check(clnt.identity) #check if the user is in the group
 		print "number:", num

 		if num == 1:
 			strng=strng+" "+x.name + "_"+str(x.identity)
 	client.send(strng)
 	return


	

def func(client, addr):
	print "connected to:  ", addr
	clnt=newcon(client,addr)
	clnt.con()
	clnt.socketer = []
	(clnt.socketer).append(client)
	# (clnt.socket).append(client)
	# print client
	# print clnt.socket[len(clnt.socket)-1]
	thread.start_new_thread(sndmsg,(client,clnt)) ## this will start sending all the messages for this suer
	
	while True:
		try:
			string = client.recv(1024)
		except socket.error as msg:
			disconnec(clnt) # object client.stat= 0
			print clnt.name , " has disconnected!!!"
			break
			
		#print addr," said => ", string
		handler(string,clnt,client)
		print "clientlist: "
		for x in clientlist:
			print x.name
		sndclntlist(client,clnt)
        printlist()
		#client.send("list")

def Main():
	host='127.0.0.1'
	port=8000
	s = socket.socket()
	s.bind((host,port))
	s.listen(10) # max number of connections

	print "Waiting for new connections"
	while True:
		client, addr = s.accept()
		thread.start_new_thread(func,(client,addr))

		
if __name__=="__main__":
	Main()
