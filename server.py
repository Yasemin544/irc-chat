#!/usr/bin/env python
import socket 

def parser(csocket, data):
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
		csocket.send(response)
		return 0

	elif data[0:3] == "SAY":
		response = "SOK"

	elif data[0:3] == "USR":
		response = "HEL"

	elif data[0:3] == "LSQ":
		response = "LSA"
	
	elif data[0:3] == "MSG":
		response = "MOK"

	else:
		response = "ERR"
		
	csocket.send(response)
	return 1
		


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()

port = 12345
s.bind((host,port))
s.listen(5)
c, addr = s.accept() 
while True:
   	
	print 'Got connection from', addr   
   	data = c.recv(1024) 
    
  	out = parser(c,data)	   
   	if (out == 0): #signal to close the connection between server and client
		c.send('\nThank you for connecting!\n')
		c.close() 
		break
	 







