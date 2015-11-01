from socket import *
from struct import *
import telnetlib
import time
import sys

def recv_until(s, data):
	buf = ""
	while True:
		c = s.recv(1)
		buf += c
		if data in buf:
			break
	return buf

host = 'play.hexa.pro'
port = 12345

s = socket( AF_INET, SOCK_STREAM )
s.connect((host,port))

# Example
'''
s.send("You can send message by using this function!\n")

# receive response from server and print it!
print s.recv(1024)

# usefull function
print recv_until(s, "Welcome to HeXA Echo Service!")
'''

# Implement your exploit HERE!


# Interact with server
try:
        t = telnetlib.Telnet()
        t.sock = s
        t.interact()
        t.close()
except KeyboardInterrupt:
        pass


