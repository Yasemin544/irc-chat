#!/usr/bin/env python

import socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname() 
port = 12345
s.connect((host, port))
while True:
	
	user_input = raw_input()
	s.send(user_input)

	data_recv = s.recv(1024)
	print data_recv
	if(data_recv[0:3] == "BYE"):
		s.close()
		break



