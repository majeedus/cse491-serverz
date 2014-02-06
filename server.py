#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse
from urlparse import parse_qs
import cgi
import StringIO
import sys
import jinja2

#Initiate jinja2 library
loader = jinja2.FileSystemLoader('./templates')
env = jinja2.Environment(loader=loader)

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
    
def send404(conn):
    conn.send('HTTP/1.0 404 NOT FOUND\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')

def send501(conn):
    conn.send('HTTP/1.0 501 Not Implemented\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n')   
		
def handle_connection(conn):
	# Get the request type and folder
	request_init = ''
	while True:
		request_init += conn.recv(1)
		if '\r\n\r\n' in request_init:
			break
		
	request = StringIO.StringIO(request_init)
	server = {}
	server['REQUEST_METHOD'], path, \
	server['SERVER_PROTOCOL'] = request.readline().split()
	
	# Grab the path
	path = urlparse(path)
	server['PATH_INFO'] = path.path
	server['QUERY_STRING'] = path.query
	
	# Parse the query string
	if server['REQUEST_METHOD'] == 'GET':
		getRequest(conn, server, request)
	elif server['REQUEST_METHOD'] == 'POST':
		postRequest(conn, server, request)
	##else
		##send500(conn, server)
	
	conn.close()
	
def getRequest(conn, server, request):	
	if server['PATH_INFO'] == '/':
		send200(conn)
		index(conn, server)
	elif server['PATH_INFO'] == '/content':
		send200(conn)
		content(conn, server)
	elif server['PATH_INFO'] == '/file':
		send200(conn)
		file(conn, server)
	elif server['PATH_INFO'] == '/image':
		send200(conn)
		image(conn, server)
	elif server['PATH_INFO'] == '/form':
		send200(conn)
		form(conn, server)
	elif server['PATH_INFO'] == '/submit':
		submit(conn, server)
	elif server['PATH_INFO'] == '/form-post':
		send200(conn)
		form_post(conn, server)
	else:
		send404(conn)
		##error_404(conn, server)
		
	conn.close()

def PostRequest(conn, server, request):
    info = {}
    line = request.readline()
    while line != '\r\n':
        k, v = line.split(': ')
        info[k.lower()] = v.strip('\r\n')
        line = request.readline()

    if 'content-length' in info.keys():
        request = StringIO.StringIO(conn.recv(int(d['content-length'])))

    form = cgi.FieldStorage(headers=d, fp=request, server=server)

    if server['PATH_INFO'] == '/submitpost':
        send200(conn)
        post_results(conn, form)
    else:
        send404(conn)

def index(conn, server):
	conn.send(env.get_template('index.html').render())

def content(conn, server):
	conn.send(env.get_template('content.html').render())

def image(conn, server):
	conn.send(env.get_template('image.html').render())

def file(conn, server):
	conn.send(env.get_template('file.html').render())

def form(conn, server):
	conn.send(env.get_template('form.html').render())
	
def form_post(conn, server):
	conn.send(env.get_template('form_post.html').render())
			 
def submit(conn, server):
    query_string = parse_qs(server['QUERY_STRING'])
    vars = {'firstname':query_string['firstname'][0], 'lastname':query_string['lastname'][0]}

    conn.send(env.get_template('form_results.html').render(vars))

def post_results(conn, form):
	vars = {'firstname':form.getvalue('firstname'), 'lastname':form.getvalue('lastname')}
    
	conn.send(env.get_template('form_results.html').render(vars))
	

if __name__ == '__main__':
   main()
