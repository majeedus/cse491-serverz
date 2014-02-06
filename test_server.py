import sys
import server
import requests

class FakeConnection(object):
    """
A fake connection class that mimics a real TCP socket for the purpose
of testing socket I/O.
"""
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>Welcome to Usman\'s Web Server</h1>' + \
                      '<div>' + \
                      '<a href="/content">Content</a><br />' + \
                      '<a href="/image">Image</a><br />' + \
                      '<a href="/file">File</a><br />' + \
                      '</div>' + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)


def test_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>Content page!</h1>' + \
                      '</body></html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>File page!</h1>' + \
                      '</body></html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>Image page!</h1>' + \
                      '</body></html>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")

    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>You have posted content.</h1>' + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    
