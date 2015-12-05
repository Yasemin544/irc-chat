#!/usr/bin/env python
import socket 

def parser(csocket, data):
	data = data.strip()
	if len(data) < 3:
		response = 'ER3'
		csocket.send(response)
		return 0

	elif data[0:3] == 'TIC':
		response = 'TOC'		
		csocket.send(response)
		return 0
		
	else:
		csocket.send('ERR')
		return 0


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()

port = 12345
s.bind((host,port))
s.listen(5)

while True:
   
   c, addr = s.accept() 
   print 'Got connection from', addr   
   data = c.recv(1024) 
    
   parser(c,data)	   
   
   c.send('\nThank you for connecting!\n')
   c.close() # Close the connection
   break






