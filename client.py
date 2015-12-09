#!/usr/bin/env python

import socket
import sys
import threading
import Queue
import time

class ReadThread (threading.Thread):
	def __init__(self, name, csoc, threadQueue, screenQueue):
		threading.Thread.__init__(self)
		self.name = name
		self.csoc = csoc
		self.nickname = ""
		self.threadQueue = threadQueue
		self.screenQueue = screenQueue

	def incoming_parser(self, data):
		if(data[0:3] == "TOC"):
			print "tic*toc"	
		
		elif(data[0:3] == "BYE"):
			self.csoc.close()
			return "CLS" #close socket signal		

	def run(self):
		while True: #for user login
			user_input = raw_input()
			s.send(user_input)
			data = self.csoc.recv(1024)
			print data
			if(data[0:3] == "HEL"):
				break
			
		while True: ##for default client commands
			user_input = raw_input()
			s.send(user_input)
			data = self.csoc.recv(1024)
			print data
			result = self.incoming_parser(data)
			if(result == "CLS"): #close socket signal
				break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname() 
port = 12345
s.connect((host, port))
sendQueue = Queue.Queue(10);
screenQueue = Queue.Queue(10);

rt = ReadThread("ReadThread", s, sendQueue, screenQueue)
rt.start()
rt.join()
s.close()





