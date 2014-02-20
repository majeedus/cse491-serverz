import sys
import server

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


def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>Welcome to majeedus\'s Web Server</h1>' in conn.sent, \
    'Got: %s' % (repr(conn.sent),)


def test_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>Content Page!</h1>' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>File Page!</h1>' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>Image Page!</h1>' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_form_get():
    conn = FakeConnection("GET /submit?firstname=Usman&lastname=Majeed HTTP/1.0\r\n\r\n")
    
    server.handle_connection(conn)

    assert 'HTTP/1.0200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert 'Hello Usman Majeed!' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_form_page_get():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<form action="/submit" method="GET">' in conn.sent, 'Got: %s' % (repr(conn.sent),)

#def test_form_page_post():
    #conn = FakeConnection("GET /formpost HTTP/1.0\r\n\r\n")

    #server.handle_connection(conn)

    #assert 'HTTP/1.0200 OK\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    #assert '<form action="submit?" method="POST">' in conn.sent, 'Got: %s' % (repr(conn.sent),)

def test_404_error():
    conn = FakeConnection("GET /404 HTTP/1.0\r\n\r\n")

    server.handle_connection(conn)

    assert 'HTTP/1.0404 NOT FOUND\r\n' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<h1>404 NOT FOUND</h1>' in conn.sent, 'Got: %s' % (repr(conn.sent),)
    assert '<p>Could not find /404, please try again.</p>' in conn.sent, 'Got: %s' % (repr(conn.sent),)




