#!/usr/bin/env python
import random
import socket
import time

s = socket.socket()         # Create a socket object
host = socket.getfqdn() # Get local machine name
port = 9082
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port
print 'The Web server URL for this would be http://%s:%d/' % (host, port)

s.listen(5)                 # Now wait for client connection.

print 'Entering infinite loop; hit CTRL-C to exit'
while True:
    # Establish connection with client.    
    c, (client_host, client_port) = s.accept()
    print 'Got connection from', client_host, client_port
    c.recv(1000) # should receive request from client. (GET ....)
    c.send('HTTP/1.0 200 OK\n')
    c.send('Content-Type: text/html\n')
    c.send('\n')
    c.send("""
        <html>
        <body>
        <h1>Hello, world</h1> this is majeedus's Web server!
        </body>
        </html>
    """)
    c.close()
	
