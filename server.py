#!/usr/bin/env python
import random
import socket
import time
import imageapp
import urlparse
import cgi
import argparse
import PIL
import jinja2
import quixote
import StringIO
from StringIO import StringIO
from app import create_app
from wsgiref.validate import validator
from wsgiref.simple_server import make_server
from quixote.demo.altdemo import create_publisher

#from quixote.demo.altdemo import create_publisher
#from quixote.demo import create_publisher
#from quixote.demo.mini_demo import create_publisher

#_the_app = None
#def create_app():
	#global _the_app

	#if _the_app is None:
		#p = create_publisher()
		#_the_app = quixote.get_wsgi_app()

	#return _the_app

def handle_connection(conn, port, wsgi_app):
    info = conn.recv(1)

    # Header Info
    while info[-4:] != '\r\n\r\n':
        info += conn.recv(1)
	
	cookie_req = StringIO(info)
	cookie_req.readline()
	c_headers = {}
	c_headers['cookie'] = ''
	
	while (True):
		temp = cookie_req.readline()
		if temp == "\r\n":
			break
		
		temp = temp.split("\r\n")[0].split(":", 1)
		headers[temp[0].lower()] = temp[1]

    # Check for POST/GET
    request = info.split('\r\n')[0].split(' ')[0]

    # Grab the path
    request_type = info.split('\r\n')[0].split(' ')[1]
    url_info = urlparse.urlparse(request_type)
    request_type = url_info.path
    query = url_info.query

    content       = '';
    contentType   = '';
    wsgi_input    = '';
    content_len = 0;
    
    line_split     = info.split('\r\n')
    if request == 'POST':
        for s in line_split:
            if 'Content-Type' in s:
                contentType = s.split(' ', 1)[1]
            if 'Content-Length' in s:
                content_len = int (s.split()[1])
        for i in range(content_len):
            content += conn.recv(1)
        wsgi_input = StringIO(content)


    environ = {}
    environ['requestUEST_METHOD'] = request
    environ['PATH_INFO']      = request_type
    environ['QUERY_STRING']   = query
    environ['CONTENT_TYPE']   = contentType
    environ['CONTENT_LENGTH'] = content_len
    environ['wsgi.input']     = wsgi_input
    environ['SCRIPT_NAME'] = ''
    environ['SERVER_NAME'] = ("%s" % conn.getsockname()[0])
    environ['SERVER_PORT'] = ("%d" % conn.getsockname()[1])
    environ['wsgi.version'] = (1,0)
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.multithread'] = 0
    environ['wsgi.multiprocess'] = 0
    environ['wsgi.run_once'] = 0
    environ['wsgi.url_scheme'] = 'http'
    environ['HTTP_COOKIE'] = c_headers['cookie']

    def start_response(status, response_headers):
        conn.send('HTTP/1.0')
        conn.send(status)
        conn.send('\r\n')
        for (k,v) in response_headers:
            conn.send(k)
            conn.send(v)
        conn.send('\r\n\r\n')
	
	#app = quixote.get_wsgi_app()
	output = app(environ, start_response)
	
	app = create_app()
    #output   = wsgi_app(environ, start_response)
    #for line in output:
        #conn.send(line)
    #"""
    #ret = ["%s: %s\n" % (key, value)
           #for key, value in environ.iteritems()]
    #print ret
    #"""
    #conn.close()
    
    output = wsgi_app(environ, start_response)

    
    for line in output:
		conn.send(line)
    conn.close()

def main():
	parse = argparse.ArgumentParser()
	parse.add_argument( '-A', '--run_app', help = 'Application to run (image/altdemo/myapp)' )
	parse.add_argument( '-p', '--port_numb', help = 'Port number', type=int )
	args = parse.parse_args()
	
	# Take care of port handling
	if args.port_numb:
		port = args.port_numb
	else:
		port = random.randrange(8000,9999)
		
	# Running the new apps
	if args.run_app == "myapp":
		wsgi_app = create_app()
	elif args.run_app == "image":
		imageapp.setup()
		p = imageapp.create_publisher()
		wsgi_app = quixote.get_wsgi_app()
	elif args.run_app == "altdemo":
		p = imageapp.create()
		wsgi_app = quixote.get_wsgi_app() 
	elif args.run_app == "chat":
		import chat
		wsgi_app == chat.setup()
	elif args.run_app == "cookie":
		wsgi_app = cookie_app.wsgi_app
	elif args.run_app == "quotes":
		import quotes
		wgsgi_app = quotes.setup()
	else:
		raise Exception("Invalid app.")
	
	
	s = socket.socket()         # Create a socket object
	host = socket.getfqdn()     # Get local machine name
	s.bind((host, port))        # Bind to the port
	
	print 'Starting server on', host, port
	print 'The Web server URL for this would be http://%s:%d/' % (host, port)
	
	s.listen(5)                 # Now wait for client connection.
	
	print 'Entering infinite loop; hit CTRL-C to exit'
	while True:
		# Establish connection with client.
		c, (client_host, client_port) = s.accept()
		print 'Got connection from', client_host, client_port
		handle_connection(c, port, wsgi_app)

if __name__ == "__main__":
    main()
