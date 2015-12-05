#!/usr/bin/env python

import socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostname() 
port = 12345 
s.connect((host, port))
user_input = raw_input()
s.send(user_input)

print s.recv(1024)

s.close()

