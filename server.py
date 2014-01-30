#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse
from urlparse import parse_qs

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
	request = conn.recv(1000).split(' ')
	url_request = request[1]
	url_info = urlparse(url_request)
	url_path = url_info.path
	
	send200(conn)
	
	if request[0] == 'GET':
		if url_path == '/':
			index(conn, url_info)
		elif url_path == '/content':
			content(conn, url_info)
		elif url_path == '/files':
			files(conn, url_info)
		elif url_path == '/images':
			images(conn, url_info)
		elif url_path == '/form':
			form(conn, url_info)
		elif url_path == '/submit':
			submit(conn, url_info, request, 'GET')
	elif request[0] == 'POST':
		if url_path == '/submiit':
			submit(conn, url_info, request, 'POST')
		else:
			post(conn, request)
			
		conn.send('<html><body>')
		conn.send('<h1>You have posted content.</h1>')
		conn.send('</body></html>')

	conn.close()

def index(conn, url_info):
	output = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<h1>Hello, world.</h1>' + \
             'This is majeedus\'s web server.</br>' + \
             '<a href="/content">Content</a></br>' + \
             '<a href="/images">Images</a></br>' + \
             '<a href="/files">Files</a></br>' + \
             '<a href="/form">Form</a></br>'
	conn.send(output)

def content(conn, url_info):
	output = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<h1>Content page!</h1>'
	conn.send(output)

def images(conn, url_info):
	output = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<h1>Images page!</h1>'
	conn.send(output)

def files(conn, url_info):
	output = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<h1>Files page!</h1>'
	conn.send(output)

def form(conn, url_info):
	output = 'HTPP/1.0 200 OK\r\n' + \
			 'Content-type: text/html\r\n\r\n' + \
			 ' \r\n' + \
			 "<form action = '/submit' method = 'GET'>" + \
			 "Enter Your First Name:<input type='text' name='first_name'>" + \
			 "Enter Your Last Name:<input type='text' name='last_name'>" + \
			 "<input type='submit' value='GET'>" + \
			 "</form>\r\n" + \
			 "<form action = '/submit' method = 'POST'>" + \
			 "Enter Your First Name:<input type='text' name='first_name'>" + \
			 "Enter Your Last Name:<input type='text' name='last_name'>" + \
			 "<input type='submit' value='POST'>" + \
			 "</form>\r\n"
	conn.send(output)
			 
def submit(conn, url_info, data, request_type):
	if request_type == "GET":
		web_info = url_info.query
	elif request_type == "POST":
		web_info = data.splitlines()[-1]
	
	info = parse_qs(web_info)
	first_name = info['first_name'][0]
	last_name = info['last_name'][0]
	
	message = 'Hello there %s %s' % (first_name, last_name)
	output = 'HTPP/1.0 200 OK\r\n' + \
			 'Content-type: text/html\r\n\r\n' + \
			 '<p>' + \
			 message +\
			 '</p>'
	conn.send(output)
	

def post(conn, url_info):
	output = 'HTTP/1.0 200 OK\r\n' + \
             'Content-type: text/html\r\n\r\n' + \
             '<h1>Hello, this is majeedus\'s web server.</h1>'
	conn.send(output)


if __name__ == '__main__':
   main()
