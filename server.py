#!/usr/bin/env python
import random
import socket
import time

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

    #send a response # @UM Need a space after send 
    c.send('HTTP/1.0 200 OK\r\n')
    c.send('Content-type: text/html\r\n\r\n') # @UM Need the <html> and <body> tags
    c.send('<html><body>')					  # @UM Also needed the extra \r\n
    c.send('<h1>Hello, world.</h1>') # @UM Add the closing </h1> tag
    c.send('This is ctb\'s Web server.') # @UM As well as the closing html/body tags
    c.send('</body></html>')
    c.close()
