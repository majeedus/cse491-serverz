#!/usr/bin/env python
import random
import socket
import time

def main():
	s = socket.socket()         # Create a socket object
	host = socket.getfqdn() # Get local machine name
	port = random.randint(8000, 9999)
	s.bind((host, port))        # Bind to the port

	print 'Starting server on', host, port
	print 'The Web server URL for this would be http://%s:%d/' % (host, port)

	s.listen(5)                 # Now wait for client connection.

	print 'Entering infinite loop; hit CTRL-C to exit'
	while True:
		# Establish connection with client.    
		c, (client_host, client_port) = s.accept()
		print 'Got connection from', client_host, client_port
		handle_connection(c, host, port)

		
def handle_connection(conn, host, port):
	path = conn.recv(1000) # Should receive request from client. (GET ....)
	path_split = path.split()
	conn.send('HTTP/1.0 200 OK\r\n')
	conn.send('Content-Type: text/html\r\n')
	conn.send('\r\n')
	conn.send("""
		<html>
		<body>
		<h1>Hello, world.</h1> 
		This is majeedus\'s Web server.
		<br/>
		URL: <a href="">http://%s:%d%s</a>
		</body>
		</html>
	""" % (host, port, path_split[1]))
	conn.close()
	
if __name__ == '__main__':
   main()
