#!/usr/bin/env python
import random
import socket
import time

def main():
	s = socket.socket()         # Create a socket object
	host = socket.getfqdn()     # Get local machine name
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
		handle_connection(c)

def send200(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')
		
def handle_connection(conn):
	path = conn.recv(1000).splitlines() # Should receive request from client. (GET ....)
	path_split = path[0].split(' ')
	
	send200(conn)
	
	if path_split[0] == 'GET':
		if path_split[1] == '/':
			conn.send('<html><body>')
			conn.send('<h1>Welcome to Usman\'s Web Server</h1>')
			conn.send('<div>')
			conn.send('<a href="/content">Content</a><br />')
			conn.send('<a href="/image">Image</a><br />')
			conn.send('<a href="/file">File</a><br />')
			conn.send('</div>')
			conn.send('</body></html>')
		elif path_split[1] == '/content':
			conn.send('<html><body>')
			conn.send('<h1>Content page!</h1>')
			conn.send('</body></html>')
		elif path_split[1] == '/file':
			conn.send('<html><body>')
			conn.send('<h1>File page!</h1>')
			conn.send('</body></html>')
		elif path_split[1] == '/image':
			conn.send('<html><body>')
			conn.send('<h1>Image page!</h1>')
			conn.send('</body></html>')
	elif path_split[0] == 'POST':
		conn.send('<html><body>')
		conn.send('<h1>You have posted content.</h1>')
		conn.send('</body></html>')

	conn.close()
	
if __name__ == '__main__':
   main()
