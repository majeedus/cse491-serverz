#!/usr/bin/env python
import random
import socket
import time
import cgi
import jinja2
import urlparse
from StringIO import StringIO
from app import create_app

def handle_connection(conn):
    info = conn.recv(1)

    # Header Info
    while info[-4:] != '\r\n\r\n':
        info += conn.recv(1)

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

    def start_response(status, response_headers):
        conn.send('HTTP/1.0')
        conn.send(status)
        conn.send('\r\n')
        for (k,v) in response_headers:
            conn.send(k)
            conn.send(v)
        conn.send('\r\n\r\n')

    wsgi_app = create_app()
    output   = wsgi_app(environ, start_response)
    for line in output:
        conn.send(line)
    """
    ret = ["%s: %s\n" % (key, value)
           for key, value in environ.iteritems()]
    print ret
    """
    conn.close()

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

if __name__ == "__main__":
    main()
