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
		#print data_recv
		if(data[0:3] == "TOC"):
			print "tic*toc"			
			#s.close()
			#break
		else:
			print "ERR"

	def run(self):
		while True:
			user_input = raw_input()
			s.send(user_input)
			data = self.csoc.recv(1024)
			incoming_parser(self, data)

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





