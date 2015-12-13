#!/usr/bin/env python

import socket
import sys
import threading
import Queue
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time

nickname = ""

class ReadThread (threading.Thread):
	def __init__(self, name, csoc, sendQueue, screenQueue):
		threading.Thread.__init__(self)
		self.name = name
		self.csoc = csoc
		self.nickname = ""
		self.sendQueue = sendQueue
		self.screenQueue = screenQueue
		
	def incoming_parser(self, data):

		if(data[0:3] == "TOC"):
			result = "Connected to server"	
		
		elif(data[0:3] == "ERL"):
			result = "Please login with /nick command."

		elif(data[0:3] == "BYE"):
			result = "CLS" #close socket signal
			return result

		elif(data[0:3] == "HEL"):
			nickname = data[4:]
			result = "New nickname: " + str(nickname)

		elif(data[0:3] == "REJ"):
			result = "Nickname already exists."
		
		elif(data[0:3] == "MOK"):
			result = "Message sent to user."

		elif(data[0:3] == "MNO"):
			result = "User not found."			

		elif(data[0:3] == "SOK"):
			result = "Message sent to all users"

		elif(data[0:3] == "LSA"):
			result = "Users in the channel: " + str(data[4:])
		
		elif(data[0:3] == "ERR"):
			result = "Wrong command"

		elif(data[0:3] == "SYS"):
			self.sendQueue.put("YOK")
			result = data[4:]
		
		else:
			result = data
		
		return result

	def run(self):
		while True: #for default client commands
			data = self.csoc.recv(1024)
			result = self.incoming_parser(data)
			print result
			if len(result) > 3 :
				if(result[0:3] == "CLS"): #close socket signal
					self.screenQueue.put("Thank you for connecting!")					
					self.csoc.close()
					quit()
					break
			self.screenQueue.put(result)			

class WriteThread (threading.Thread):
	def __init__(self, name, csoc, threadQueue):
		threading.Thread.__init__(self)
		self.name = name
		self.csoc = csoc
		self.threadQueue = threadQueue
	def run(self):
		while True:
			if not (self.threadQueue).empty():
				queue_message = self.threadQueue.get()
				try:
					self.csoc.send(queue_message)
				except socket.error:
					self.csoc.close()
					break


class ClientDialog(QDialog):
	#''' An example application for PyQt. Instantiate and call the run method to run. '''
	def __init__(self, threadQueue, screenQueue):
		self.threadQueue = threadQueue
		self.screenQueue = screenQueue
		self.qt_app = QApplication(sys.argv) # create a Qt application --- every PyQt app needs one
		QDialog.__init__(self, None)# Call the parent constructor on the current object
		self.setWindowTitle('IRC Client')# Set up the window
		self.setMinimumSize(500, 200)
		self.resize(640, 480)
		self.vbox = QVBoxLayout()# Add a vertical layout
		self.vbox.setGeometry(QRect(10, 10, 621, 461))
		self.hbox = QHBoxLayout()# Add a horizontal layout
		self.sender = QLineEdit("", self)# The sender textbox
		self.channel = QTextBrowser()# The channel region
		self.channel.setMinimumSize(QSize(480, 0))
		self.send_button = QPushButton('&Send')# The send button
		self.userList = QListView()# The users' section
		self.send_button.clicked.connect(self.outgoing_parser)# Connect the Go button to its callback
		self.vbox.addLayout(self.hbox)# Add the controls to the vertical layout
		self.vbox.addWidget(self.sender)
		self.vbox.addWidget(self.send_button)
		self.hbox.addWidget(self.channel)
		self.hbox.addWidget(self.userList)
		self.timer = QTimer()# start timer
		self.timer.timeout.connect(self.updateChannelWindow)
		self.timer.start(10)# update every 10 ms
		self.setLayout(self.vbox)# Use the vertical layout for the current window

	def cprint(self, data):
		data = str(nickname) + ": " + str(data)
		self.channel.append(data)
		self.channel.append(screenQueue.get())

	def updateChannelWindow(self):
		if not (self.screenQueue).empty():		
			queue_message = self.screenQueue.get()
			self.channel.append(queue_message)

	def outgoing_parser(self):
		senderText = self.sender.text()
		data = str(senderText)
		if len(data) == 0:
			return
		if data[0] == "/":
			cmdWithParam = data.split()
			command = cmdWithParam[0][1:]
			parameters = cmdWithParam[1:]
			if command == "list":
				self.threadQueue.put("LSQ")
				self.cprint(data)

			elif command == "quit":
				self.threadQueue.put("QUI")
				self.cprint(data)

			elif command == "nick":
				self.threadQueue.put("USR " + str(parameters[0]))
				self.cprint(data)

			elif command == "msg":
				self.threadQueue.put("MSG " + str(parameters))
				self.cprint(data)

			elif command == "tic":
				self.threadQueue.put("TIC")

			else:
				self.cprint("Local: Command Error.")

		else:
			self.threadQueue.put("SAY " + data)
			self.cprint(data)
		self.sender.clear()

	def run(self):
		#''' Run the app and show the main form. '''
		self.show()
		self.qt_app.exec_()



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = "178.233.19.205"  
#host = socket.gethostname()
port = 12345
s.connect((host, port))


sendQueue = Queue.Queue(100)
screenQueue = Queue.Queue(100)
app = ClientDialog(sendQueue, screenQueue)
# start threads
rt = ReadThread("ReadThread", s, sendQueue, screenQueue)
rt.start()
wt = WriteThread("WriteThread", s, sendQueue)
wt.start()
app.run()
rt.join()
wt.join()
s.close()






