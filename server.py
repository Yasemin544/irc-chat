#!/usr/bin/env python
import sys
import socket
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Queue
import time

user_list = []

class ReadThread (threading.Thread):
	def __init__(self, name, csoc, threadQueue, screenQueue):
		threading.Thread.__init__(self)
		self.name = name
		self.csoc = csoc
		self.nickname = ""
		self.threadQueue = threadQueue
		self.screenQueue = screenQueue

	def outgoing_parser(self, data):
		
		data = data.strip()

		if len(data) == 0:
			return 1

		elif len(data) < 3:
			response = 'ER3'

		elif len(data) > 3 and not data[3] == " ":
			response = "ERR"
		
		elif data[0:3] == 'TIC':
			response = 'TOC'		
		
		elif data[0:3] == "QUI":
			response = "BYE" 
			self.csoc.send(response)
			return 0

		elif data[0:3] == "SAY":
			response = "SOK"

		elif data[0:3] == "USR":
			if data[4:] not in user_list:
				user_list.append(data[4:])
				response = "HEL " + data[4:]
			else:
				response = "REJ"

		elif data[0:3] == "LSQ":
			response = "LSA " + ":".join(user_list)
	
		elif data[0:3] == "MSG":
			response = "MOK"

		else:
			response = "ERR"
		
		self.csoc.send(response)
		return 1
	def run(self):
		while True:
			data = self.csoc.recv(1024)
			
			self.outgoing_parser(data) 
			


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()

port = 12345
s.bind((host,port))

threadID = 1;

threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
sendQueue = Queue.Queue(10);
screenQueue = Queue.Queue(10);
workQueue = Queue.Queue(10)

rt = ReadThread(threadID, s, sendQueue, screenQueue)
threads = []
threadID = 1
# Create new threads
for tName in threadList:
	s.listen(5)
	c, addr = s.accept()
	print 'Got connection from', addr
	thread = ReadThread(threadID, c, sendQueue, screenQueue)
	thread.start()
	threads.append(thread)
	threadID += 1
# Fill the queue
	queueLock.acquire()
	for word in nameList:
		workQueue.put(word)
	queueLock.release()








